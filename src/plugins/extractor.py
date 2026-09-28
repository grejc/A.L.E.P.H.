"""
Extrator de features de fluxo de rede baseado em NFStream.
Alinhado rigorosamente aos padrões de dados CICFlowMeter / CIC-UNSW-NB15 / CIC-BCCC-NRC-2024.

Princípio da Responsabilidade Única (SRP):
    Este módulo é responsável ESTRITAMENTE pela captura e extração das 76 features
    estatísticas canônicas brutas da rede. Nenhuma transformação de modelo de Machine Learning
    (como log1p, RobustScaler, codificação de labels ou particionamento em especialistas)
    é realizada neste arquivo.
"""

import time
from typing import Any, Dict, List, Optional, Union, Literal
import numpy as np
import pandas as pd
from nfstream import NFPlugin, NFStreamer


def encode_tcp_flags(packet: Any) -> int:
    """
    Codifica 8 flags TCP presentes em um pacote em uma máscara binária de 8 bits.

    Ordem dos bits (LSB -> MSB):
        Bit 0: SYN
        Bit 1: CWR
        Bit 2: ECE
        Bit 3: URG
        Bit 4: ACK
        Bit 5: PSH
        Bit 6: RST
        Bit 7: FIN

    Args:
        packet: Objeto NFPacket fornecido pelo NFStream contendo atributos booleanos das flags.

    Returns:
        int: Inteiro entre 0 e 255 com a codificação das flags TCP.
    """
    flags: int = 0
    flags |= (1 if getattr(packet, "syn", False) else 0) << 0
    flags |= (1 if getattr(packet, "cwr", False) else 0) << 1
    flags |= (1 if getattr(packet, "ece", False) else 0) << 2
    flags |= (1 if getattr(packet, "urg", False) else 0) << 3
    flags |= (1 if getattr(packet, "ack", False) else 0) << 4
    flags |= (1 if getattr(packet, "psh", False) else 0) << 5
    flags |= (1 if getattr(packet, "rst", False) else 0) << 6
    flags |= (1 if getattr(packet, "fin", False) else 0) << 7
    return flags


def extract_tcp_window_size(packet: Any) -> int:
    """
    Extrai o tamanho da janela TCP (16 bits) a partir dos bytes brutos do cabeçalho IP.

    Trata tanto pacotes IPv4 (calculando dinamicamente o Internet Header Length - IHL)
    quanto IPv6 padrão (verificando se o Next Header no offset 6 é TCP).

    Args:
        packet: Objeto NFPacket com atributo ip_packet (bytes brutos começando no cabeçalho IP).

    Returns:
        int: Tamanho da janela anunciado em bytes (16 bits), ou 0 se não for TCP ou inválido.
    """
    try:
        if getattr(packet, "protocol", None) != 6:
            return 0
        raw: Optional[bytes] = getattr(packet, "ip_packet", None)
        if not raw or len(raw) < 20:
            return 0

        version: int = (raw[0] >> 4) & 0x0F
        if version == 4:
            ihl: int = (raw[0] & 0x0F) * 4
            tcp_offset: int = ihl
        elif version == 6:
            # Cabeçalho IPv6 padrão: 40 bytes. Verifica se Next Header (offset 6) é TCP (6)
            if len(raw) < 40 or raw[6] != 6:
                return 0
            tcp_offset = 40
        else:
            return 0

        if len(raw) >= tcp_offset + 16:
            return int.from_bytes(raw[tcp_offset + 14 : tcp_offset + 16], byteorder="big")
    except Exception:
        pass
    return 0

