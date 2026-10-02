"""
Pipeline de Inferência em Produção, Auditoria SIEM e Defesa Ativa para ALF-MoE.

Recursos Integrados:
1. ModelInferenceEngine: Motor de inferência otimizado para consumo mínimo de VRAM (teto 512MB ou 0MB em CPU).
2. InferenceBatchPool: Pool de micro-batching dinâmico (lotes de até 128 itens, timeout de 10ms) para expiração de pacotes/fluxos.
3. InferencePipeline: Classificação de fluxos de rede em tempo real (NFStream) ou em lotes tabulares (CSV/DataFrame).
4. InferenceAuditor: Trilha de auditoria forense estruturada em JSONL (padrão SIEM) e log rotativo.
5. ActiveDefenseAgent: Agente NIPS de bloqueio automático no firewall nftables (5 min) com proteção anti-auto-bloqueio.
"""

import os
import sys
import time
import json
import queue
import socket
import logging
import argparse
import ipaddress
import threading
import subprocess
import atexit
import pickle
import concurrent.futures
from dataclasses import dataclass, field
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Tuple, Any, Optional, Union, Callable, Literal

# Configurações de ambiente para estabilidade de drivers e bibliotecas
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")
os.environ.setdefault("TF_ENABLE_ONEDNN_OPTS", "0")
os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "max_split_size_mb:128")

import numpy as np
import pandas as pd
import tensorflow as tf
import keras

from config import CONFIG
from domain_features import CICDomainFeatures
from preprocessing import Preprocessor
from neural.model import ALFMoEModel


# =============================================================================
# 0. CONFIGURAÇÃO DE HARDWARE E VRAM
# =============================================================================
def configure_hardware(device: str = "gpu", vram_limit_mb: Optional[int] = 512) -> str:
    """
    Configura o runtime TensorFlow/Keras para controle estrito de memória de vídeo.
    - Se device == 'cpu': força CPU ocultando GPUs físicas (0 MB de VRAM).
    - Se device == 'gpu': configura teto virtual rígido em MB ou ativa memory growth dinâmico.
    """
    dev = str(device).strip().lower()
    if dev == "cpu":
        try:
            tf.config.set_visible_devices([], "GPU")
        except RuntimeError:
            pass
        return "cpu"

    gpus = tf.config.list_physical_devices("GPU")
    if not gpus:
        return "cpu"

    try:
        if vram_limit_mb is not None and vram_limit_mb > 0:
            tf.config.set_logical_device_configuration(
                gpus[0],
                [tf.config.LogicalDeviceConfiguration(memory_limit=int(vram_limit_mb))]
            )
        else:
            tf.config.experimental.set_memory_growth(gpus[0], True)
        return "gpu"
    except RuntimeError:
        # Contexto já inicializado previamente
        try:
            for g in gpus:
                tf.config.experimental.set_memory_growth(g, True)
        except RuntimeError:
            pass
        return "gpu"


# =============================================================================
# 1. UTILITÁRIOS DE AUDITORIA E SERIALIZAÇÃO JSON
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
# 2. SUBSISTEMA DE AUDITORIA SIEM JSONL
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
            print(f"[InferenceAuditor] Aviso: Diretório '{target_log_dir}' inacessível ({exc}). Fallback: '{self.log_dir}'")

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
# 3. DEFESA ATIVA (NIPS) E ANTI-AUTO-BLOQUEIO
# =============================================================================
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

    # IP da máquina atacante em ambientes de teste
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
        responder_port: Optional[int] = None,
        auditor: Optional[InferenceAuditor] = None,
        custom_whitelist: Optional[Union[List[str], Set[str], str]] = None,
        **kwargs: Any,
    ) -> None:
        self.table_name = table_name
        self.set_name = set_name
        self.block_duration_sec = block_duration_sec
        self.response_text = response_text
        self.auditor = auditor

        self.lock = threading.Lock()
        self.active_blocks: Dict[str, Dict[str, Any]] = {}
        self.local_ips = get_host_local_ips()
        self.whitelist = set(self.BASE_WHITELIST) | self.local_ips

        if custom_whitelist:
            if isinstance(custom_whitelist, (list, set)):
                self.whitelist.update(str(x).strip() for x in custom_whitelist)
            elif isinstance(custom_whitelist, str):
                self.whitelist.update(x.strip() for x in custom_whitelist.split(","))

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
                    "{", "type", "ipv4_addr;", "flags", "timeout;", "timeout", f"{self.block_duration_sec}s;", "}"
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
                details=f"Ameaça {attack_type} (confiança: {confidence*100:.1f}%) | Descarte silencioso (drop)",
            )
        print(f"\n🚨 [DEFESA ATIVA] IP BLOQUEADO: {ip} | Ameaça: {attack_type} | Duração: {self.block_duration_sec}s | Regra: nftables drop")
        return True

    def close(self) -> None:
        """Limpa tabelas do firewall se aplicável."""
        if self.is_root:
            try:
                subprocess.run(["nft", "delete", "table", "inet", self.table_name], capture_output=True)
            except Exception:
                pass


