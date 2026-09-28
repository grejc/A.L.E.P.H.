"""
Pipeline de Inferência em Produção, Auditoria SIEM e Defesa Ativa para ALF-MoE.

Recursos Integrados:
1. InferencePipeline: Classificação de fluxos únicos (NFStream) ou lotes tabulares (CSV/DataFrame).
2. InferenceAuditor: Trilha de auditoria forense estruturada em JSONL (padrão SIEM) e log rotativo.
3. ActiveDefenseAgent: Agente NIPS de bloqueio automático no firewall nftables (5 min) com:
   - Proteção estrita anti-auto-bloqueio (enumeração dinâmica de interfaces, loopback e gateway)
   - Seleção direcional inteligente do IP hostil remoto
   - Notificação ativa via socket TCP ("I SEE YOU!")
4. Extrator NFStream em tempo real para as 76 features canônicas do CICDomainFeatures.
"""

import os
import sys
import time
import json
import socket
import logging
import argparse
import ipaddress
import threading
import subprocess
import atexit
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Tuple, Any, Optional, Union, Literal

# Silenciar logs excessivos do TensorFlow para treinamento limpo
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "0")
os.environ.setdefault("TF_ENABLE_ONEDNN_OPTS", "0")
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:128"

import numpy as np
import pandas as pd
import keras

from config import CONFIG
from domain_features import CICDomainFeatures
from preprocessing import Preprocessor
from neural.model import ALFMoEModel


# =============================================================================
# UTILITÁRIOS DE AUDITORIA E SERIALIZAÇÃO JSON
# =============================================================================
def _to_serializable(val: Any) -> Any:
    """Converte tipos NumPy, Path e outros objetos em tipos primitivos JSON."""
    if isinstance(val, (np.integer, int)):
        return int(val)
    elif isinstance(val, (np.floating, float)):
        return float(val) if not np.isnan(val) and not np.isinf(val) else None
    elif isinstance(val, (np.ndarray, list, tuple)):
        return [_to_serializable(x) for x in val]
    elif isinstance(val, (np.bool_, bool)):
        return bool(val)
    elif isinstance(val, Path):
        return str(val)
    elif isinstance(val, dict):
        return {str(k): _to_serializable(v) for k, v in val.items()}
    return val


def _extract_flow_metadata(
    raw_flow: Union[Dict[str, Any], pd.DataFrame, pd.Series, Any],
    sample_index: int = 0,
    override_metadata: Optional[Union[Dict[str, Any], List[Dict[str, Any]], Any]] = None,
) -> Dict[str, Any]:
    """Extrai 5-tuple de rede e metadados de identificação do fluxo bruto."""
    meta: Dict[str, Any] = {
        "flow_id": None,
        "src_ip": None,
        "src_port": None,
        "dst_ip": None,
        "dst_port": None,
        "protocol": None,
        "timestamp": None,
    }

    target_meta = None
    if override_metadata is not None:
        if isinstance(override_metadata, list):
            if len(override_metadata) > sample_index:
                target_meta = override_metadata[sample_index]
        else:
            target_meta = override_metadata

    def _extract_from_dict_like(row_dict: Dict[str, Any]) -> Dict[str, Any]:
        extracted: Dict[str, Any] = {}
        keys = {str(k).strip().lower(): k for k in row_dict.keys()}
        mappings = [
            ("flow_id", ("flow id", "flow_id", "id", "flowid")),
            ("src_ip", ("src ip", "src_ip", "source ip", "ipv4_src_addr", "ip_src", "srcip", "src")),
            ("src_port", ("src port", "src_port", "source port", "l4_src_port", "sport", "srcport")),
            ("dst_ip", ("dst ip", "dst_ip", "destination ip", "ipv4_dst_addr", "ip_dst", "dstip", "dst")),
            ("dst_port", ("dst port", "dst_port", "destination port", "l4_dst_port", "dport", "dstport")),
            ("protocol", ("protocol", "proto", "l4_protocol")),
            ("timestamp", ("timestamp", "time", "flow start time", "bidirectional_first_seen_ms")),
        ]
        for field, aliases in mappings:
            for alias in aliases:
                if alias in keys:
                    val = row_dict[keys[alias]]
                    if pd.notna(val) and val is not None and str(val).strip() not in ("", "None", "nan"):
                        extracted[field] = val
                        break
        return extracted

    def _extract_from_obj(obj: Any) -> Dict[str, Any]:
        extracted: Dict[str, Any] = {}
        if hasattr(obj, "id"):
            extracted["flow_id"] = getattr(obj, "id")
        if hasattr(obj, "src_ip"):
            extracted["src_ip"] = getattr(obj, "src_ip")
        if hasattr(obj, "src_port"):
            extracted["src_port"] = getattr(obj, "src_port")
        if hasattr(obj, "dst_ip"):
            extracted["dst_ip"] = getattr(obj, "dst_ip")
        if hasattr(obj, "dst_port"):
            extracted["dst_port"] = getattr(obj, "dst_port")
        if hasattr(obj, "protocol"):
            extracted["protocol"] = getattr(obj, "protocol")
        if hasattr(obj, "bidirectional_first_seen_ms"):
            extracted["timestamp"] = getattr(obj, "bidirectional_first_seen_ms")
        return extracted

    if target_meta is not None:
        if isinstance(target_meta, dict):
            meta.update(_extract_from_dict_like(target_meta))
        elif hasattr(target_meta, "src_ip") or hasattr(target_meta, "id"):
            meta.update(_extract_from_obj(target_meta))

    if meta.get("src_ip") is None or meta.get("dst_ip") is None:
        if hasattr(raw_flow, "src_ip") or hasattr(raw_flow, "id"):
            for k, v in _extract_from_obj(raw_flow).items():
                if meta.get(k) is None:
                    meta[k] = v
        elif isinstance(raw_flow, dict):
            for k, v in _extract_from_dict_like(raw_flow).items():
                if meta.get(k) is None:
                    meta[k] = v
        elif isinstance(raw_flow, pd.Series):
            for k, v in _extract_from_dict_like(raw_flow.to_dict()).items():
                if meta.get(k) is None:
                    meta[k] = v
        elif isinstance(raw_flow, pd.DataFrame):
            if len(raw_flow) > sample_index:
                for k, v in _extract_from_dict_like(raw_flow.iloc[sample_index].to_dict()).items():
                    if meta.get(k) is None:
                        meta[k] = v

    return meta