class FeatureExtractor(NFPlugin):
    """
    Plugin NFStream para cômputo das estatísticas canônicas de fluxo no padrão CICFlowMeter
    e inferência neural inline via ALF-MoE ao término do fluxo (on_expire).

    Gera os atributos complementares em flow.udps necessários para totalizar as 76 features
    canônicas dos datasets CIC-UNSW-NB15 e CIC-BCCC-NRC-2024, e executa a classificação de
    ameaças no fechamento do fluxo para eliminar gargalos de inferência no loop consumidor.

    Grandezas e Unidades:
        - Duração de fluxo: Microssegundos (μs).
        - Inter-Arrival Times (IAT): Microssegundos (μs).
        - Active / Idle Times: Microssegundos (μs).
        - Tamanhos de segmentos e cabeçalhos: Bytes.
        - Taxas: Unidades por segundo (Bytes/s, Packets/s).
    """

    FLAG_NAMES: List[str] = ["syn", "cwr", "ece", "urg", "ack", "psh", "rst", "fin"]

    def __init__(
        self,
        preprocessor: Optional[Any] = None,
        model_wrapper: Optional[Any] = None,
        classes: Optional[List[str]] = None,
        threat_threshold: float = 0.70,
        pattern: Literal[1, 2] = 1,
        **kwargs: Any,
    ) -> None:
        """
        Inicializa o plugin NFStream.

        Args:
            preprocessor: Instância opcional de Preprocessor para transformação de features.
            model_wrapper: Instância opcional do ALFMoEModel ou modelo Keras para inferência.
            classes: Lista opcional de nomes de classes (rótulos).
            threat_threshold: Limiar de confiança para detecção de ameaça.
            pattern: 1 para CICFlowMeter / CIC-UNSW-NB15 / CIC-BCCC-NRC-2024, 2 para CSE-CIC-IDS2018.
        """
        super().__init__(**kwargs)
        self.preprocessor = preprocessor
        self.model_wrapper = model_wrapper
        self.classes = classes or (getattr(preprocessor, "classes", []) if preprocessor else [])
        self.threat_threshold = float(threat_threshold)
        self.pattern = pattern
        self._model = getattr(model_wrapper, "model", model_wrapper)

    def on_init(self, packet: Any, flow: Any) -> None:
        """
        Invocado na criação de um novo fluxo no NFStream (no primeiro pacote observado).

        Inicializa todas as métricas em flow.udps e computa os valores do primeiro pacote.

        Args:
            packet: Primeiro pacote associado ao fluxo.
            flow: Objeto NFlow em inicialização.
        """
        # Taxas e proporções
        flow.udps.bytes_per_second: float = 0.0
        flow.udps.packets_per_second: float = 0.0
        flow.udps.fwd_packets_per_second: float = 0.0
        flow.udps.bwd_packets_per_second: float = 0.0
        flow.udps.avg_bytes_per_packet: float = 0.0
        flow.udps.down_up_ratio: float = 0.0
        flow.udps.packet_length_variance: float = 0.0

        # Cabeçalhos e Janelas TCP (Padrão CICFlowMeter)
        flow.udps.fwd_header_length: int = 0
        flow.udps.bwd_header_length: int = 0
        flow.udps.fwd_seg_size_min: int = 0
        flow.udps.fwd_act_data_pkts: int = 0
        flow.udps.fwd_init_win_bytes: int = -1
        flow.udps.bwd_init_win_bytes: int = -1
        flow.udps.fwd_segment_size_avg: float = 0.0
        flow.udps.bwd_segment_size_avg: float = 0.0

        # Subfluxos (Subflow features)
        flow.udps.subflow_fwd_packets: int = 0
        flow.udps.subflow_fwd_bytes: int = 0
        flow.udps.subflow_bwd_packets: int = 0
        flow.udps.subflow_bwd_bytes: int = 0

        # Métricas de Bulk (padrão 0.0 no CICFlowMeter e descartadas nos modelos)
        flow.udps.fwd_bytes_bulk_avg: float = 0.0
        flow.udps.fwd_packet_bulk_avg: float = 0.0
        flow.udps.fwd_bulk_rate_avg: float = 0.0
        flow.udps.bwd_bytes_bulk_avg: float = 0.0
        flow.udps.bwd_packet_bulk_avg: float = 0.0
        flow.udps.bwd_bulk_rate_avg: float = 0.0

        # Controle de períodos Ativos e Ociosos (Active & Idle) em microssegundos (μs)
        # Limiar de ociosidade clássico: 5.000.000 μs = 5 segundos (5000 ms no delta_time)
        flow.udps.active_times: List[float] = []
        flow.udps.idle_times: List[float] = []
        flow.udps.start_active_time_ms: int = packet.time
        flow.udps.end_active_time_ms: int = packet.time
        flow.udps.active_min: float = 0.0
        flow.udps.active_mean: float = 0.0
        flow.udps.active_max: float = 0.0
        flow.udps.active_std: float = 0.0
        flow.udps.idle_min: float = 0.0
        flow.udps.idle_mean: float = 0.0
        flow.udps.idle_max: float = 0.0
        flow.udps.idle_std: float = 0.0

        flow.udps.PREDICTION = {
            "LABEL": "",
            "confidence": 0,
            "is_threat": -1,
            "gating_attention_weights": {
                "DNN": 0,
                "CNN": 0,
                "GRU": 0,
                "CAE": 0,
                "LSTM": 0,
            },
            "experts_predictions": {
                "DNN": "",
                "CNN": "",
                "GRU": "",
                "CAE": "",
                "LSTM": "",
            },
            "performance": {
                "latency_ms": 0,
                "latency_until_inference": 0
            },
        }

        self.on_update(packet, flow)

    def on_update(self, packet: Any, flow: Any) -> None:
        """
        Invocado a cada pacote pertencente ao fluxo.

        Atualiza acumuladores de cabeçalho, janela inicial, pacotes com dados
        e janelas de atividade/inatividade.

        Args:
            packet: Pacote NFPacket atual.
            flow: Objeto NFlow associado.
        """
        # Comprimento total do cabeçalho (IP + L4)
        total_header_len: int = max(0, packet.ip_size - packet.payload_size)
        # Comprimento do cabeçalho da camada de transporte L4 (puro)
        transport_header_len: int = max(0, packet.transport_size - packet.payload_size)

        if packet.direction == 0:
            flow.udps.fwd_header_length += total_header_len

            # fwd_seg_size_min no CICFlowMeter reflete o menor cabeçalho TCP L4 observado
            if transport_header_len > 0:
                if flow.udps.fwd_seg_size_min == 0 or transport_header_len < flow.udps.fwd_seg_size_min:
                    flow.udps.fwd_seg_size_min = transport_header_len

            if packet.payload_size > 0:
                flow.udps.fwd_act_data_pkts += 1

            # Janela inicial forward capturada estritamente no primeiro pacote TCP da direção
            if flow.udps.fwd_init_win_bytes == -1:
                flow.udps.fwd_init_win_bytes = extract_tcp_window_size(packet) if packet.protocol == 6 else 0
        else:
            flow.udps.bwd_header_length += total_header_len

            # Janela inicial backward capturada no primeiro pacote TCP reverso
            if flow.udps.bwd_init_win_bytes == -1:
                flow.udps.bwd_init_win_bytes = extract_tcp_window_size(packet) if packet.protocol == 6 else 0

        # Rastreamento de períodos de Atividade e Ociosidade (Idle threshold: 5000 ms = 5s)
        if packet.delta_time > 5000:
            active_duration_us: float = float(flow.udps.end_active_time_ms - flow.udps.start_active_time_ms) * 1000.0
            if active_duration_us > 0:
                flow.udps.active_times.append(active_duration_us)
            flow.udps.idle_times.append(float(packet.delta_time) * 1000.0)
            flow.udps.start_active_time_ms = packet.time
            flow.udps.end_active_time_ms = packet.time
        else:
            flow.udps.end_active_time_ms = packet.time

    def on_expire(self, flow: Any) -> None:
        """
        Invocado no encerramento (expiração) do fluxo no NFStream.

        Calcula as agregações finais: taxas por segundo, médias de segmentos,
        variância do tamanho de pacotes e estatísticas completas de Active/Idle em microssegundos (μs).

        Args:
            flow: Objeto NFlow expirado contendo métricas nativas acumuladas.
        """
        # Garante inicialização limpa de janelas caso fluxo não tenha recebido pacotes em uma direção
        if flow.udps.fwd_init_win_bytes == -1:
            flow.udps.fwd_init_win_bytes = 0
        if flow.udps.bwd_init_win_bytes == -1:
            flow.udps.bwd_init_win_bytes = 0

        total_packets: int = flow.bidirectional_packets
        total_bytes: int = flow.bidirectional_bytes
        duration_s: float = flow.bidirectional_duration_ms / 1000.0

        if total_packets > 0:
            flow.udps.avg_bytes_per_packet = float(total_bytes / total_packets)

        if duration_s > 0:
            flow.udps.bytes_per_second = float(total_bytes / duration_s)
            flow.udps.packets_per_second = float(total_packets / duration_s)
            flow.udps.fwd_packets_per_second = float(flow.src2dst_packets / duration_s)
            flow.udps.bwd_packets_per_second = float(flow.dst2src_packets / duration_s)

        if flow.src2dst_packets > 0:
            flow.udps.down_up_ratio = float(flow.dst2src_packets / flow.src2dst_packets)

        # Estatísticas de subfluxos
        flow.udps.subflow_fwd_packets = flow.src2dst_packets
        flow.udps.subflow_fwd_bytes = flow.src2dst_bytes
        flow.udps.subflow_bwd_packets = flow.dst2src_packets
        flow.udps.subflow_bwd_bytes = flow.dst2src_bytes

        # Médias de tamanho de segmento
        flow.udps.fwd_segment_size_avg = float(getattr(flow, "src2dst_mean_ps", 0.0))
        flow.udps.bwd_segment_size_avg = float(getattr(flow, "dst2src_mean_ps", 0.0))

        # Variância do comprimento dos pacotes (desvio padrão amostral elevado ao quadrado)
        b_std: float = float(getattr(flow, "bidirectional_stddev_ps", 0.0))
        flow.udps.packet_length_variance = float(b_std ** 2)

        # Consolidação do último período ativo
        final_active_us: float = float(flow.udps.end_active_time_ms - flow.udps.start_active_time_ms) * 1000.0
        if final_active_us > 0:
            flow.udps.active_times.append(final_active_us)
        elif not flow.udps.active_times and flow.bidirectional_duration_ms > 0:
            # Caso não tenha havido períodos de inatividade, o período ativo é a duração total do fluxo em μs
            flow.udps.active_times.append(float(flow.bidirectional_duration_ms * 1000.0))

        # Estatísticas de Active Time (em microssegundos)
        if flow.udps.active_times:
            act: np.ndarray = np.asarray(flow.udps.active_times, dtype=np.float64)
            flow.udps.active_min = float(np.min(act))
            flow.udps.active_mean = float(np.mean(act))
            flow.udps.active_max = float(np.max(act))
            flow.udps.active_std = float(np.std(act))

        # Estatísticas de Idle Time (em microssegundos)
        if flow.udps.idle_times:
            idl: np.ndarray = np.asarray(flow.udps.idle_times, dtype=np.float64)
            flow.udps.idle_min = float(np.min(idl))
            flow.udps.idle_mean = float(np.mean(idl))
            flow.udps.idle_max = float(np.max(idl))
            flow.udps.idle_std = float(np.std(idl))

        # NOTA ARQUITETURAL (SRP e CUDA Context):
        # A inferência de modelos neurais (TensorFlow/Keras/PyTorch) NÃO deve ser executada
        # dentro de plugins do NFStream (on_expire/on_update). O NFStream utiliza multiprocessing
        # via fork no Linux; qualquer chamada ao driver CUDA em processo filho forked resulta em:
        # CUDA_ERROR_NOT_INITIALIZED (absl crash fatal). Além disso, violaria o SRP do extrator.
        # A inferência de produção deve ser sempre realizada no loop consumidor do processo principal.

    def _infer_flow(self, flow: Any) -> None:
        """
        Executa inferência direta no modelo neural ALF-MoE ao expirar o fluxo.
        Popula flow.udps.PREDICTION com as classes, probabilidades, pesos e latências.
        """
        try:
            t0 = time.perf_counter()
            features_dict = flow_to_dict(flow) if self.pattern == 1 else flow_to_dict_2(flow)
            X = self.preprocessor.transform_features(features_dict)

            # Execução direta pelo grafo funcional Keras (evita overhead do predict())
            if callable(self._model):
                preds = self._model(X, training=False)
            else:
                preds = self.model_wrapper.predict(X, batch_size=1)

            latency_ms = (time.perf_counter() - t0) * 1000.0

            alf_probs = preds["ALF"].numpy()[0] if hasattr(preds["ALF"], "numpy") else np.asarray(preds["ALF"])[0]
            pred_idx = int(np.argmax(alf_probs))
            pred_class = self.classes[pred_idx] if self.classes and pred_idx < len(self.classes) else str(pred_idx)
            confidence = float(alf_probs[pred_idx])
            is_threat = 1 if (("benign" not in pred_class.lower()) and (confidence >= self.threat_threshold)) else 0

            expert_names = ["DNN", "CNN", "GRU", "CAE", "LSTM"]
            gn_raw = preds["GN"].numpy()[0] if hasattr(preds["GN"], "numpy") else np.asarray(preds["GN"])[0]
            gn_weights = {name: float(w) for name, w in zip(expert_names, gn_raw)}

            experts_preds = {}
            for name in expert_names:
                if name in preds:
                    exp_raw = preds[name].numpy()[0] if hasattr(preds[name], "numpy") else np.asarray(preds[name])[0]
                    e_idx = int(np.argmax(exp_raw))
                    experts_preds[name] = self.classes[e_idx] if self.classes and e_idx < len(self.classes) else str(e_idx)
                else:
                    experts_preds[name] = ""

            arrival_time_ms = getattr(flow, "bidirectional_first_seen_ms", 0)
            now_ms = time.time() * 1000.0
            latency_until_inference = max(0.0, now_ms - arrival_time_ms) if arrival_time_ms > 0 else latency_ms

            flow.udps.PREDICTION = {
                "LABEL": pred_class,
                "confidence": confidence,
                "is_threat": is_threat,
                "gating_attention_weights": gn_weights,
                "experts_predictions": experts_preds,
                "performance": {
                    "latency_ms": latency_ms,
                    "latency_until_inference": latency_until_inference,
                },
            }
        except Exception:
            flow.udps.PREDICTION = {
                "LABEL": "ERROR",
                "confidence": 0.0,
                "is_threat": -1,
                "gating_attention_weights": {k: 0.0 for k in ["DNN", "CNN", "GRU", "CAE", "LSTM"]},
                "experts_predictions": {k: "" for k in ["DNN", "CNN", "GRU", "CAE", "LSTM"]},
                "performance": {
                    "latency_ms": 0.0,
                    "latency_until_inference": 0.0,
                },
            }

    def cleanup(self) -> None:
        """Limpeza de recursos do plugin."""
        pass