# =============================================================================
# 4. CLASSE DE GERENCIAMENTO DO MODELO E PRÉ-PROCESSAMENTO
# =============================================================================
class ModelInferenceEngine:
    """
    Mecanismo de inferência encapsulado para o modelo ALF-MoE.
    Otimizado para consumo mínimo de VRAM (teto virtual de 512MB ou fallback CPU com 0 MB).
    """

    def __init__(
        self,
        base_dir: Optional[Union[str, Path]] = None,
        model_filename: Optional[str] = None,
        artifacts_filename: Optional[str] = None,
        device: str = "gpu",
        vram_limit_mb: Optional[int] = 512,
    ):
        self.device = str(device).lower()
        self.vram_limit_mb = vram_limit_mb

        # 1. Configurar limites de memória de vídeo
        self.device = configure_hardware(self.device, self.vram_limit_mb)

        # 2. Localização dos arquivos
        self.base_dir = Path(base_dir) if base_dir else self._find_default_base_dir()
        self.artifacts_path = self._resolve_artifacts_path(artifacts_filename)
        self.model_path = self._resolve_model_path(model_filename)

        # 3. Carregar artefatos de pré-processamento
        self._load_artifacts()

        # 4. Carregar modelo Keras (com compile=False para economizar VRAM)
        self._load_model()

    def _find_default_base_dir(self) -> Path:
        dataset_name = CONFIG.preprocessing.dataset_name
        target_dir = CONFIG.artifacts_dir / dataset_name
        if target_dir.exists():
            subdirs = [p for p in target_dir.iterdir() if p.is_dir() and not p.name.startswith(".")]
            if subdirs:
                subdirs.sort(key=lambda p: p.name, reverse=True)
                return subdirs[0]
            return target_dir
        return Path(__file__).resolve().parent

    def _resolve_artifacts_path(self, artifacts_filename: Optional[str]) -> Path:
        if artifacts_filename:
            p = Path(artifacts_filename)
            if p.is_absolute() and p.exists():
                return p
            cand = self.base_dir / artifacts_filename
            if cand.exists():
                return cand
            cand_prep = self.base_dir / "preprocess" / artifacts_filename
            if cand_prep.exists():
                return cand_prep

        # Busca automática do pickle de artefatos
        prep_dir = self.base_dir / "preprocess"
        candidates = (
            list(prep_dir.glob("*_artifacts.pkl"))
            + list(self.base_dir.glob("*_artifacts.pkl"))
            + list(self.base_dir.glob("**/*_artifacts.pkl"))
            + list(CONFIG.artifacts_dir.glob("**/*_artifacts.pkl"))
        )
        if candidates:
            return candidates[0]
        raise FileNotFoundError(f"Arquivo de artefatos não localizado em: {self.base_dir}")

    def _resolve_model_path(self, model_filename: Optional[str]) -> Path:
        if model_filename:
            p = Path(model_filename)
            if p.is_absolute() and p.exists():
                return p
            cand = self.base_dir / model_filename
            if cand.exists():
                return cand
            cand_m = self.base_dir / "model" / model_filename
            if cand_m.exists():
                return cand_m

        # Prioridade para pesos (.weights.h5) para reconstrução funcional estável no Keras 3
        model_dir = self.base_dir / "model"
        weights_cands = (
            list(model_dir.glob("*.weights.h5"))
            + list(self.base_dir.glob("*.weights.h5"))
            + list(self.base_dir.glob("**/*.weights.h5"))
        )
        if weights_cands:
            return weights_cands[0]

        # Alternativa para model.keras / alf_moe.keras
        keras_cands = (
            list(model_dir.glob("*.keras"))
            + list(self.base_dir.glob("*.keras"))
            + list(self.base_dir.glob("**/*.keras"))
        )
        if keras_cands:
            return keras_cands[0]

        raise FileNotFoundError(f"Modelo ou pesos não encontrados em: {self.base_dir}")

    def _load_artifacts(self) -> None:
        if not self.artifacts_path.exists():
            raise FileNotFoundError(f"Arquivo de artefatos não encontrado: {self.artifacts_path}")

        with open(self.artifacts_path, "rb") as f:
            artifacts = pickle.load(f)

        self.scaler = artifacts["scaler"]
        self.label_encoder = artifacts["label_encoder"]
        self.feature_names = artifacts["feature_names"]
        self.log1p_features = set(artifacts.get("log1p_features", []))
        self.feature_medians = artifacts.get("feature_medians", {})
        self.domain_indices = artifacts.get("domain_indices", None)
        self.classes = list(self.label_encoder.classes_)

        # Mapeamento rápido de índices para transformação log1p
        self.log1p_indices = [
            i for i, feat in enumerate(self.feature_names) if feat in self.log1p_features
        ]

        # Normalizador de chaves para mapeamento rápido de features
        self.clean_feature_map = {
            self._clean_key(name): i for i, name in enumerate(self.feature_names)
        }

        # Vetor padrão com medianas para imputação ultrarrápida
        self.default_vector = np.array(
            [self.feature_medians.get(f, 0.0) for f in self.feature_names],
            dtype=np.float32,
        )

    @staticmethod
    def _clean_key(key: str) -> str:
        """Normaliza chaves de dicionário (minúsculas, sem espaços ou sublinhados)."""
        return str(key).strip().lower().replace(" ", "").replace("_", "").replace("-", "")

    def _load_model(self) -> None:
        """
        Carrega modelo com compile=False para evitar alocação de buffers do Adam na VRAM.
        Suporta tanto arquivos de pesos .weights.h5 (via ALFMoEModel) quanto .keras salvos.
        """
        is_weights = str(self.model_path).endswith(".weights.h5") or str(self.model_path).endswith(".h5")
        
        if is_weights:
            # Reconstrução funcional do ALF-MoE garantindo todas as subcamadas do CAE construídas
            domain_idx = self.domain_indices
            if domain_idx is None:
                prep = Preprocessor(auto_load=False)
                domain_idx = prep.get_domain_indices()

            self.model_wrapper = ALFMoEModel(
                feature_names=self.feature_names,
                classes=self.classes,
                domain_indices=domain_idx,
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
            self.model_wrapper.load_weights(str(self.model_path))
            self.model = self.model_wrapper.model
        else:
            try:
                # compile=False evita alocar memória para os pesos de otimizador (Adam)
                self.model = keras.models.load_model(str(self.model_path), compile=False)
                self.model_wrapper = None
            except Exception:
                # Fallback de reconstrução caso load_model falhe por subcamadas não construídas
                domain_idx = self.domain_indices or Preprocessor(auto_load=False).get_domain_indices()
                self.model_wrapper = ALFMoEModel(
                    feature_names=self.feature_names,
                    classes=self.classes,
                    domain_indices=domain_idx,
                )
                cand_w = list(self.model_path.parent.glob("*.weights.h5"))
                if cand_w:
                    self.model_wrapper.load_weights(str(cand_w[0]))
                self.model = self.model_wrapper.model

    def preprocess(
        self,
        features: Union[Dict[str, Any], List[Dict[str, Any]], pd.DataFrame, pd.Series, np.ndarray],
        n_items: Optional[int] = None,
    ) -> np.ndarray:
        """
        Converte as features de entrada em uma matriz numpy normalizada (n_items, 73).
        Suporta dicionários com listas/escalares, listas de dicionários, DataFrames e matrizes.
        """
        if isinstance(features, np.ndarray):
            if features.shape[-1] == len(self.feature_names):
                return features.astype(np.float32, copy=False)
            raise ValueError(f"Shape inválido para matriz numpy: {features.shape}, esperado (N, {len(self.feature_names)})")

        if isinstance(features, pd.DataFrame):
            n = len(features) if n_items is None else min(len(features), n_items)
            data = np.tile(self.default_vector, (n, 1))
            col_map = {self._clean_key(c): c for c in features.columns}
            for clean_k, col_idx in self.clean_feature_map.items():
                if clean_k in col_map:
                    data[:, col_idx] = features[col_map[clean_k]].values[:n]
        elif isinstance(features, list):
            # Lista de dicionários (cenário da pool de inferência em micro-lotes)
            n = len(features) if n_items is None else min(len(features), n_items)
            data = np.tile(self.default_vector, (n, 1))
            for row_idx, item_dict in enumerate(features[:n]):
                if isinstance(item_dict, dict):
                    for k, v in item_dict.items():
                        ck = self._clean_key(k)
                        if ck in self.clean_feature_map:
                            try:
                                data[row_idx, self.clean_feature_map[ck]] = float(v)
                            except (ValueError, TypeError):
                                pass
        elif isinstance(features, pd.Series):
            n = 1
            data = np.tile(self.default_vector, (1, 1))
            row_dict = features.to_dict()
            for k, v in row_dict.items():
                ck = self._clean_key(k)
                if ck in self.clean_feature_map:
                    try:
                        data[0, self.clean_feature_map[ck]] = float(v)
                    except (ValueError, TypeError):
                        pass
        elif isinstance(features, dict):
            # Dicionário com escalares ou listas
            if n_items is None:
                # Descobre n_items pelas listas presentes
                n = 1
                for v in features.values():
                    if isinstance(v, (list, tuple, np.ndarray)):
                        n = max(n, len(v))
            else:
                n = n_items

            data = np.tile(self.default_vector, (n, 1))
            input_cleaned = {self._clean_key(k): v for k, v in features.items()}

            for clean_k, col_idx in self.clean_feature_map.items():
                if clean_k in input_cleaned:
                    val = input_cleaned[clean_k]
                    if isinstance(val, (list, tuple, np.ndarray)):
                        val_arr = np.asarray(val, dtype=np.float32)
                        cnt = len(val_arr)
                        if cnt >= n:
                            data[:, col_idx] = val_arr[:n]
                        elif cnt > 0:
                            repeated = np.pad(val_arr, (0, max(0, n - cnt)), mode="edge")
                            data[:, col_idx] = repeated[:n]
                    else:
                        try:
                            data[:, col_idx] = float(val)
                        except (ValueError, TypeError):
                            pass
        else:
            raise TypeError(f"Tipo de features não suportado: {type(features)}")

        # Aplica transformação log1p
        if self.log1p_indices:
            data[:, self.log1p_indices] = np.log1p(
                np.maximum(data[:, self.log1p_indices], 0.0)
            )

        # RobustScaler treinado
        scaled_data = self.scaler.transform(data)
        return scaled_data.astype(np.float32, copy=False)

    def infer(
        self,
        features: Union[Dict[str, Any], List[Dict[str, Any]], pd.DataFrame, pd.Series, np.ndarray],
        n_items: Optional[int] = None,
        batch_size: int = 128,
        return_details: bool = False,
    ) -> Dict[str, Any]:
        """
        Executa a inferência direta no grafo Keras em lotes para manter pegada mínima de VRAM.
        """
        X = self.preprocess(features, n_items=n_items)
        total_items = len(X)
        if total_items == 0:
            return {
                "predictions": [],
                "class_indices": [],
                "confidences": [],
                "probabilities": np.empty((0, len(self.classes))),
                "classes": self.classes,
                "n_items": 0,
            }

        alf_probs_list = []
        gn_weights_list = []

        total_batches = int(np.ceil(total_items / batch_size))
        for b in range(total_batches):
            batch_x = X[b * batch_size : (b + 1) * batch_size]
            outputs = self.model(batch_x, training=False)

            # Saídas: ['DNN', 'CNN', 'GRU', 'CAE', 'LSTM', 'GN', 'ALF']
            if isinstance(outputs, (list, tuple)):
                gn_out = outputs[5].numpy() if len(outputs) > 5 else None
                alf_out = outputs[-1].numpy()
            else:
                gn_out = None
                alf_out = outputs.numpy()

            alf_probs_list.append(alf_out)
            if gn_out is not None:
                gn_weights_list.append(gn_out)

        probs = np.vstack(alf_probs_list)
        class_indices = np.argmax(probs, axis=1)
        predictions = [self.classes[idx] for idx in class_indices]
        confidences = np.max(probs, axis=1).tolist()

        result = {
            "predictions": predictions,
            "class_indices": class_indices.tolist(),
            "confidences": confidences,
            "probabilities": probs,
            "classes": self.classes,
            "n_items": total_items,
        }

        if return_details and gn_weights_list:
            result["expert_weights"] = np.vstack(gn_weights_list)

        return result


# =============================================================================
# 5. SINGLETON E FUNÇÕES PÚBLICAS DE INFERÊNCIA
# =============================================================================
_ENGINE_INSTANCE: Optional[ModelInferenceEngine] = None
_ENGINE_LOCK = threading.Lock()


def get_inference_engine(
    device: str = "gpu",
    vram_limit_mb: Optional[int] = 512,
    base_dir: Optional[Union[str, Path]] = None,
) -> ModelInferenceEngine:
    """Retorna a instância singleton do motor de inferência, evitando re-carregar o modelo na VRAM."""
    global _ENGINE_INSTANCE
    with _ENGINE_LOCK:
        if _ENGINE_INSTANCE is None:
            _ENGINE_INSTANCE = ModelInferenceEngine(
                base_dir=base_dir,
                device=device,
                vram_limit_mb=vram_limit_mb,
            )
        return _ENGINE_INSTANCE


def infer(
    features: Union[Dict[str, Any], List[Dict[str, Any]], pd.DataFrame, pd.Series, np.ndarray],
    n_items: Optional[int] = None,
    device: str = "gpu",
    vram_limit_mb: Optional[int] = 512,
    return_details: bool = False,
) -> Dict[str, Any]:
    """
    Função pública principal de inferência.
    """
    engine = get_inference_engine(device=device, vram_limit_mb=vram_limit_mb)
    return engine.infer(features=features, n_items=n_items, return_details=return_details)


# Alias de conveniência
predict = infer


# =============================================================================
# 6. POOL DE INFERÊNCIA DINÂMICA (MICRO-BATCHING EM TEMPO REAL)
# =============================================================================
@dataclass
class _BatchPoolRequest:
    features: Union[Dict[str, Any], pd.Series, Any]
    metadata: Dict[str, Any]
    arrival_time: datetime
    arrival_time_ms: float
    future: concurrent.futures.Future
    callback: Optional[Callable[[Dict[str, Any]], None]] = None


class InferenceBatchPool:
    """
    Pool de inferência com micro-batching dinâmico para fluxos/pacotes expirados.

    Acumula requisições concorrentes e dispara a execução em lote na GPU/CPU assim que:
    1. Atinge max_batch_size (padrão: 128 itens, obtendo 75ms por lote completo)
    OU
    2. O timeout de espera máxima (max_wait_ms: 10.0 ms) expira.

    Elimina o gargalo do processamento unitário (1 item = 100ms) e impede o aumento
    da latência de ponta a ponta (e2e) em períodos de tráfego intenso.
    """

    def __init__(
        self,
        engine: ModelInferenceEngine,
        max_batch_size: int = 128,
        max_wait_ms: float = 10.0,
        threat_threshold: float = 0.70,
        active_defense: Optional[ActiveDefenseAgent] = None,
        auditor: Optional[InferenceAuditor] = None,
        name: str = "ALF-InferenceBatchPool",
    ) -> None:
        self.engine = engine
        self.max_batch_size = int(max_batch_size)
        self.max_wait_ms = float(max_wait_ms)
        self.threat_threshold = float(threat_threshold)
        self.active_defense = active_defense
        self.auditor = auditor
        self.name = name

        self._queue: queue.Queue[Optional[_BatchPoolRequest]] = queue.Queue(maxsize=50000)
        self._running = False
        self._worker_thread: Optional[threading.Thread] = None

        self.total_processed = 0
        self.total_batches = 0

    def start(self) -> None:
        """Inicia a thread de despacho de inferência da pool."""
        if self._running:
            return
        self._running = True
        self._worker_thread = threading.Thread(
            target=self._worker_loop,
            name=f"{self.name}-Worker",
            daemon=True,
        )
        self._worker_thread.start()

    def submit(
        self,
        features: Union[Dict[str, Any], pd.Series, Any],
        metadata: Optional[Dict[str, Any]] = None,
        arrival_time: Optional[datetime] = None,
        arrival_time_ms: Optional[float] = None,
        callback: Optional[Callable[[Dict[str, Any]], None]] = None,
    ) -> concurrent.futures.Future:
        """
        Submete um fluxo expirado para a pool de inferência sem bloquear o sniffer de rede.
        Retorna um Future que será resolvido assim que o micro-lote for processado.
        """
        if not self._running:
            self.start()

        arr_dt = arrival_time or datetime.now()
        arr_ms = arrival_time_ms if arrival_time_ms is not None else (time.time() * 1000.0)
        meta = metadata or {}

        fut = concurrent.futures.Future()
        req = _BatchPoolRequest(
            features=features,
            metadata=meta,
            arrival_time=arr_dt,
            arrival_time_ms=arr_ms,
            future=fut,
            callback=callback,
        )

        try:
            self._queue.put_nowait(req)
        except queue.Full:
            # Em caso de saturação extrema da fila, descarta o fluxo mais antigo ou força inserção
            self._queue.put(req, block=True, timeout=0.05)

        return fut

    def _worker_loop(self) -> None:
        """Loop contínuo de coleta em micro-batch e execução na GPU."""
        while self._running:
            try:
                first_req = self._queue.get(timeout=0.1)
            except queue.Empty:
                continue

            if first_req is None:
                # Sinal de encerramento
                break

            batch: List[_BatchPoolRequest] = [first_req]
            t_batch_start = time.perf_counter()
            deadline = t_batch_start + (self.max_wait_ms / 1000.0)

            # Acumula até atingir max_batch_size (128) ou timeout de 10ms
            while len(batch) < self.max_batch_size:
                remaining_time = deadline - time.perf_counter()
                if remaining_time <= 0:
                    break
                try:
                    nxt = self._queue.get(timeout=remaining_time)
                    if nxt is None:
                        self._running = False
                        break
                    batch.append(nxt)
                except queue.Empty:
                    break

            # Execução vetorizada do lote agrupado
            self._process_batch(batch)

    def _process_batch(self, batch: List[_BatchPoolRequest]) -> None:
        if not batch:
            return

        batch_count = len(batch)
        features_list = [
            req.features.to_dict() if isinstance(req.features, pd.Series) else (
                req.features.iloc[0].to_dict() if isinstance(req.features, pd.DataFrame) else req.features
            )
            for req in batch
        ]

        t0 = time.perf_counter()
        inf_result = self.engine.infer(
            features=features_list,
            n_items=batch_count,
            batch_size=self.max_batch_size,
            return_details=True,
        )
        batch_latency_ms = (time.perf_counter() - t0) * 1000.0
        avg_item_latency_ms = batch_latency_ms / batch_count if batch_count > 0 else 0.0

        expert_names = ["DNN", "CNN", "GRU", "CAE", "LSTM"]
        now_ms = time.time() * 1000.0

        for idx, req in enumerate(batch):
            pred_class = inf_result["predictions"][idx]
            confidence = float(inf_result["confidences"][idx])
            is_threat = ("benign" not in pred_class.lower()) and (confidence >= self.threat_threshold)

            gn_weights = {}
            if "expert_weights" in inf_result and inf_result["expert_weights"] is not None:
                gn_weights = {
                    name: float(inf_result["expert_weights"][idx][i])
                    for i, name in enumerate(expert_names)
                    if i < inf_result["expert_weights"].shape[1]
                }

            latency_until_inf = max(0.0, now_ms - req.arrival_time_ms)

            # Defesa Ativa via nftables
            action_taken = "LOG"
            if is_threat and self.active_defense:
                target_ip = self.active_defense.select_target(req.metadata.get("src_ip"), req.metadata.get("dst_ip"))
                if target_ip:
                    blocked = self.active_defense.block_ip(target_ip, attack_type=pred_class, confidence=confidence)
                    action_taken = f"BLOCKED:{target_ip}" if blocked else "ALREADY_BLOCKED"
                else:
                    action_taken = "HOST_PROTECTED"

            # Trilha Forense SIEM JSONL
            if self.auditor:
                self.auditor.log_flow_prediction(
                    meta=req.metadata,
                    pred_class=pred_class,
                    confidence=confidence,
                    is_threat=is_threat,
                    gn_weights=gn_weights,
                    experts_preds={},
                    inference_latency_ms=avg_item_latency_ms,
                    action_taken=action_taken,
                )

            res_dict = {
                "predicted_class": pred_class,
                "confidence": confidence,
                "is_threat": is_threat,
                "action_taken": action_taken,
                "latency_ms": avg_item_latency_ms,
                "batch_latency_ms": batch_latency_ms,
                "batch_size": batch_count,
                "e2e_latency_ms": latency_until_inf,
                "attention_weights": gn_weights,
                "metadata": req.metadata,
                "flow_id": req.metadata.get("flow_id"),
            }

            # Resolve o Future e aciona callback opcional
            if not req.future.done():
                req.future.set_result(res_dict)

            if req.callback:
                try:
                    req.callback(res_dict)
                except Exception as exc:
                    if self.auditor:
                        self.auditor.log_error(f"Erro no callback do fluxo {req.metadata.get('flow_id')}: {exc}")

        self.total_processed += batch_count
        self.total_batches += 1

    def flush(self, timeout: float = 5.0) -> None:
        """Aguarda o processamento de todos os itens atualmente enfileirados."""
        t_end = time.time() + timeout
        while not self._queue.empty() and time.time() < t_end:
            time.sleep(0.01)

    def stop(self) -> None:
        """Finaliza a thread de execução da pool."""
        self._running = False
        try:
            self._queue.put_nowait(None)
        except Exception:
            pass
        if self._worker_thread and self._worker_thread.is_alive():
            self._worker_thread.join(timeout=2.0)


# =============================================================================
# 7. PIPELINE UNIFICADO DE INFERÊNCIA
# =============================================================================
class InferencePipeline:
    """
    Pipeline unificado de inferência para produção.
    Conecta fluxos de rede brutos, pré-processamento, motor otimizado ALF-MoE, pool assíncrona, auditoria e defesa ativa.
    """

    def __init__(
        self,
        artifacts_dir: Optional[Union[str, Path]] = None,
        weights_path: Optional[Union[str, Path]] = None,
        dataset_name: str = CONFIG.preprocessing.dataset_name,
        threat_threshold: float = CONFIG.inference.threat_threshold,
        enable_active_defense: bool = CONFIG.inference.enable_active_defense,
        enable_audit: bool = CONFIG.inference.enable_audit,
        device: str = "gpu",
        vram_limit_mb: Optional[int] = 512,
        batch_size: int = 128,
        max_wait_ms: float = 10.0,
    ) -> None:
        self.dataset_name = dataset_name
        self.threat_threshold = float(threat_threshold)
        self.pattern: Literal[1, 2] = 2 if "CSE-CIC-IDS2018" in self.dataset_name else 1
        self.device = device
        self.vram_limit_mb = vram_limit_mb

        # 1. Auditoria SIEM
        self.auditor = InferenceAuditor() if enable_audit else None

        # 2. Defesa Ativa
        self.active_defense = None
        if enable_active_defense:
            self.active_defense = ActiveDefenseAgent(
                block_duration_sec=CONFIG.inference.active_defense_duration,
                response_text=CONFIG.inference.active_response_text,
                auditor=self.auditor,
                custom_whitelist=CONFIG.inference.protected_ips,
            )
            atexit.register(self.close)

        # 3. Motor de Inferência (baixo consumo de VRAM)
        self.engine = ModelInferenceEngine(
            base_dir=artifacts_dir,
            model_filename=str(weights_path) if weights_path else None,
            device=self.device,
            vram_limit_mb=self.vram_limit_mb,
        )

        self.classes = self.engine.classes
        self.feature_names = self.engine.feature_names
        self.artifacts_dir = self.engine.base_dir
        self.weights_path = self.engine.model_path

        # 4. Pool de Inferência em Lote (Micro-Batching Dinâmico)
        self.batch_pool = InferenceBatchPool(
            engine=self.engine,
            max_batch_size=batch_size,
            max_wait_ms=max_wait_ms,
            threat_threshold=self.threat_threshold,
            active_defense=self.active_defense,
            auditor=self.auditor,
        )
        self.batch_pool.start()

        if self.auditor:
            self.auditor.log_pipeline_init(
                artifacts_dir=self.artifacts_dir,
                dataset_name=self.dataset_name,
                classes=self.classes,
                feature_names=self.feature_names,
                weights_path=self.weights_path,
            )

    def predict_flow(
        self,
        raw_flow: Union[Dict[str, Any], pd.DataFrame, pd.Series, Any],
        override_metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Classifica um único fluxo e aplica mitigação ativa caso seja malicioso."""
        t0 = time.perf_counter()
        meta = _extract_flow_metadata(raw_flow, override_metadata=override_metadata)

        # Inferência direta via motor vetorizado
        res = self.engine.infer(raw_flow, n_items=1, batch_size=1, return_details=True)
        latency_ms = (time.perf_counter() - t0) * 1000.0

        pred_class = res["predictions"][0]
        confidence = float(res["confidences"][0])
        is_threat = ("benign" not in pred_class.lower()) and (confidence >= self.threat_threshold)

        expert_names = ["DNN", "CNN", "GRU", "CAE", "LSTM"]
        gn_weights = {}
        if "expert_weights" in res and res["expert_weights"] is not None:
            gn_weights = {
                name: float(res["expert_weights"][0][i])
                for i, name in enumerate(expert_names)
                if i < res["expert_weights"].shape[1]
            }

        action_taken = "LOG"
        if is_threat and self.active_defense:
            target_ip = self.active_defense.select_target(meta.get("src_ip"), meta.get("dst_ip"))
            if target_ip:
                blocked = self.active_defense.block_ip(target_ip, attack_type=pred_class, confidence=confidence)
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
                experts_preds={},
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
            "metadata": meta,
        }

    def predict_batch(self, df: pd.DataFrame, batch_size: int = 128) -> List[Dict[str, Any]]:
        """
        Classifica um lote de fluxos a partir de um DataFrame de forma vetorizada em blocos de até 128.
        """
        t0 = time.perf_counter()
        n_items = len(df)
        res = self.engine.infer(df, n_items=n_items, batch_size=batch_size, return_details=True)
        total_time_ms = (time.perf_counter() - t0) * 1000.0

        expert_names = ["DNN", "CNN", "GRU", "CAE", "LSTM"]
        results = []

        for i in range(n_items):
            pred_class = res["predictions"][i]
            confidence = float(res["confidences"][i])
            is_threat = ("benign" not in pred_class.lower()) and (confidence >= self.threat_threshold)

            gn_weights = {}
            if "expert_weights" in res and res["expert_weights"] is not None:
                gn_weights = {
                    name: float(res["expert_weights"][i][j])
                    for j, name in enumerate(expert_names)
                    if j < res["expert_weights"].shape[1]
                }

            meta = _extract_flow_metadata(df, sample_index=i)
            results.append({
                "predicted_class": pred_class,
                "confidence": confidence,
                "is_threat": is_threat,
                "attention_weights": gn_weights,
                "metadata": meta,
                "latency_ms": total_time_ms / n_items if n_items > 0 else 0.0,
            })

        return results

    def stream_capture(self, interface: str, max_flows: Optional[int] = None) -> None:
        """
        Captura pacotes e classifica fluxos em tempo real via NFStream com pool assíncrona.
        Elimina o atraso cumulativo e2e ao despachar pacotes expirados em lotes dinâmicos.
        """
        from nfstream import NFStreamer
        from plugins.extractor import FeatureExtractor, convert_into_features

        print(f"\n[InferencePipeline] Iniciando escuta em tempo real na interface '{interface}'...")
        print(f"[InferencePipeline] Hardware: {self.engine.device.upper()} | Teto VRAM: {self.engine.vram_limit_mb}MB | Batch Máx: {self.batch_pool.max_batch_size} | Timeout Micro-Batch: {self.batch_pool.max_wait_ms}ms")

        extractor = FeatureExtractor(pattern=self.pattern)
        streamer = NFStreamer(
            source=interface,
            decode_tunnels=False,
            promiscuous_mode=True,
            statistical_analysis=True,
            udps=[extractor],
            idle_timeout=120,
            active_timeout=240,
            performance_report=10,
        )

        flow_count = 0

        def _on_flow_predicted(res: Dict[str, Any]) -> None:
            meta = res["metadata"]
            status_icon = "🚨" if res["is_threat"] else "🟢"
            f_id = res.get("flow_id", "-")
            print(
                f"{status_icon} [{f_id}] {meta.get('src_ip')}:{meta.get('src_port')} -> {meta.get('dst_ip')}:{meta.get('dst_port')} | "
                f"{res['predicted_class']} ({res['confidence']*100:.1f}%) | "
                f"lote: {res.get('batch_size', 1)} | inf: {res['latency_ms']:.2f}ms | e2e: {res['e2e_latency_ms']/1000.0:.2f}s | ação: {res['action_taken']}"
            )

        try:
            for flow in streamer:
                flow_count += 1
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

                # Extrai as 76 features canônicas no padrão CIC
                flow_df = convert_into_features(flow, pattern=self.pattern)

                # Despacha para a pool de inferência de forma NÃO-BLOQUEANTE
                self.batch_pool.submit(
                    features=flow_df,
                    metadata=meta,
                    arrival_time=arrival_time,
                    arrival_time_ms=arrival_ms or (time.time() * 1000.0),
                    callback=_on_flow_predicted,
                )

                if max_flows and flow_count >= max_flows:
                    break
        except KeyboardInterrupt:
            if self.auditor:
                self.auditor.log_error("USER STOPPED THE CAPTURING")
        finally:
            print("\n[InferencePipeline] Drenando requisições pendentes na pool de inferência...")
            self.batch_pool.flush()

    def close(self) -> None:
        """Encerra pool de inferência e limpa tabelas do firewall se aplicável."""
        if hasattr(self, "batch_pool") and self.batch_pool:
            self.batch_pool.stop()
        if self.active_defense:
            self.active_defense.close()


# =============================================================================
# 8. CLI EXECUTÁVEL E DEMONSTRAÇÃO
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
    parser.add_argument("--device", type=str, default="gpu", choices=["gpu", "cpu"], help="Dispositivo para execução (gpu ou cpu)")
    parser.add_argument("--vram-limit", type=int, default=512, help="Teto virtual de VRAM em MB (default: 512)")
    parser.add_argument("--batch-size", type=int, default=128, help="Tamanho máximo de lote da pool (default: 128)")
    parser.add_argument("--max-wait-ms", type=float, default=10.0, help="Tempo máximo de espera em ms para micro-batch (default: 10.0)")

    args = parser.parse_args()

    pipeline = InferencePipeline(
        artifacts_dir=args.artifacts_dir,
        threat_threshold=args.threshold,
        enable_active_defense=True,
        enable_audit=True,
        device=args.device,
        vram_limit_mb=args.vram_limit,
        batch_size=args.batch_size,
        max_wait_ms=args.max_wait_ms,
    )

    if args.demo or (args.interface is None and args.csv is None):
        run_demo(pipeline)
    elif args.interface:
        pipeline.stream_capture(interface=args.interface)
    elif args.csv:
        print(f"Processando lote do CSV: {args.csv}...")
        df = pd.read_csv(args.csv)
        results = pipeline.predict_batch(df, batch_size=args.batch_size)
        print(f"Concluída inferência de {len(results)} registros.")


if __name__ == "__main__":
    main()
