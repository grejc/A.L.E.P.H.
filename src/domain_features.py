
from typing import Literal, Optional, Any
from collections.abc import Iterator


class CICDomainFeatures:
    def __init__(self):
        self.raw = self._raw_features_list()
        self.F_g = len(self.x_g())
        self.L_s = len(self.x_s())
        self.T_v = len(self.x_v()) // 4
        self.d_v = 4
        self.L_f = len(self.x_f())
        self.T_t = len(self.x_t())

    def _raw_features_list(self) -> list[str]:
        '''
        Returns the raw features list extracted from CICFlowMeter
        '''
        return [
            'Flow duration',
            'Total Fwd Packet',
            'Total Bwd packets',
            'Total Length of Fwd Packet',
            'Total Length of Bwd Packet',
            'Fwd Packet Length Min',
            'Fwd Packet Length Max',
            'Fwd Packet Length Mean',
            'Fwd Packet Length Std',
            'Bwd Packet Length Min',
            'Bwd Packet Length Max',
            'Bwd Packet Length Mean',
            'Bwd Packet Length Std',
            'Flow Bytes/s',
            'Flow Packets/s',
            'Flow IAT Mean',
            'Flow IAT Std',
            'Flow IAT Max',
            'Flow IAT Min',
            'Fwd IAT Min',
            'Fwd IAT Max',
            'Fwd IAT Mean',
            'Fwd IAT Std',
            'Fwd IAT Total',
            'Bwd IAT Min',
            'Bwd IAT Max',
            'Bwd IAT Mean',
            'Bwd IAT Std',
            'Bwd IAT Total',
            'Fwd PSH flags',
            'Bwd PSH Flags',
            'Fwd URG Flags',
            'Bwd URG Flags',
            'Fwd Header Length',
            'Bwd Header Length',
            'FWD Packets/s',
            'Bwd Packets/s',
            'Packet Length Min',
            'Packet Length Max',
            'Packet Length Mean',
            'Packet Length Std',
            'Packet Length Variance',
            'FIN Flag Count',
            'SYN Flag Count',
            'RST Flag Count',
            'PSH Flag Count',
            'ACK Flag Count',
            'URG Flag Count',
            'CWR Flag Count',
            'ECE Flag Count',
            'Down/Up Ratio',
            'Average Packet Size',
            'Fwd Segment Size Avg',
            'Bwd Segment Size Avg',
            'Fwd Bytes/Bulk Avg',
            'Fwd Packet/Bulk Avg',
            'Fwd Bulk Rate Avg',
            'Bwd Bytes/Bulk Avg',
            'Bwd Packet/Bulk Avg',
            'Bwd Bulk Rate Avg',
            'Subflow Fwd Packets',
            'Subflow Fwd Bytes',
            'Subflow Bwd Packets',
            'Subflow Bwd Bytes',
            'Fwd Init Win bytes',
            'Bwd Init Win bytes',
            'Fwd Act Data Pkts',
            'Fwd Seg Size Min',
            'Active Min',
            'Active Mean',
            'Active Max',
            'Active Std',
            'Idle Min',
            'Idle Mean',
            'Idle Max',
            'Idle Std',
        ]

    def x_g(self) -> list[str]:
        return [
            'Flow duration',
            'Total Fwd Packet',
            'Total Bwd packets',
            'Total Length of Fwd Packet',
            'Total Length of Bwd Packet',
            'Flow Bytes/s',
            'Flow Packets/s',
            'Fwd PSH flags',
            'Fwd URG Flags',
            'Fwd Header Length',
            'Bwd Header Length',
            'FIN Flag Count',
            'SYN Flag Count',
            'RST Flag Count',
            'PSH Flag Count',
            'ACK Flag Count',
            'URG Flag Count',
            'CWR Flag Count',
            'ECE Flag Count',
            'Down/Up Ratio',
            'Average Packet Size',
            'Subflow Fwd Packets',
            'Subflow Fwd Bytes',
            'Subflow Bwd Packets',
            'Subflow Bwd Bytes',
            'Fwd Init Win bytes',
            'Bwd Init Win bytes',
            'Fwd Act Data Pkts',
            'Fwd Seg Size Min',
        ]

    def x_s(self) -> list[str]:
        return [
            'Fwd Packet Length Min',
            'Fwd Packet Length Max',
            'Fwd Packet Length Mean',
            'Fwd Packet Length Std',
            'Bwd Packet Length Min',
            'Bwd Packet Length Max',
            'Bwd Packet Length Mean',
            'Bwd Packet Length Std',
            'Packet Length Min',
            'Packet Length Max',
            'Packet Length Mean',
            'Packet Length Std',
            'Packet Length Variance',
            'Average Packet Size',
            'Fwd Segment Size Avg',
            'Bwd Segment Size Avg',
            'Fwd Header Length',
            'Bwd Header Length',
            'Down/Up Ratio',
            'Flow Packets/s',
        ]

    def x_v(self) -> list[str]:
        return [
            'Flow IAT Min',
            'Flow IAT Mean',
            'Flow IAT Std',
            'Flow IAT Max',
            'Fwd IAT Min',
            'Fwd IAT Mean',
            'Fwd IAT Std',
            'Fwd IAT Max',
            'Bwd IAT Min',
            'Bwd IAT Max',
            'Bwd IAT Mean',
            'Bwd IAT Std',
            'Total Fwd Packet',
            'Total Bwd packets',
            'Total Length of Fwd Packet',
            'Total Length of Bwd Packet',
            'Down/Up Ratio',
            'FWD Packets/s',
            'Bwd Packets/s',
            'Flow Packets/s',
            'Active Min',
            'Active Mean',
            'Active Max',
            'Active Std',
            'Idle Min',
            'Idle Mean',
            'Idle Max',
            'Idle Std',
            'Flow duration',
            'Fwd IAT Total',
            'Bwd IAT Total',
            'Packet Length Variance',
        ]

    def x_f(self) -> list[str]:
        return [
            'Flow duration',
            'Flow Bytes/s',
            'Flow Packets/s',
            'Flow IAT Mean',
            'Flow IAT Std',
            'Flow IAT Max',
            'Flow IAT Min',
            'Fwd IAT Min',
            'Fwd IAT Max',
            'Fwd IAT Mean',
            'Fwd IAT Std',
            'Fwd IAT Total',
            'Bwd IAT Min',
            'Bwd IAT Max',
            'Bwd IAT Mean',
            'Bwd IAT Std',
            'Bwd IAT Total',
            'Active Min',
            'Active Mean',
            'Active Max',
            'Active Std',
            'Idle Min',
            'Idle Mean',
            'Idle Max',
            'Idle Std',
            'Packet Length Std',
            'Packet Length Variance',
        ]

    def x_t(self) -> list[str]:
        return [
            'Flow duration',
            'Fwd IAT Total',
            'Bwd IAT Total',
            'Flow IAT Min',
            'Fwd IAT Min',
            'Bwd IAT Min',
            'Flow IAT Max',
            'Fwd IAT Max',
            'Bwd IAT Max',
            'Flow IAT Mean',
            'Fwd IAT Mean',
            'Bwd IAT Mean',
            'Flow IAT Std',
            'Fwd IAT Std',
            'Bwd IAT Std',
            'Flow Packets/s',
            'FWD Packets/s',
            'Bwd Packets/s',
        ]

    def __iter__(self) -> Iterator[list[str]]:
        return iter([
            self.x_g(),
            self.x_s(),
            self.x_v(),
            self.x_f(),
            self.x_t(),
            self._raw_features_list(),
        ])

    def __getitem__(
        self,
        _key: None | Literal['g', 's', 'v', 'f', 't'] | int | slice,
    ) -> list[str] | str:
        if isinstance(_key, int):
            return self._raw_features_list()[_key]
        if isinstance(_key, slice):
            return self._raw_features_list()[_key]
        if _key == 'g':
            return self.x_g()
        if _key == 's':
            return self.x_s()
        if _key == 'v':
            return self.x_v()
        if _key == 'f':
            return self.x_f()
        if _key == 't':
            return self.x_t()
        return self._raw_features_list()

    def get_colums(self, _group: Optional[Literal['g', 's', 'v', 'f', 't']]) -> list[int]:
        raw = self._raw_features_list()

        if not _group:
            wanted = raw
        elif _group == 'g':
            wanted = self.x_g()
        elif _group == 's':
            wanted = self.x_s()
        elif _group == 'v':
            wanted = self.x_v()
        elif _group == 'f':
            wanted = self.x_f()
        elif _group == 't':
            wanted = self.x_t()
        else:
            wanted = raw

        wanted_set = set(wanted)
        matched = [i for i in range(len(raw)) if raw[i] in wanted_set]
        if len(matched) == len(wanted):
            return matched

        # Fallback for common alias/abbreviation and case differences
        alias_map = {
            'flow duration': 'Flow duration',
            'fwd iat tot': 'Fwd IAT Total',
            'bwd iat tot': 'Bwd IAT Total',
            'flow pkts/s': 'Flow Packets/s',
            'fwd pkts/s': 'FWD Packets/s',
            'bwd pkts/s': 'Bwd Packets/s',
            'tot fwd pkts': 'Total Fwd Packet',
            'tot bwd pkts': 'Total Bwd packets',
            'totlen fwd pkts': 'Total Length of Fwd Packet',
            'totlen bwd pkts': 'Total Length of Bwd Packet',
            'fwd pkt len min': 'Fwd Packet Length Min',
            'fwd pkt len max': 'Fwd Packet Length Max',
            'fwd pkt len mean': 'Fwd Packet Length Mean',
            'fwd pkt len std': 'Fwd Packet Length Std',
            'bwd pkt len min': 'Bwd Packet Length Min',
            'bwd pkt len max': 'Bwd Packet Length Max',
            'bwd pkt len mean': 'Bwd Packet Length Mean',
            'bwd pkt len std': 'Bwd Packet Length Std',
            'pkt len min': 'Packet Length Min',
            'pkt len max': 'Packet Length Max',
            'pkt len mean': 'Packet Length Mean',
            'pkt len std': 'Packet Length Std',
            'pkt len var': 'Packet Length Variance',
            'pkt size avg': 'Average Packet Size',
            'fin flag cnt': 'FIN Flag Count',
            'syn flag cnt': 'SYN Flag Count',
            'rst flag cnt': 'RST Flag Count',
            'psh flag cnt': 'PSH Flag Count',
            'ack flag cnt': 'ACK Flag Count',
            'urg flag cnt': 'URG Flag Count',
            'cwe flag count': 'CWR Flag Count',
            'cwr flag cnt': 'CWR Flag Count',
            'ece flag cnt': 'ECE Flag Count',
            'fwd header len': 'Fwd Header Length',
            'bwd header len': 'Bwd Header Length',
            'init fwd win byts': 'Fwd Init Win bytes',
            'init bwd win byts': 'Bwd Init Win bytes',
        }
        resolved_wanted = set()
        for item in wanted:
            if item in raw:
                resolved_wanted.add(item)
            elif item.lower() in alias_map:
                resolved_wanted.add(alias_map[item.lower()])
            else:
                found = False
                for r in raw:
                    if r.lower() == item.lower():
                        resolved_wanted.add(r)
                        found = True
                        break
                if not found:
                    resolved_wanted.add(item)

        return [i for i in range(len(raw)) if raw[i] in resolved_wanted]

    @staticmethod
    def nfstream_to_cic_map(with_udps_prefix: bool = True, include_unprefixed: bool = True) -> dict[str, str]:
        '''
        Translation dictionary from NFStream (native features + FeatureExtractor plugin UDPS)
        to CICDomainFeatures / CICFlowMeter column names.

        Args:
            with_udps_prefix: If True, includes columns with 'udps.' prefix as generated by NFStream.to_pandas().
            include_unprefixed: If True, also includes unprefixed versions for direct flow.udps usage.

        Returns:
            Dictionary mapping NFStream feature names to CICDomainFeatures feature names.
        '''
        # Base mapping from native NFStream columns and plugin UDPS feature names
        native_mapping = {
            'bidirectional_duration_ms': 'Flow duration',
            'src2dst_packets': 'Total Fwd Packet',
            'dst2src_packets': 'Total Bwd packets',
            'src2dst_bytes': 'Total Length of Fwd Packet',
            'dst2src_bytes': 'Total Length of Bwd Packet',
            'src2dst_min_ps': 'Fwd Packet Length Min',
            'src2dst_max_ps': 'Fwd Packet Length Max',
            'src2dst_mean_ps': 'Fwd Packet Length Mean',
            'src2dst_stddev_ps': 'Fwd Packet Length Std',
            'dst2src_min_ps': 'Bwd Packet Length Min',
            'dst2src_max_ps': 'Bwd Packet Length Max',
            'dst2src_mean_ps': 'Bwd Packet Length Mean',
            'dst2src_stddev_ps': 'Bwd Packet Length Std',
            'bidirectional_mean_piat_ms': 'Flow IAT Mean',
            'bidirectional_stddev_piat_ms': 'Flow IAT Std',
            'bidirectional_max_piat_ms': 'Flow IAT Max',
            'bidirectional_min_piat_ms': 'Flow IAT Min',
            'src2dst_min_piat_ms': 'Fwd IAT Min',
            'src2dst_max_piat_ms': 'Fwd IAT Max',
            'src2dst_mean_piat_ms': 'Fwd IAT Mean',
            'src2dst_stddev_piat_ms': 'Fwd IAT Std',
            'src2dst_duration_ms': 'Fwd IAT Total',
            'dst2src_min_piat_ms': 'Bwd IAT Min',
            'dst2src_max_piat_ms': 'Bwd IAT Max',
            'dst2src_mean_piat_ms': 'Bwd IAT Mean',
            'dst2src_stddev_piat_ms': 'Bwd IAT Std',
            'dst2src_duration_ms': 'Bwd IAT Total',
            'src2dst_psh_packets': 'Fwd PSH flags',
            'dst2src_psh_packets': 'Bwd PSH Flags',
            'src2dst_urg_packets': 'Fwd URG Flags',
            'dst2src_urg_packets': 'Bwd URG Flags',
            'bidirectional_min_ps': 'Packet Length Min',
            'bidirectional_max_ps': 'Packet Length Max',
            'bidirectional_mean_ps': 'Packet Length Mean',
            'bidirectional_stddev_ps': 'Packet Length Std',
            'bidirectional_fin_packets': 'FIN Flag Count',
            'bidirectional_syn_packets': 'SYN Flag Count',
            'bidirectional_rst_packets': 'RST Flag Count',
            'bidirectional_psh_packets': 'PSH Flag Count',
            'bidirectional_ack_packets': 'ACK Flag Count',
            'bidirectional_urg_packets': 'URG Flag Count',
            'bidirectional_cwr_packets': 'CWR Flag Count',
            'bidirectional_ece_packets': 'ECE Flag Count',
        }

        plugin_udps_mapping = {
            'bytes_per_second': 'Flow Bytes/s',
            'packets_per_second': 'Flow Packets/s',
            'fwd_header_length': 'Fwd Header Length',
            'bwd_header_length': 'Bwd Header Length',
            'fwd_packets_per_second': 'FWD Packets/s',
            'bwd_packets_per_second': 'Bwd Packets/s',
            'packet_length_variance': 'Packet Length Variance',
            'down_up_ratio': 'Down/Up Ratio',
            'avg_bytes_per_packet': 'Average Packet Size',
            'fwd_segment_size_avg': 'Fwd Segment Size Avg',
            'bwd_segment_size_avg': 'Bwd Segment Size Avg',
            'fwd_bytes_bulk_avg': 'Fwd Bytes/Bulk Avg',
            'fwd_packet_bulk_avg': 'Fwd Packet/Bulk Avg',
            'fwd_bulk_rate_avg': 'Fwd Bulk Rate Avg',
            'bwd_bytes_bulk_avg': 'Bwd Bytes/Bulk Avg',
            'bwd_packet_bulk_avg': 'Bwd Packet/Bulk Avg',
            'bwd_bulk_rate_avg': 'Bwd Bulk Rate Avg',
            'subflow_fwd_packets': 'Subflow Fwd Packets',
            'subflow_fwd_bytes': 'Subflow Fwd Bytes',
            'subflow_bwd_packets': 'Subflow Bwd Packets',
            'subflow_bwd_bytes': 'Subflow Bwd Bytes',
            'fwd_init_win_bytes': 'Fwd Init Win bytes',
            'bwd_init_win_bytes': 'Bwd Init Win bytes',
            'fwd_act_data_pkts': 'Fwd Act Data Pkts',
            'fwd_seg_size_min': 'Fwd Seg Size Min',
            'active_min': 'Active Min',
            'active_mean': 'Active Mean',
            'active_max': 'Active Max',
            'active_std': 'Active Std',
            'idle_min': 'Idle Min',
            'idle_mean': 'Idle Mean',
            'idle_max': 'Idle Max',
            'idle_std': 'Idle Std',
            # Additional direct udps convenience attributes
            'flow_duration': 'Flow duration',
            'total_fwd_packets': 'Total Fwd Packet',
            'total_bwd_packets': 'Total Bwd packets',
            'total_length_of_fwd_packet': 'Total Length of Fwd Packet',
            'total_length_of_bwd_packet': 'Total Length of Bwd Packet',
            'fwd_packet_length_min': 'Fwd Packet Length Min',
            'fwd_packet_length_max': 'Fwd Packet Length Max',
            'fwd_packet_length_mean': 'Fwd Packet Length Mean',
            'fwd_packet_length_std': 'Fwd Packet Length Std',
            'bwd_packet_length_min': 'Bwd Packet Length Min',
            'bwd_packet_length_max': 'Bwd Packet Length Max',
            'bwd_packet_length_mean': 'Bwd Packet Length Mean',
            'bwd_packet_length_std': 'Bwd Packet Length Std',
            'flow_iat_mean': 'Flow IAT Mean',
            'flow_iat_std': 'Flow IAT Std',
            'flow_iat_max': 'Flow IAT Max',
            'flow_iat_min': 'Flow IAT Min',
            'fwd_iat_min': 'Fwd IAT Min',
            'fwd_iat_max': 'Fwd IAT Max',
            'fwd_iat_mean': 'Fwd IAT Mean',
            'fwd_iat_std': 'Fwd IAT Std',
            'fwd_iat_total': 'Fwd IAT Total',
            'bwd_iat_min': 'Bwd IAT Min',
            'bwd_iat_max': 'Bwd IAT Max',
            'bwd_iat_mean': 'Bwd IAT Mean',
            'bwd_iat_std': 'Bwd IAT Std',
            'bwd_iat_total': 'Bwd IAT Total',
            'fwd_psh_flags': 'Fwd PSH flags',
            'bwd_psh_flags': 'Bwd PSH Flags',
            'fwd_urg_flags': 'Fwd URG Flags',
            'bwd_urg_flags': 'Bwd URG Flags',
            'packet_length_min': 'Packet Length Min',
            'packet_length_max': 'Packet Length Max',
            'packet_length_mean': 'Packet Length Mean',
            'packet_length_std': 'Packet Length Std',
            'fin_flag_count': 'FIN Flag Count',
            'syn_flag_count': 'SYN Flag Count',
            'rst_flag_count': 'RST Flag Count',
            'psh_flag_count': 'PSH Flag Count',
            'ack_flag_count': 'ACK Flag Count',
            'urg_flag_count': 'URG Flag Count',
            'cwr_flag_count': 'CWR Flag Count',
            'ece_flag_count': 'ECE Flag Count',
        }

        result = {}

        # 1. Add native features
        result.update(native_mapping)

        # 2. Add prefixed plugin features if requested
        if with_udps_prefix:
            for k, v in plugin_udps_mapping.items():
                result[f'udps.{k}'] = v

        # 3. Add unprefixed plugin features if requested
        if include_unprefixed:
            for k, v in plugin_udps_mapping.items():
                if k not in result:
                    result[k] = v

        return result

    # Aliases
    nfstream_translation = nfstream_to_cic_map
    nfstream_to_cic = nfstream_to_cic_map
    get_nfstream_translation = nfstream_to_cic_map

    def match_columns(self, available_columns: list[str]) -> list[str]:
        '''
        Maps the 76 canonical CICDomainFeatures to matching columns in a DataFrame,
        supporting case-insensitivity, whitespace variations, and common dataset abbreviations
        (such as CSE-CIC-IDS2018: 'Tot Fwd Pkts', 'TotLen Fwd Pkts', 'Flow Byts/s', etc.).

        Args:
            available_columns: Iterable of column names present in the dataset.

        Returns:
            List of 76 column names from available_columns matching self.raw in order.
        '''
        alias_candidates = {
            'flow duration': ['flow duration'],
            'total fwd packet': ['tot fwd pkts', 'total fwd packet', 'total fwd packets', 'tot fwd pkt'],
            'total bwd packets': ['tot bwd pkts', 'total bwd packets', 'total bwd packet', 'total backward packets'],
            'total length of fwd packet': ['totlen fwd pkts', 'total length of fwd packet', 'total length of fwd packets'],
            'total length of bwd packet': ['totlen bwd pkts', 'total length of bwd packet', 'total length of bwd packets'],
            'fwd packet length min': ['fwd pkt len min', 'fwd packet length min'],
            'fwd packet length max': ['fwd pkt len max', 'fwd packet length max'],
            'fwd packet length mean': ['fwd pkt len mean', 'fwd packet length mean'],
            'fwd packet length std': ['fwd pkt len std', 'fwd packet length std'],
            'bwd packet length min': ['bwd pkt len min', 'bwd packet length min'],
            'bwd packet length max': ['bwd pkt len max', 'bwd packet length max'],
            'bwd packet length mean': ['bwd pkt len mean', 'bwd packet length mean'],
            'bwd packet length std': ['bwd pkt len std', 'bwd packet length std'],
            'flow bytes/s': ['flow byts/s', 'flow bytes/s'],
            'flow packets/s': ['flow pkts/s', 'flow packets/s'],
            'flow iat mean': ['flow iat mean'],
            'flow iat std': ['flow iat std'],
            'flow iat max': ['flow iat max'],
            'flow iat min': ['flow iat min'],
            'fwd iat min': ['fwd iat min'],
            'fwd iat max': ['fwd iat max'],
            'fwd iat mean': ['fwd iat mean'],
            'fwd iat std': ['fwd iat std'],
            'fwd iat total': ['fwd iat tot', 'fwd iat total'],
            'bwd iat min': ['bwd iat min'],
            'bwd iat max': ['bwd iat max'],
            'bwd iat mean': ['bwd iat mean'],
            'bwd iat std': ['bwd iat std'],
            'bwd iat total': ['bwd iat tot', 'bwd iat total'],
            'fwd psh flags': ['fwd psh flags'],
            'bwd psh flags': ['bwd psh flags'],
            'fwd urg flags': ['fwd urg flags'],
            'bwd urg flags': ['bwd urg flags'],
            'fwd header length': ['fwd header len', 'fwd header length', 'fwd header length.1'],
            'bwd header length': ['bwd header len', 'bwd header length'],
            'fwd packets/s': ['fwd pkts/s', 'fwd packets/s'],
            'bwd packets/s': ['bwd pkts/s', 'bwd packets/s'],
            'packet length min': ['pkt len min', 'packet length min'],
            'packet length max': ['pkt len max', 'packet length max'],
            'packet length mean': ['pkt len mean', 'packet length mean'],
            'packet length std': ['pkt len std', 'packet length std'],
            'packet length variance': ['pkt len var', 'packet length variance'],
            'fin flag count': ['fin flag cnt', 'fin flag count'],
            'syn flag count': ['syn flag cnt', 'syn flag count'],
            'rst flag count': ['rst flag cnt', 'rst flag count'],
            'psh flag count': ['psh flag cnt', 'psh flag count'],
            'ack flag count': ['ack flag cnt', 'ack flag count'],
            'urg flag count': ['urg flag cnt', 'urg flag count'],
            'cwr flag count': ['cwe flag count', 'cwr flag count', 'cwr flag cnt'],
            'ece flag count': ['ece flag cnt', 'ece flag count'],
            'down/up ratio': ['down/up ratio'],
            'average packet size': ['pkt size avg', 'average packet size'],
            'fwd segment size avg': ['fwd seg size avg', 'fwd segment size avg'],
            'bwd segment size avg': ['bwd seg size avg', 'bwd segment size avg'],
            'fwd bytes/bulk avg': ['fwd byts/b avg', 'fwd bytes/bulk avg'],
            'fwd packet/bulk avg': ['fwd pkts/b avg', 'fwd packet/bulk avg', 'fwd packets/bulk avg'],
            'fwd bulk rate avg': ['fwd blk rate avg', 'fwd bulk rate avg'],
            'bwd bytes/bulk avg': ['bwd byts/b avg', 'bwd bytes/bulk avg'],
            'bwd packet/bulk avg': ['bwd pkts/b avg', 'bwd packet/bulk avg', 'bwd packets/bulk avg'],
            'bwd bulk rate avg': ['bwd blk rate avg', 'bwd bulk rate avg'],
            'subflow fwd packets': ['subflow fwd pkts', 'subflow fwd packets'],
            'subflow fwd bytes': ['subflow fwd byts', 'subflow fwd bytes'],
            'subflow bwd packets': ['subflow bwd pkts', 'subflow bwd packets'],
            'subflow bwd bytes': ['subflow bwd byts', 'subflow bwd bytes'],
            'fwd init win bytes': ['init fwd win byts', 'fwd init win bytes', 'init_win_bytes_forward'],
            'bwd init win bytes': ['init bwd win byts', 'bwd init win bytes', 'init_win_bytes_backward'],
            'fwd act data pkts': ['fwd act data pkts', 'act_data_pkt_fwd'],
            'fwd seg size min': ['fwd seg size min', 'min_seg_size_forward'],
            'active min': ['active min'],
            'active mean': ['active mean'],
            'active max': ['active max'],
            'active std': ['active std'],
            'idle min': ['idle min'],
            'idle mean': ['idle mean'],
            'idle max': ['idle max'],
            'idle std': ['idle std'],
        }

        cols_map = {str(c).lower().strip(): c for c in available_columns}
        matched = []
        for feat in self.raw:
            f_key = feat.lower().strip()
            if f_key in cols_map:
                matched.append(cols_map[f_key])
            else:
                candidates = alias_candidates.get(f_key, [])
                found = False
                for cand in candidates:
                    if cand in cols_map:
                        matched.append(cols_map[cand])
                        found = True
                        break
                if not found:
                    raise KeyError(f"Feature '{feat}' não encontrada nas colunas fornecidas.")
        return matched

    def align_features(
        self,
        source_df: Any,
        target_columns: list[str],
        fill_missing: bool = False,
        default_value: float = 0.0,
    ) -> Any:
        """
        Alinha e reordena as colunas de um DataFrame de features para corresponder
        estritamente à lista de colunas esperadas por um modelo ou pré-processador.

        Suporta variações de maiúsculas/minúsculas, espaços, abreviações bidirecionais
        (CSE-CIC-IDS2018 <-> CICFlowMeter canônico) e preenchimento opcional de colunas ausentes.

        Args:
            source_df: DataFrame contendo as features brutas extraídas.
            target_columns: Lista ordenada dos nomes de colunas exigidos pelo modelo.
            fill_missing: Se True, preenche colunas ausentes com default_value em vez de lançar KeyError.
            default_value: Valor padrão para colunas ausentes quando fill_missing=True.

        Returns:
            DataFrame com exatamente as colunas de target_columns na ordem correta.

        Raises:
            KeyError: Se alguma coluna obrigatória de target_columns não for encontrada e fill_missing=False.
        """
        import numpy as np
        import pandas as pd

        cols_map = {str(c).lower().strip(): c for c in source_df.columns}
        selected_series = {}

        # Mapeamento de sinonímias bidirecionais (CSE-CIC-IDS2018 <-> CICFlowMeter canônico)
        synonyms_groups = [
            ("flow duration",),
            ("tot fwd pkts", "total fwd packet", "total fwd packets"),
            ("tot bwd pkts", "total bwd packets", "total bwd packet"),
            ("totlen fwd pkts", "total length of fwd packet"),
            ("totlen bwd pkts", "total length of bwd packet"),
            ("fwd pkt len min", "fwd packet length min"),
            ("fwd pkt len max", "fwd packet length max"),
            ("fwd pkt len mean", "fwd packet length mean"),
            ("fwd pkt len std", "fwd packet length std"),
            ("bwd pkt len min", "bwd packet length min"),
            ("bwd pkt len max", "bwd packet length max"),
            ("bwd pkt len mean", "bwd packet length mean"),
            ("bwd pkt len std", "bwd packet length std"),
            ("flow byts/s", "flow bytes/s"),
            ("flow pkts/s", "flow packets/s"),
            ("flow iat mean",),
            ("flow iat std",),
            ("flow iat max",),
            ("flow iat min",),
            ("fwd iat tot", "fwd iat total"),
            ("fwd iat min",),
            ("fwd iat max",),
            ("fwd iat mean",),
            ("fwd iat std",),
            ("bwd iat tot", "bwd iat total"),
            ("bwd iat min",),
            ("bwd iat max",),
            ("bwd iat mean",),
            ("bwd iat std",),
            ("fwd psh flags",),
            ("bwd psh flags",),
            ("fwd urg flags",),
            ("bwd urg flags",),
            ("fwd header len", "fwd header length"),
            ("bwd header len", "bwd header length"),
            ("fwd pkts/s", "fwd packets/s"),
            ("bwd pkts/s", "bwd packets/s"),
            ("pkt len min", "packet length min"),
            ("pkt len max", "packet length max"),
            ("pkt len mean", "packet length mean"),
            ("pkt len std", "packet length std"),
            ("pkt len var", "packet length variance"),
            ("fin flag cnt", "fin flag count"),
            ("syn flag cnt", "syn flag count"),
            ("rst flag cnt", "rst flag count"),
            ("psh flag cnt", "psh flag count"),
            ("ack flag cnt", "ack flag count"),
            ("urg flag cnt", "urg flag count"),
            ("cwe flag count", "cwr flag count", "cwr flag cnt"),
            ("ece flag cnt", "ece flag count"),
            ("down/up ratio",),
            ("pkt size avg", "average packet size"),
            ("fwd segment size avg", "fwd seg size avg"),
            ("bwd segment size avg", "bwd seg size avg"),
            ("fwd bytes/bulk avg",),
            ("fwd packet/bulk avg",),
            ("fwd bulk rate avg",),
            ("bwd bytes/bulk avg",),
            ("bwd packet/bulk avg",),
            ("bwd bulk rate avg",),
            ("subflow fwd packets",),
            ("subflow fwd bytes",),
            ("subflow bwd packets",),
            ("subflow bwd bytes",),
            ("init fwd win byts", "fwd init win bytes", "init_win_bytes_forward"),
            ("init bwd win byts", "bwd init win bytes", "init_win_bytes_backward"),
            ("fwd act data pkts",),
            ("fwd seg size min",),
            ("active min",),
            ("active mean",),
            ("active max",),
            ("active std",),
            ("idle min",),
            ("idle mean",),
            ("idle max",),
            ("idle std",),
        ]

        alias_map = {}
        for group in synonyms_groups:
            for item in group:
                alias_map[item] = [x for x in group if x != item]

        for target in target_columns:
            t_key = target.lower().strip()
            if t_key in cols_map:
                selected_series[target] = source_df[cols_map[t_key]].values
            else:
                candidates = alias_map.get(t_key, [])
                found = False
                for cand in candidates:
                    cand_clean = cand.lower().strip()
                    if cand_clean in cols_map:
                        selected_series[target] = source_df[cols_map[cand_clean]].values
                        found = True
                        break
                if not found:
                    if fill_missing:
                        selected_series[target] = np.full(len(source_df), default_value, dtype=np.float64)
                    else:
                        raise KeyError(f"Feature obrigatória '{target}' não encontrada no DataFrame de entrada.")

        return pd.DataFrame(selected_series, index=source_df.index)