def flow_to_dict(flow: Any) -> Dict[str, Union[int, float]]:
    """
    Converte um objeto NFlow do NFStream em um dicionário com as 76 features canônicas
    do padrão CICFlowMeter / CIC-UNSW-NB15 / CIC-BCCC-NRC-2024.

    Garante que todas as métricas temporais estejam estritamente em microssegundos (μs),
    reproduzindo exatamente a distribuição esperada pelos modelos treinados nesses datasets.

    Args:
        flow: Objeto NFlow processado pelo NFStream com o plugin FeatureExtractor.

    Returns:
        Dict[str, Union[int, float]]: Dicionário com as 76 chaves canônicas do CICFlowMeter.
    """
    udps: Any = getattr(flow, "udps", None)

    return {
        # 1. Duração do fluxo (microssegundos: ms * 1000)
        "Flow duration": float(getattr(flow, "bidirectional_duration_ms", 0) * 1000.0),

        # 2. Contadores de pacotes e bytes
        "Total Fwd Packet": int(getattr(flow, "src2dst_packets", 0)),
        "Total Bwd packets": int(getattr(flow, "dst2src_packets", 0)),
        "Total Length of Fwd Packet": int(getattr(flow, "src2dst_bytes", 0)),
        "Total Length of Bwd Packet": int(getattr(flow, "dst2src_bytes", 0)),

        # 3. Estatísticas de comprimento dos pacotes Forward
        "Fwd Packet Length Min": float(getattr(flow, "src2dst_min_ps", 0.0)),
        "Fwd Packet Length Max": float(getattr(flow, "src2dst_max_ps", 0.0)),
        "Fwd Packet Length Mean": float(getattr(flow, "src2dst_mean_ps", 0.0)),
        "Fwd Packet Length Std": float(getattr(flow, "src2dst_stddev_ps", 0.0)),

        # 4. Estatísticas de comprimento dos pacotes Backward
        "Bwd Packet Length Min": float(getattr(flow, "dst2src_min_ps", 0.0)),
        "Bwd Packet Length Max": float(getattr(flow, "dst2src_max_ps", 0.0)),
        "Bwd Packet Length Mean": float(getattr(flow, "dst2src_mean_ps", 0.0)),
        "Bwd Packet Length Std": float(getattr(flow, "dst2src_stddev_ps", 0.0)),

        # 5. Taxas de transferência
        "Flow Bytes/s": float(getattr(udps, "bytes_per_second", 0.0) if udps else 0.0),
        "Flow Packets/s": float(getattr(udps, "packets_per_second", 0.0) if udps else 0.0),

        # 6. Estatísticas de IAT Bidirecional (microssegundos: ms * 1000)
        "Flow IAT Mean": float(getattr(flow, "bidirectional_mean_piat_ms", 0.0) * 1000.0),
        "Flow IAT Std": float(getattr(flow, "bidirectional_stddev_piat_ms", 0.0) * 1000.0),
        "Flow IAT Max": float(getattr(flow, "bidirectional_max_piat_ms", 0.0) * 1000.0),
        "Flow IAT Min": float(getattr(flow, "bidirectional_min_piat_ms", 0.0) * 1000.0),

        # 7. Estatísticas de IAT Forward (microssegundos: ms * 1000)
        "Fwd IAT Min": float(getattr(flow, "src2dst_min_piat_ms", 0.0) * 1000.0),
        "Fwd IAT Max": float(getattr(flow, "src2dst_max_piat_ms", 0.0) * 1000.0),
        "Fwd IAT Mean": float(getattr(flow, "src2dst_mean_piat_ms", 0.0) * 1000.0),
        "Fwd IAT Std": float(getattr(flow, "src2dst_stddev_piat_ms", 0.0) * 1000.0),
        "Fwd IAT Total": float(getattr(flow, "src2dst_duration_ms", 0.0) * 1000.0),

        # 8. Estatísticas de IAT Backward (microssegundos: ms * 1000)
        "Bwd IAT Min": float(getattr(flow, "dst2src_min_piat_ms", 0.0) * 1000.0),
        "Bwd IAT Max": float(getattr(flow, "dst2src_max_piat_ms", 0.0) * 1000.0),
        "Bwd IAT Mean": float(getattr(flow, "dst2src_mean_piat_ms", 0.0) * 1000.0),
        "Bwd IAT Std": float(getattr(flow, "dst2src_stddev_piat_ms", 0.0) * 1000.0),
        "Bwd IAT Total": float(getattr(flow, "dst2src_duration_ms", 0.0) * 1000.0),

        # 9. Flags TCP direcionais
        "Fwd PSH flags": int(getattr(flow, "src2dst_psh_packets", 0)),
        "Bwd PSH Flags": int(getattr(flow, "dst2src_psh_packets", 0)),
        "Fwd URG Flags": int(getattr(flow, "src2dst_urg_packets", 0)),
        "Bwd URG Flags": int(getattr(flow, "dst2src_urg_packets", 0)),

        # 10. Cabeçalhos e Taxas direcionais
        "Fwd Header Length": int(getattr(udps, "fwd_header_length", 0) if udps else 0),
        "Bwd Header Length": int(getattr(udps, "bwd_header_length", 0) if udps else 0),
        "FWD Packets/s": float(getattr(udps, "fwd_packets_per_second", 0.0) if udps else 0.0),
        "Bwd Packets/s": float(getattr(udps, "bwd_packets_per_second", 0.0) if udps else 0.0),

        # 11. Estatísticas de comprimento bidirecional dos pacotes
        "Packet Length Min": float(getattr(flow, "bidirectional_min_ps", 0.0)),
        "Packet Length Max": float(getattr(flow, "bidirectional_max_ps", 0.0)),
        "Packet Length Mean": float(getattr(flow, "bidirectional_mean_ps", 0.0)),
        "Packet Length Std": float(getattr(flow, "bidirectional_stddev_ps", 0.0)),
        "Packet Length Variance": float(getattr(udps, "packet_length_variance", 0.0) if udps else 0.0),

        # 12. Contadores globais de flags TCP
        "FIN Flag Count": int(getattr(flow, "bidirectional_fin_packets", 0)),
        "SYN Flag Count": int(getattr(flow, "bidirectional_syn_packets", 0)),
        "RST Flag Count": int(getattr(flow, "bidirectional_rst_packets", 0)),
        "PSH Flag Count": int(getattr(flow, "bidirectional_psh_packets", 0)),
        "ACK Flag Count": int(getattr(flow, "bidirectional_ack_packets", 0)),
        "URG Flag Count": int(getattr(flow, "bidirectional_urg_packets", 0)),
        "CWR Flag Count": int(getattr(flow, "bidirectional_cwr_packets", 0)),
        "ECE Flag Count": int(getattr(flow, "bidirectional_ece_packets", 0)),

        # 13. Razões e Médias de segmentos
        "Down/Up Ratio": float(getattr(udps, "down_up_ratio", 0.0) if udps else 0.0),
        "Average Packet Size": float(getattr(udps, "avg_bytes_per_packet", 0.0) if udps else 0.0),
        "Fwd Segment Size Avg": float(getattr(udps, "fwd_segment_size_avg", 0.0) if udps else 0.0),
        "Bwd Segment Size Avg": float(getattr(udps, "bwd_segment_size_avg", 0.0) if udps else 0.0),

        # 14. Atributos de Bulk (padrão 0.0)
        "Fwd Bytes/Bulk Avg": float(getattr(udps, "fwd_bytes_bulk_avg", 0.0) if udps else 0.0),
        "Fwd Packet/Bulk Avg": float(getattr(udps, "fwd_packet_bulk_avg", 0.0) if udps else 0.0),
        "Fwd Bulk Rate Avg": float(getattr(udps, "fwd_bulk_rate_avg", 0.0) if udps else 0.0),
        "Bwd Bytes/Bulk Avg": float(getattr(udps, "bwd_bytes_bulk_avg", 0.0) if udps else 0.0),
        "Bwd Packet/Bulk Avg": float(getattr(udps, "bwd_packet_bulk_avg", 0.0) if udps else 0.0),
        "Bwd Bulk Rate Avg": float(getattr(udps, "bwd_bulk_rate_avg", 0.0) if udps else 0.0),

        # 15. Atributos de Subfluxo
        "Subflow Fwd Packets": int(getattr(udps, "subflow_fwd_packets", 0) if udps else 0),
        "Subflow Fwd Bytes": int(getattr(udps, "subflow_fwd_bytes", 0) if udps else 0),
        "Subflow Bwd Packets": int(getattr(udps, "subflow_bwd_packets", 0) if udps else 0),
        "Subflow Bwd Bytes": int(getattr(udps, "subflow_bwd_bytes", 0) if udps else 0),

        # 16. Janelas TCP e pacotes ativos de dados
        "Fwd Init Win bytes": int(getattr(udps, "fwd_init_win_bytes", 0) if udps else 0),
        "Bwd Init Win bytes": int(getattr(udps, "bwd_init_win_bytes", 0) if udps else 0),
        "Fwd Act Data Pkts": int(getattr(udps, "fwd_act_data_pkts", 0) if udps else 0),
        "Fwd Seg Size Min": int(getattr(udps, "fwd_seg_size_min", 0) if udps else 0),

        # 17. Estatísticas de Atividade e Ociosidade (microssegundos)
        "Active Min": float(getattr(udps, "active_min", 0.0) if udps else 0.0),
        "Active Mean": float(getattr(udps, "active_mean", 0.0) if udps else 0.0),
        "Active Max": float(getattr(udps, "active_max", 0.0) if udps else 0.0),
        "Active Std": float(getattr(udps, "active_std", 0.0) if udps else 0.0),
        "Idle Min": float(getattr(udps, "idle_min", 0.0) if udps else 0.0),
        "Idle Mean": float(getattr(udps, "idle_mean", 0.0) if udps else 0.0),
        "Idle Max": float(getattr(udps, "idle_max", 0.0) if udps else 0.0),
        "Idle Std": float(getattr(udps, "idle_std", 0.0) if udps else 0.0),
    }