# =============================================================================
# SUBSISTEMA DE AUDITORIA SIEM JSONL
# =============================================================================
class InferenceAuditor:
    """
    Registrador estruturado de eventos para SOC / SIEM / Análise Forense.
    Grava eventos operacionais legíveis e trilha estruturada em JSONL com rotação.
    """

    def __init__(
        self,
        log_dir: Optional[Union[str, Path]] = None,
        enable_file: bool = True,
        enable_console: bool = False,
        enable_jsonl: bool = True,
        log_level: int = logging.INFO,
        session_timestamp: Optional[str] = None,
    ) -> None:
        target_log_dir = Path(log_dir) if log_dir else CONFIG.logs_dir
        try:
            target_log_dir.mkdir(parents=True, exist_ok=True)
            if not os.access(target_log_dir, os.W_OK):
                raise PermissionError(f"Sem permissão de escrita em {target_log_dir}")
            self.log_dir = target_log_dir
        except Exception as exc:
            fallback = Path.home() / ".alf_moe" / "logs"
            fallback.mkdir(parents=True, exist_ok=True)
            self.log_dir = fallback
            print(f"[InferenceAuditor] Aviso: Diretório de logs '{target_log_dir}' inacessível ({exc}). Usando fallback: '{self.log_dir}'")

        self.enable_file = enable_file
        self.enable_console = enable_console
        self.enable_jsonl = enable_jsonl
        self.log_level = log_level

        ts = session_timestamp or datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        self.txt_log_path = self.log_dir / f"audit_inference_{ts}.log"
        self.jsonl_log_path = self.log_dir / f"audit_inference_{ts}.jsonl"

        self.logger = logging.getLogger(f"ALF_MoE.InferenceAuditor.{ts}")
        self.logger.setLevel(log_level)
        self.logger.propagate = False

        formatter = logging.Formatter(
            fmt="%(asctime)s [%(levelname)s] [PID:%(process)d] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        if enable_file:
            from logging.handlers import RotatingFileHandler
            fh = RotatingFileHandler(self.txt_log_path, maxBytes=10 * 1024 * 1024, backupCount=5, encoding="utf-8")
            fh.setLevel(log_level)
            fh.setFormatter(formatter)
            self.logger.addHandler(fh)

        if enable_console:
            ch = logging.StreamHandler(sys.stdout)
            ch.setLevel(log_level)
            ch.setFormatter(formatter)
            self.logger.addHandler(ch)

        self._jsonl_lock = threading.Lock()

    def _write_jsonl_event(self, event: Dict[str, Any]) -> None:
        """Escreve um registro atômico no arquivo JSON Lines."""
        if not self.enable_jsonl:
            return
        event_clean = _to_serializable(event)
        event_clean["timestamp_utc"] = datetime.now().isoformat() + "Z"
        line = json.dumps(event_clean, ensure_ascii=False) + "\n"
        with self._jsonl_lock:
            with open(self.jsonl_log_path, "a", encoding="utf-8") as f:
                f.write(line)

    def log_pipeline_init(
        self,
        artifacts_dir: Path,
        dataset_name: str,
        classes: List[str],
        feature_names: List[str],
        weights_path: Path,
    ) -> None:
        self.logger.info(
            f"Pipeline de inferência inicializado: Dataset={dataset_name} | "
            f"Classes={len(classes)} | Features={len(feature_names)} | Pesos={weights_path}"
        )
        self._write_jsonl_event({
            "event_type": "PIPELINE_INIT",
            "dataset_name": dataset_name,
            "classes": classes,
            "feature_names_count": len(feature_names),
            "artifacts_dir": str(artifacts_dir),
            "weights_path": str(weights_path),
        })

    def log_flow_prediction(
        self,
        meta: Dict[str, Any],
        pred_class: str,
        confidence: float,
        is_threat: bool,
        gn_weights: Dict[str, float],
        experts_preds: Dict[str, str],
        inference_latency_ms: float,
        action_taken: str = "LOG",
    ) -> None:
        log_msg = (
            f"FLUXO [{meta.get('src_ip')}:{meta.get('src_port')} -> {meta.get('dst_ip')}:{meta.get('dst_port')}] "
            f"Predição: {pred_class} (Confiança: {confidence * 100:.1f}%) | Ação: {action_taken} | "
            f"Latência: {inference_latency_ms:.3f}ms"
        )
        if is_threat:
            self.logger.warning(log_msg)
        else:
            self.logger.info(log_msg)

        self._write_jsonl_event({
            "event_type": "FLOW_PREDICTION",
            "metadata": meta,
            "prediction": {
                "class": pred_class,
                "confidence": round(confidence, 4),
                "is_threat": is_threat,
            },
            "gating_attention_weights": {k: round(v, 4) for k, v in gn_weights.items()},
            "experts_predictions": experts_preds,
            "performance": {
                "latency_ms": round(inference_latency_ms, 3),
            },
            "action_taken": action_taken,
        })

    def log_active_defense_action(
        self,
        action: str,
        target_ip: str,
        duration_sec: int,
        details: str,
    ) -> None:
        msg = f"[DEFESA ATIVA] Ação={action} | IP={target_ip} | Duração={duration_sec}s | Detalhes={details}"
        self.logger.warning(msg)
        self._write_jsonl_event({
            "event_type": "ACTIVE_DEFENSE",
            "action": action,
            "target_ip": target_ip,
            "duration_sec": duration_sec,
            "details": details,
        })

    def log_error(self, message: str) -> None:
        self.logger.error(message)
        self._write_jsonl_event({
            "event_type": "ERROR",
            "message": message,
        })


# =============================================================================
# DEFESA ATIVA (NIPS) E ANTI-AUTO-BLOQUEIO
# =============================================================================
class _ActiveTCPResponder:
    """Socket server TCP que responde aos atacantes com a mensagem de alerta configurada."""

    def __init__(self, host: str = "127.0.0.1", port: int = 9999, response_text: str = "I SEE YOU!") -> None:
        self.host = host
        self.port = port
        self.response_text = response_text
        self.server_socket: Optional[socket.socket] = None
        self.thread: Optional[threading.Thread] = None
        self.running: bool = False

    def start(self) -> bool:
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(128)
            self.server_socket.settimeout(1.0)
            self.running = True
            self.thread = threading.Thread(target=self._serve, name="ALF-MoE-TCPResponder", daemon=True)
            self.thread.start()
            return True
        except Exception:
            self.running = False
            return False

    def _serve(self) -> None:
        while self.running and self.server_socket:
            try:
                client_sock, _ = self.server_socket.accept()
                threading.Thread(target=self._handle_client, args=(client_sock,), daemon=True).start()
            except socket.timeout:
                continue
            except Exception:
                break

    def _handle_client(self, client_sock: socket.socket) -> None:
        try:
            client_sock.settimeout(2.0)
            resp = f"{self.response_text}\n".encode("utf-8")
            client_sock.sendall(resp)
        except Exception:
            pass
        finally:
            try:
                client_sock.close()
            except Exception:
                pass

    def stop(self) -> None:
        self.running = False
        if self.server_socket:
            try:
                self.server_socket.close()
            except Exception:
                pass
            self.server_socket = None


def get_host_local_ips() -> Set[str]:
    """Descobre dinamicamente todos os IPs locais do host para proteção anti-auto-bloqueio."""
    ips: Set[str] = {"127.0.0.1", "::1", "localhost", "0.0.0.0", "::"}
    try:
        res = subprocess.run(["ip", "-j", "addr"], capture_output=True, text=True, timeout=2)
        if res.returncode == 0:
            for iface in json.loads(res.stdout):
                for info in iface.get("addr_info", []):
                    if "local" in info:
                        raw_ip = str(info["local"]).split("%")[0].strip()
                        ips.add(raw_ip)
    except Exception:
        pass

    try:
        hostname = socket.gethostname()
        for info in socket.getaddrinfo(hostname, None):
            raw_ip = str(info[4][0]).split("%")[0].strip()
            ips.add(raw_ip)
    except Exception:
        pass

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            ips.add(s.getsockname()[0])
    except Exception:
        pass

    # IP da máquina atacante
    if "192.168.3.3" in ips:
        ips.remove("192.168.3.3")

    return ips


class ActiveDefenseAgent:
    """
    Agente NIPS com mitigação de ameaças no firewall nftables.
    - Bloqueia IP hostil por 5 minutos (flags timeout no nftables).
    - Proteção estrita anti-auto-bloqueio (nunca bloqueia interfaces locais do host).
    - Seleção direcional correta de alvos (iniciados vs recebidos).
    """

    BASE_WHITELIST = {"127.0.0.1", "::1", "localhost", "0.0.0.0", "::", "N/A", "None", "", "239.255.255.250", "255.255.255.255"}

    def __init__(
        self,
        table_name: str = "alf_defense",
        set_name: str = "blocked_ips",
        block_duration_sec: int = 300,
        response_text: str = "I SEE YOU!",
        responder_port: int = 9999,
        auditor: Optional[InferenceAuditor] = None,
        custom_whitelist: Optional[Union[List[str], Set[str], str]] = None,
    ) -> None:
        self.table_name = table_name
        self.set_name = set_name
        self.block_duration_sec = block_duration_sec
        self.response_text = response_text
        self.auditor = auditor
        self.responder_port = responder_port

        self.lock = threading.Lock()
        self.active_blocks: Dict[str, Dict[str, Any]] = {}
        self.local_ips = get_host_local_ips()
        self.whitelist = set(self.BASE_WHITELIST) | self.local_ips

        if custom_whitelist:
            if isinstance(custom_whitelist, (list, set)):
                self.whitelist.update(str(x).strip() for x in custom_whitelist)
            elif isinstance(custom_whitelist, str):
                self.whitelist.update(x.strip() for x in custom_whitelist.split(","))

        self.tcp_responder = _ActiveTCPResponder(
            host="127.0.0.1", port=self.responder_port, response_text=self.response_text
        )
        self.tcp_responder.start()

        self.is_root = (os.geteuid() == 0) if hasattr(os, "geteuid") else False
        self._init_nftables()

    def _init_nftables(self) -> None:
        """Inicializa tabela de mitigação no nftables se for root."""
        if not self.is_root:
            return
        try:
            subprocess.run(["nft", "add", "table", "inet", self.table_name], check=True, capture_output=True)
            subprocess.run(
                [
                    "nft", "add", "set", "inet", self.table_name, self.set_name,
                    "{", "type", "ipv4_addr;", "flags", "timeout;", f"timeout", f"{self.block_duration_sec}s;", "}"
                ],
                check=True,
                capture_output=True,
            )
            subprocess.run(
                ["nft", "add", "chain", "inet", self.table_name, "input", "{", "type", "filter", "hook", "input", "priority", "-10;", "policy", "accept;", "}"],
                check=True,
                capture_output=True,
            )
            subprocess.run(
                ["nft", "add", "rule", "inet", self.table_name, "input", "ip", "saddr", f"@{self.set_name}", "drop", "comment", f'"{self.response_text}"'],
                check=True,
                capture_output=True,
            )
        except Exception as exc:
            if self.auditor:
                self.auditor.log_error(f"Erro ao inicializar nftables: {exc}")

    def is_protected(self, ip: Optional[str]) -> bool:
        if not ip:
            return True
        clean = str(ip).strip()
        if clean in self.whitelist:
            return True
        try:
            ip_obj = ipaddress.ip_address(clean)
            return ip_obj.is_loopback or ip_obj.is_unspecified or ip_obj.is_link_local
        except ValueError:
            return True

    def select_target(self, src_ip: Optional[str], dst_ip: Optional[str]) -> Optional[str]:
        """Seleciona a contraparte remota para bloqueio."""
        clean_src = str(src_ip).strip() if src_ip else ""
        clean_dst = str(dst_ip).strip() if dst_ip else ""

        src_prot = self.is_protected(clean_src)
        dst_prot = self.is_protected(clean_dst)

        if src_prot and not dst_prot:
            return clean_dst
        if dst_prot and not src_prot:
            return clean_src
        if not src_prot and clean_src:
            return clean_src
        if not dst_prot and clean_dst:
            return clean_dst
        return None

    def block_ip(self, ip: str, attack_type: str = "Unknown", confidence: float = 1.0) -> bool:
        """Bloqueia endereço IP atacante por 5 minutos com proteção anti-auto-bloqueio."""
        if not ip or self.is_protected(ip):
            return False

        with self.lock:
            now = time.time()
            if ip in self.active_blocks:
                exp = self.active_blocks[ip]["expires_at"]
                if now < exp:
                    return False

            self.active_blocks[ip] = {
                "blocked_at": now,
                "expires_at": now + self.block_duration_sec,
                "attack_type": attack_type,
                "confidence": confidence,
            }

        # Aplica regra de kernel no nftables se for root
        if self.is_root:
            try:
                subprocess.run(
                    ["nft", "add", "element", "inet", self.table_name, self.set_name, "{", ip, "}"],
                    check=True,
                    capture_output=True,
                )
            except Exception as exc:
                if self.auditor:
                    self.auditor.log_error(f"Falha ao adicionar elemento no nftables para {ip}: {exc}")

        if self.auditor:
            self.auditor.log_active_defense_action(
                action="BLOCK_IP",
                target_ip=ip,
                duration_sec=self.block_duration_sec,
                details=f"Ameaça {attack_type} (confiança: {confidence*100:.1f}%) | Resposta: {self.response_text}",
            )
        print(f"\n🚨 [DEFESA ATIVA] IP BLOQUEADO: {ip} | Ameaça: {attack_type} | Duração: {self.block_duration_sec}s | Msg: {self.response_text}")
        return True

    def close(self) -> None:
        """Encerra responder TCP e limpa tabelas do firewall se aplicável."""
        self.tcp_responder.stop()
        if self.is_root:
            try:
                subprocess.run(["nft", "delete", "table", "inet", self.table_name], capture_output=True)
            except Exception:
                pass


# =============================================================================
# PIPELINE UNIFICADO DE INFERÊNCIA
# =============================================================================
class InferencePipeline:
    """
    Pipeline unificado de inferência para produção.
    Conecta fluxos de rede brutos, pré-processamento, modelo ALF-MoE, auditoria e defesa ativa.
    """

    def __init__(
        self,
        artifacts_dir: Optional[Union[str, Path]] = None,
        weights_path: Optional[Union[str, Path]] = None,
        dataset_name: str = CONFIG.preprocessing.dataset_name,
        threat_threshold: float = CONFIG.inference.threat_threshold,
        enable_active_defense: bool = CONFIG.inference.enable_active_defense,
        enable_audit: bool = CONFIG.inference.enable_audit,
    ) -> None:
        self.dataset_name = dataset_name
        self.threat_threshold = float(threat_threshold)
        self.pattern: Literal[1, 2] = 2 if "CSE-CIC-IDS2018" in self.dataset_name else 1

        if artifacts_dir is None:
            self.artifacts_dir = self._find_latest_artifacts(dataset_name)
        else:
            self.artifacts_dir = Path(artifacts_dir)

        # 1. Auditoria SIEM
        self.auditor = InferenceAuditor() if enable_audit else None

        # 2. Defesa Ativa
        self.active_defense = None
        if enable_active_defense:
            self.active_defense = ActiveDefenseAgent(
                block_duration_sec=CONFIG.inference.active_defense_duration,
                response_text=CONFIG.inference.active_response_text,
                responder_port=CONFIG.inference.active_responder_port,
                auditor=self.auditor,
                custom_whitelist=CONFIG.inference.protected_ips,
            )
            atexit.register(self.close)

        # 3. Pré-processamento
        prep_dir = self.artifacts_dir / "preprocess"
        pkl_files = (
            list(prep_dir.glob("*_artifacts.pkl"))
            + list(self.artifacts_dir.glob("*_artifacts.pkl"))
            + list(self.artifacts_dir.glob("**/*_artifacts.pkl"))
            + list(self.artifacts_dir.parent.glob("*_artifacts.pkl"))
        )
        if not pkl_files:
            raise FileNotFoundError(f"Artefatos pickle não encontrados em {self.artifacts_dir}")
        self.preprocessor = Preprocessor(dataset=dataset_name, auto_load=False).load_artifacts(pkl_files[0])

        self.classes = self.preprocessor.classes
        self.num_classes = len(self.classes)
        self.feature_names = self.preprocessor.feature_names

        # 4. Especialistas e Mapeamento
        domain_indices = self.preprocessor.get_domain_indices()

        # 5. Modelo ALF-MoE
        self.model_wrapper = ALFMoEModel(
            feature_names=self.feature_names,
            classes=self.classes,
            domain_indices=domain_indices,
            dnn_units=CONFIG.model.dnn_units,
            dnn_dropout=CONFIG.model.dnn_dropout,
            cnn_filters=CONFIG.model.cnn_filters,
            cnn_kernel_size=CONFIG.model.cnn_kernel_size,
            cnn_dense_units=CONFIG.model.cnn_dense_units,
            cnn_dropout=CONFIG.model.cnn_dropout,
            gru_units=CONFIG.model.gru_units,
            gru_dense_units=CONFIG.model.gru_dense_units,
            gru_dropout=CONFIG.model.gru_dropout,
            cae_filters=CONFIG.model.cae_filters,
            cae_kernel_size=CONFIG.model.cae_kernel_size,
            cae_lambda_rec=CONFIG.model.cae_lambda_rec,
            cae_lambda_reg=CONFIG.model.cae_lambda_reg,
            cae_dense_units=CONFIG.model.cae_dense_units,
            cae_dropout=CONFIG.model.cae_dropout,
            lstm_units=CONFIG.model.lstm_units,
            lstm_dense_units=CONFIG.model.lstm_dense_units,
            lstm_dropout=CONFIG.model.lstm_dropout,
            gating_units=CONFIG.model.gating_units,
            gating_dropout=CONFIG.model.gating_dropout,
            gating_temperature_init=CONFIG.model.gating_temperature_init,
            alf_units=CONFIG.model.alf_units,
            alf_dropout=CONFIG.model.alf_dropout,
        )

        model_dir = self.artifacts_dir / "model"
        target_w = Path(weights_path) if weights_path else None
        if target_w is None or not target_w.exists():
            candidates = list(model_dir.glob("*.weights.h5")) or list(self.artifacts_dir.glob("*.weights.h5"))
            if candidates:
                target_w = candidates[0]

        if target_w is None or not target_w.exists():
            raise FileNotFoundError(f"Arquivo de pesos não encontrado em {model_dir}")

        self.model_wrapper.load_weights(str(target_w))
        self.weights_path = target_w

        if self.auditor:
            self.auditor.log_pipeline_init(
                artifacts_dir=self.artifacts_dir,
                dataset_name=self.dataset_name,
                classes=self.classes,
                feature_names=self.feature_names,
                weights_path=self.weights_path,
            )

    def _find_latest_artifacts(self, dataset_name: str) -> Path:
        target_dir = CONFIG.artifacts_dir / dataset_name
        if not target_dir.exists():
            candidates = list(CONFIG.artifacts_dir.glob(f"**/*{dataset_name}*"))
            if not candidates:
                raise FileNotFoundError(f"Diretório de artefatos não localizado em: {CONFIG.artifacts_dir}")
            target_dir = candidates[0]
        subdirs = [p for p in target_dir.iterdir() if p.is_dir() and not p.name.startswith(".")]
        if not subdirs:
            return target_dir
        subdirs.sort(key=lambda p: p.name, reverse=True)
        return subdirs[0]

    def predict_flow(
        self,
        raw_flow: Union[Dict[str, Any], pd.DataFrame, pd.Series, Any],
        override_metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Classifica um único fluxo e aplica mitigação ativa caso seja malicioso."""
        t0 = time.perf_counter()
        meta = _extract_flow_metadata(raw_flow, override_metadata=override_metadata)

        # Pré-processamento
        X = self.preprocessor.transform_features(raw_flow)  # Shape: (1, 76)

        # Inferência
        preds = self.model_wrapper.predict(X, batch_size=1)
        latency_ms = (time.perf_counter() - t0) * 1000.0

        alf_probs = preds["ALF"][0]
        pred_idx = int(np.argmax(alf_probs))
        pred_class = self.classes[pred_idx]
        confidence = float(alf_probs[pred_idx])
        is_threat = ("benign" not in pred_class.lower()) and (confidence >= self.threat_threshold)

        # Atenção da Gating Network
        expert_names = ["DNN", "CNN", "GRU", "CAE", "LSTM"]
        gn_weights = {name: float(w) for name, w in zip(expert_names, preds["GN"][0])}

        # Predições de cada especialista
        experts_preds = {}
        for m in expert_names:
            e_idx = int(np.argmax(preds[m][0]))
            experts_preds[m] = self.classes[e_idx]

        action_taken = "LOG"
        if is_threat and self.active_defense:
            target_ip = self.active_defense.select_target(meta.get("src_ip"), meta.get("dst_ip"))
            if target_ip:
                # ------------------------------------------------------------------------------------------------------
                blocked = self.active_defense.block_ip(target_ip, attack_type=pred_class, confidence=confidence)
                # ------------------------------------------------------------------------------------------------------
                action_taken = f"BLOCKED:{target_ip}" if blocked else "ALREADY_BLOCKED"
            else:
                action_taken = "HOST_PROTECTED"

        if self.auditor:
            self.auditor.log_flow_prediction(
                meta=meta,
                pred_class=pred_class,
                confidence=confidence,
                is_threat=is_threat,
                gn_weights=gn_weights,
                experts_preds=experts_preds,
                inference_latency_ms=latency_ms,
                action_taken=action_taken,
            )

        return {
            "predicted_class": pred_class,
            "confidence": confidence,
            "is_threat": is_threat,
            "action_taken": action_taken,
            "latency_ms": latency_ms,
            "attention_weights": gn_weights,
            "expert_predictions": experts_preds,
            "metadata": meta,
        }

    def predict_batch(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Classifica um lote de fluxos a partir de um DataFrame."""
        results = []
        for i in range(len(df)):
            row = df.iloc[i]
            res = self.predict_flow(row)
            results.append(res)
        return results

    def stream_capture(self, interface: str, max_flows: Optional[int] = None) -> None:
        """Captura pacotes e classifica fluxos em tempo real via NFStream."""
        from nfstream import NFStreamer
        from plugins.extractor import FeatureExtractor, convert_into_features

        print(f"\n[InferencePipeline] Iniciando escuta em tempo real na interface '{interface}'...")
        # O FeatureExtractor atua exclusivamente na extração das métricas canônicas brutas no worker do NFStream.
        # A inferência do modelo neural é executada no processo principal para evitar erros fatais
        # de contexto CUDA decorrentes do multiprocessing fork do NFStream (CUDA_ERROR_NOT_INITIALIZED).
        extractor = FeatureExtractor(pattern=self.pattern)
        streamer = NFStreamer(
            source=interface,
            decode_tunnels=False,
            promiscuous_mode=True,
            statistical_analysis=True,
            udps=[extractor],
            n_meters=1,
            idle_timeout=120,
            active_timeout=240,
            performance_report=10
        )

        flow_count = 0
        try:
            for flow in streamer:
                arrival_ms = getattr(flow, "bidirectional_first_seen_ms", None)
                arrival_time = datetime.fromtimestamp(arrival_ms / 1000) if arrival_ms else datetime.now()

                meta = {
                    "flow_id": flow_count,
                    "src_ip": getattr(flow, "src_ip", None),
                    "src_port": getattr(flow, "src_port", None),
                    "dst_ip": getattr(flow, "dst_ip", None),
                    "dst_port": getattr(flow, "dst_port", None),
                    "protocol": getattr(flow, "protocol", None),
                    "timestamp": str(arrival_time),
                }

                flow_df = convert_into_features(flow, pattern=self.pattern)
                res = self.predict_flow(flow_df, override_metadata=meta)

                pred_class = res["predicted_class"]
                confidence = res["confidence"]
                is_threat = res["is_threat"]
                action_taken = res["action_taken"]
                latency_ms = res["latency_ms"]
                latency_until_inf = (datetime.now() - arrival_time).total_seconds() * 1000.0

                flow_count += 1
                status_icon = "🚨" if is_threat else "🟢"
                print(
                    f"{status_icon} [{flow_count}] {meta['src_ip']}:{meta['src_port']} -> {meta['dst_ip']}:{meta['dst_port']} | "
                    f"{pred_class} ({confidence*100:.1f}%) | inferência: {latency_ms:.2f}ms | e2e: {latency_until_inf/1000.0:.2f}s | ação: {action_taken}"
                )
                if max_flows and flow_count >= max_flows:
                    break
        except KeyboardInterrupt:
            if self.auditor:
                self.auditor.log_error("USER STOPPED THE CAPTURING")


    def close(self) -> None:
        if self.active_defense:
            self.active_defense.close()


# =============================================================================
# CLI EXECUTÁVEL
# =============================================================================
def run_demo(pipeline: InferencePipeline) -> None:
    """Executa demonstração rápida com fluxos sintéticos benéficos e maliciosos."""
    print("\n" + "=" * 70)
    print("        DEMO DE INFERÊNCIA E DEFESA ATIVA ALF-MoE")
    print("=" * 70)

    # 1. Fluxo Benigno
    benign_flow = {f: 10.0 for f in pipeline.feature_names}
    meta_benign = {"src_ip": "192.168.1.50", "src_port": 54321, "dst_ip": "192.168.1.1", "dst_port": 443}
    res_b = pipeline.predict_flow(benign_flow, override_metadata=meta_benign)
    print(f"Fluxo Benigno:    Predição={res_b['predicted_class']} | Confiança={res_b['confidence']*100:.1f}% | Ação={res_b['action_taken']}")

    # 2. Fluxo Malicioso Hostil (Simulado)
    attack_flow = {f: 100000.0 if "IAT" in f or "Packet" in f else 500.0 for f in pipeline.feature_names}
    meta_attack = {"src_ip": "203.0.113.199", "src_port": 6666, "dst_ip": "192.168.1.50", "dst_port": 80}
    res_a = pipeline.predict_flow(attack_flow, override_metadata=meta_attack)
    print(f"Fluxo Hostil:     Predição={res_a['predicted_class']} | Confiança={res_a['confidence']*100:.1f}% | Ação={res_a['action_taken']}")

    print("\nPesos de Atenção Gating:")
    for expert, w in res_a["attention_weights"].items():
        print(f"  {expert:<8}: {w:.4f}")
    print("=" * 70 + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Pipeline de inferência de produção ALF-MoE")
    parser.add_argument("--interface", type=str, default=None, help="Interface de rede para escuta NFStream em tempo real")
    parser.add_argument("--csv", type=str, default=None, help="Caminho de arquivo CSV para inferência em lote")
    parser.add_argument("--demo", action="store_true", help="Executa demonstração sintética do pipeline e auditoria")
    parser.add_argument("--artifacts-dir", type=str, default=None, help="Diretório de artefatos de treinamento")
    parser.add_argument("--threshold", type=float, default=CONFIG.inference.threat_threshold, help="Limiar de confiança para alerta e bloqueio")

    args = parser.parse_args()

    pipeline = InferencePipeline(
        artifacts_dir=args.artifacts_dir,
        threat_threshold=args.threshold,
        enable_active_defense=True,
        enable_audit=True,
    )

    if args.demo or (args.interface is None and args.csv is None):
        run_demo(pipeline)
    elif args.interface:
        pipeline.stream_capture(interface=args.interface)
    elif args.csv:
        print(f"Processando lote do CSV: {args.csv}...")
        df = pd.read_csv(args.csv)
        results = pipeline.predict_batch(df)
        print(f"Concluída inferência de {len(results)} registros.")


if __name__ == "__main__":
    main()