def flow_to_dict_2(flow: Any) -> Dict[str, Union[int, float]]:
    """
    Converte um objeto NFlow do NFStream em um dicionário com as 76 features canônicas
    do padrão CSE-CIC-IDS2018.

    Garante que todas as métricas temporais estejam estritamente em microssegundos (μs),
    reproduzindo exatamente a distribuição esperada pelos modelos treinados nesses datasets.

    Args:
        flow: Objeto NFlow processado pelo NFStream com o plugin FeatureExtractor.

    Returns:
        Dict[str, Union[int, float]]: Dicionário com as 76 chaves canônicas do CICFlowMeter.
    """
    udps: Any = getattr(flow, "udps", None)


    return {
        # 1. Duração do fluxo (microssegundos: ms * 1000)
        "Flow Duration": float(getattr(flow, "bidirectional_duration_ms", 0) * 1000.0),

        # 2. Contadores de pacotes e bytes
        "Tot Fwd Pkts": int(getattr(flow, "src2dst_packets", 0)),
        "Tot Bwd Pkts": int(getattr(flow, "dst2src_packets", 0)),
        "TotLen Fwd Pkts": int(getattr(flow, "src2dst_bytes", 0)),
        "TotLen Bwd Pkts": int(getattr(flow, "dst2src_bytes", 0)),

        # 3. Estatísticas de comprimento dos pacotes Forward
        "Fwd Pkt Len Min": float(getattr(flow, "src2dst_min_ps", 0.0)),
        "Fwd Pkt Len Max": float(getattr(flow, "src2dst_max_ps", 0.0)),
        "Fwd Pkt Len Mean": float(getattr(flow, "src2dst_mean_ps", 0.0)),
        "Fwd Pkt Len Std": float(getattr(flow, "src2dst_stddev_ps", 0.0)),

        # 4. Estatísticas de comprimento dos pacotes Backward
        "Bwd Pkt Len Min": float(getattr(flow, "dst2src_min_ps", 0.0)),
        "Bwd Pkt Len Max": float(getattr(flow, "dst2src_max_ps", 0.0)),
        "Bwd Pkt Len Mean": float(getattr(flow, "dst2src_mean_ps", 0.0)),
        "Bwd Pkt Len Std": float(getattr(flow, "dst2src_stddev_ps", 0.0)),

        # 5. Taxas de transferência
        "Flow Byts/s": float(getattr(udps, "bytes_per_second", 0.0) if udps else 0.0),
        "Flow Pkts/s": float(getattr(udps, "packets_per_second", 0.0) if udps else 0.0),

        # 6. Estatísticas de IAT Bidirecional (microssegundos: ms * 1000)
        "Flow IAT Mean": float(getattr(flow, "bidirectional_mean_piat_ms", 0.0) * 1000.0),
        "Flow IAT Std": float(getattr(flow, "bidirectional_stddev_piat_ms", 0.0) * 1000.0),
        "Flow IAT Max": float(getattr(flow, "bidirectional_max_piat_ms", 0.0) * 1000.0),
        "Flow IAT Min": float(getattr(flow, "bidirectional_min_piat_ms", 0.0) * 1000.0),

        # 7. Estatísticas de IAT Forward (microssegundos: ms * 1000)
        "Fwd IAT Min": float(getattr(flow, "src2dst_min_piat_ms", 0.0) * 1000.0),
        "Fwd IAT Max": float(getattr(flow, "src2dst_max_piat_ms", 0.0) * 1000.0),
        "Fwd IAT Mean": float(getattr(flow, "src2dst_mean_piat_ms", 0.0) * 1000.0),
        "Fwd IAT Std": float(getattr(flow, "src2dst_stddev_piat_ms", 0.0) * 1000.0),
        "Fwd IAT Tot": float(getattr(flow, "src2dst_duration_ms", 0.0) * 1000.0),

        # 8. Estatísticas de IAT Backward (microssegundos: ms * 1000)
        "Bwd IAT Min": float(getattr(flow, "dst2src_min_piat_ms", 0.0) * 1000.0),
        "Bwd IAT Max": float(getattr(flow, "dst2src_max_piat_ms", 0.0) * 1000.0),
        "Bwd IAT Mean": float(getattr(flow, "dst2src_mean_piat_ms", 0.0) * 1000.0),
        "Bwd IAT Std": float(getattr(flow, "dst2src_stddev_piat_ms", 0.0) * 1000.0),
        "Bwd IAT Tot": float(getattr(flow, "dst2src_duration_ms", 0.0) * 1000.0),

        # 9. Flags TCP direcionais
        "Fwd PSH Flags": int(getattr(flow, "src2dst_psh_packets", 0)),
        "Bwd PSH Flags": int(getattr(flow, "dst2src_psh_packets", 0)),
        "Fwd URG Flags": int(getattr(flow, "src2dst_urg_packets", 0)),
        "Bwd URG Flags": int(getattr(flow, "dst2src_urg_packets", 0)),

        # 10. Cabeçalhos e Taxas direcionais
        "Fwd Header Len": int(getattr(udps, "fwd_header_length", 0) if udps else 0),
        "Bwd Header Len": int(getattr(udps, "bwd_header_length", 0) if udps else 0),
        "Fwd Pkts/s": float(getattr(udps, "fwd_packets_per_second", 0.0) if udps else 0.0),
        "Bwd Pkts/s": float(getattr(udps, "bwd_packets_per_second", 0.0) if udps else 0.0),

        # 11. Estatísticas de comprimento bidirecional dos pacotes
        "Pkt Len Min": float(getattr(flow, "bidirectional_min_ps", 0.0)),
        "Pkt Len Max": float(getattr(flow, "bidirectional_max_ps", 0.0)),
        "Pkt Len Mean": float(getattr(flow, "bidirectional_mean_ps", 0.0)),
        "Pkt Len Std": float(getattr(flow, "bidirectional_stddev_ps", 0.0)),
        "Pkt Len Var": float(getattr(udps, "packet_length_variance", 0.0) if udps else 0.0),

        # 12. Contadores globais de flags TCP
        "FIN Flag Cnt": int(getattr(flow, "bidirectional_fin_packets", 0)),
        "SYN Flag Cnt": int(getattr(flow, "bidirectional_syn_packets", 0)),
        "RST Flag Cnt": int(getattr(flow, "bidirectional_rst_packets", 0)),
        "PSH Flag Cnt": int(getattr(flow, "bidirectional_psh_packets", 0)),
        "ACK Flag Cnt": int(getattr(flow, "bidirectional_ack_packets", 0)),
        "URG Flag Cnt": int(getattr(flow, "bidirectional_urg_packets", 0)),
        "CWE Flag Count": int(getattr(flow, "bidirectional_cwr_packets", 0)),
        "ECE Flag Cnt": int(getattr(flow, "bidirectional_ece_packets", 0)),

        # 13. Razões e Médias de segmentos
        "Down/Up Ratio": float(getattr(udps, "down_up_ratio", 0.0) if udps else 0.0),
        "Pkt Size Avg": float(getattr(udps, "avg_bytes_per_packet", 0.0) if udps else 0.0),
        "Fwd Seg Size Avg": float(getattr(udps, "fwd_segment_size_avg", 0.0) if udps else 0.0),
        "Bwd Seg Size Avg": float(getattr(udps, "bwd_segment_size_avg", 0.0) if udps else 0.0),

        # 14. Atributos de Bulk (padrão 0.0)
        "Fwd Byts/b Avg": float(getattr(udps, "fwd_bytes_bulk_avg", 0.0) if udps else 0.0),
        "Fwd Pkts/b Avg": float(getattr(udps, "fwd_packet_bulk_avg", 0.0) if udps else 0.0),
        "Fwd Blk Rate Avg": float(getattr(udps, "fwd_bulk_rate_avg", 0.0) if udps else 0.0),
        "Bwd Byts/b Avg": float(getattr(udps, "bwd_bytes_bulk_avg", 0.0) if udps else 0.0),
        "Bwd Pkts/b Avg": float(getattr(udps, "bwd_packet_bulk_avg", 0.0) if udps else 0.0),
        "Bwd Blk Rate Avg": float(getattr(udps, "bwd_bulk_rate_avg", 0.0) if udps else 0.0),

        # 15. Atributos de Subfluxo
        "Subflow Fwd Pkts": int(getattr(udps, "subflow_fwd_packets", 0) if udps else 0),
        "Subflow Fwd Byts": int(getattr(udps, "subflow_fwd_bytes", 0) if udps else 0),
        "Subflow Bwd Pkts": int(getattr(udps, "subflow_bwd_packets", 0) if udps else 0),
        "Subflow Bwd Byts": int(getattr(udps, "subflow_bwd_bytes", 0) if udps else 0),

        # 16. Janelas TCP e pacotes ativos de dados
        "Init Fwd Win Byts": int(getattr(udps, "fwd_init_win_bytes", 0) if udps else 0),
        "Init Bwd Win Byts": int(getattr(udps, "bwd_init_win_bytes", 0) if udps else 0),
        "Fwd Act Data Pkts": int(getattr(udps, "fwd_act_data_pkts", 0) if udps else 0),
        "Fwd Seg Size Min": int(getattr(udps, "fwd_seg_size_min", 0) if udps else 0),

        # 17. Estatísticas de Atividade e Ociosidade (microssegundos)
        "Active Min": float(getattr(udps, "active_min", 0.0) if udps else 0.0),
        "Active Mean": float(getattr(udps, "active_mean", 0.0) if udps else 0.0),
        "Active Max": float(getattr(udps, "active_max", 0.0) if udps else 0.0),
        "Active Std": float(getattr(udps, "active_std", 0.0) if udps else 0.0),
        "Idle Min": float(getattr(udps, "idle_min", 0.0) if udps else 0.0),
        "Idle Mean": float(getattr(udps, "idle_mean", 0.0) if udps else 0.0),
        "Idle Max": float(getattr(udps, "idle_max", 0.0) if udps else 0.0),
        "Idle Std": float(getattr(udps, "idle_std", 0.0) if udps else 0.0),
    }



def convert_into_features(flow: Any, pattern: Literal[1, 2] = 1) -> pd.DataFrame:
    """
    Converte um objeto NFlow do NFStream em um DataFrame com as 76 features canônicas do CICFlowMeter.

    Mantém o Princípio da Responsabilidade Única (SRP): não aplica transformações numéricas
    de machine learning (log1p, scalers, encoders) ou reshaping de especialistas.

    Args:
        flow: Objeto NFlow processado pelo NFStream com o plugin FeatureExtractor.
        pattern: 
            - 1 : CICFlowMeter / CIC-UNSW-NB15 / CIC-BCCC-NRC-2024
            - 2 : CSE-CIC-IDS2018

    Returns:
        pd.DataFrame: DataFrame contendo 1 linha e as 76 colunas canônicas brutas.
    """
    features_dict: Dict[str, Union[int, float]] = flow_to_dict(flow) if pattern == 1 else flow_to_dict_2(flow)
    return pd.DataFrame([features_dict])


if __name__ == "__main__":
    import sys

    interface: str = "wlp63s0" if len(sys.argv) < 2 else sys.argv[1]
    print(f"{'='*20} Feature Extractor Test (Interface: {interface}) {'='*20}")

    try:
        streamer: NFStreamer = NFStreamer(
            source=interface,
            decode_tunnels=True,
            promiscuous_mode=True,
            statistical_analysis=True,
            udps=[FeatureExtractor()],
            idle_timeout=120,
            active_timeout=1800,
        )
    except Exception as exc:
        print(f"Erro ao inicializar captura na interface {interface}: {exc}")
        sys.exit(1)

    flow_count: int = 0
    for flow in streamer:
        flow_df: pd.DataFrame = convert_into_features(flow)
        print(f"Fluxo capturado [{flow_count + 1}]: {flow.src_ip}:{flow.src_port} -> {flow.dst_ip}:{flow.dst_port}")
        print(f"Shape do DataFrame: {flow_df.shape} | Colunas: {len(flow_df.columns)}")
        print(f"Duração (μs): {flow_df['Flow duration'].iloc[0]:.2f} | Total Pacotes: {flow_df['Total Fwd Packet'].iloc[0] + flow_df['Total Bwd packets'].iloc[0]}")
        print(f"{'='*60}\n")
        flow_count += 1
        if flow_count >= 10:
            break
