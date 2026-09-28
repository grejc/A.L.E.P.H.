"""
Pipeline Unificado e Robusto de Pré-processamento para ALF-MoE.

Garante integridade matemática rigorosa para o NIDS:
- Alinhamento determinístico com as 76 features canônicas do CICDomainFeatures
- Sanitização numérica de infinitos e NaNs com integridade dimensional
- Detecção e aplicação de transformação log1p em features com assimetria (|skew| > 3.0)
- Escalonamento via RobustScaler ajustado estritamente no conjunto de treino
- Divisão estratificada (Treino / Validação / Teste) sem data leakage
- Persistência atômica de artefatos (.pkl e .json) para auditoria e inferência
"""

import os
import sys
import json
import pickle
import tempfile
import warnings
from pathlib import Path
from datetime import datetime
from typing import Tuple, List, Union, Optional, Dict, Any, Literal

import numpy as np
import pandas as pd
from sklearn.preprocessing import RobustScaler, LabelEncoder
from sklearn.model_selection import train_test_split

from domain_features import CICDomainFeatures

warnings.filterwarnings("ignore", category=RuntimeWarning)


def _runtime_audit() -> Dict[str, str]:
    """Coleta metadados sobre o ambiente de execução no momento do fit/save."""
    import sklearn
    return {
        "generated_at": datetime.now().isoformat() + "Z",
        "sklearn_version": sklearn.__version__,
        "numpy_version": np.__version__,
        "pandas_version": pd.__version__,
        "python_version": sys.version.split()[0],
    }


class Preprocessor:
    """
    Pipeline unificado de pré-processamento para detecção de intrusão com ALF-MoE.

    Suporta datasets da família CIC:
        - CSECICIDS2018_improved (.parquet ou .csv)
        - CSE-CIC-IDS2018 (AWS Network Traffic)
        - CIC-UNSW-NB15
        - CIC-BCCC-NRC-2024
    """

    EXPLICIT_DROP_COLUMNS: List[str] = ["Fwd URG Flags", "Bwd URG Flags", "URG Flag Count"]

    def __init__(
        self,
        dataset: str = "CSECICIDS2018_improved",
        load_sampled: bool = True,
        train_val_size: float = 0.8,
        val_size: float = 0.2,
        test_size: float = 0.2,
        random_state: int = 42,
        skew_threshold: float = 3.0,
        threat_level: Literal[0, 1, 2] = 2,
        artifacts_dir: Optional[Union[str, Path]] = None,
        base_path: Optional[Union[str, Path]] = None,
        dataset_path: Optional[Union[str, Path]] = None,
        auto_load: bool = False,
    ) -> None:
        self.dataset_name = dataset
        self.load_sampled = load_sampled
        self.train_val_size = train_val_size
        self.val_size = val_size
        self.test_size = test_size
        self.random_state = random_state
        self.skew_threshold = skew_threshold
        self.threat_level = threat_level
        self._threat_level_used: Optional[int] = threat_level

        if not np.isclose(train_val_size + test_size, 1.0):
            raise ValueError("A soma de train_val_size e test_size deve ser igual a 1.0.")
        if not (0.0 < val_size < 1.0):
            raise ValueError("val_size deve estar no intervalo (0, 1).")

        suffix = "_sampled.csv" if load_sampled else ".csv"
        if base_path:
            self.base_path = Path(base_path)
        elif "DATASETS_DIR" in os.environ:
            self.base_path = Path(os.environ["DATASETS_DIR"])
        elif Path("/run/media/null/VM_s/DATASETS").exists():
            self.base_path = Path("/run/media/null/VM_s/DATASETS")
        else:
            self.base_path = Path("./data")

        if dataset_path:
            self.dataset_path = Path(dataset_path)
        else:
            clean_name = dataset[:-8] if dataset.endswith(".parquet") else (
                dataset[:-4] if dataset.endswith(".csv") else dataset
            )
            cand_paths = []
            if load_sampled:
                cand_paths.extend([
                    self.base_path / f"{clean_name}_sampled.parquet",
                    self.base_path / f"{clean_name}_sampled.csv",
                ])
            if dataset.endswith(".parquet") or dataset.endswith(".csv"):
                cand_paths.append(self.base_path / dataset)
            cand_paths.extend([
                self.base_path / f"{clean_name}.parquet",
                self.base_path / f"{clean_name}.csv",
                self.base_path / f"{clean_name}{suffix}",
            ])
            chosen_path = None
            for p in cand_paths:
                if p.exists():
                    chosen_path = p
                    break
            self.dataset_path = chosen_path if chosen_path is not None else cand_paths[0]

        if artifacts_dir:
            self.artifacts_dir = Path(artifacts_dir)
        elif "ARTIFACTS_DIR" in os.environ:
            self.artifacts_dir = Path(os.environ["ARTIFACTS_DIR"]) / dataset
        elif Path("./artifacts").exists():
            self.artifacts_dir = Path("./artifacts") / dataset
        else:
            self.artifacts_dir = Path("./artifacts") / dataset
        try:
            self.artifacts_dir.mkdir(parents=True, exist_ok=True)
        except Exception:
            self.artifacts_dir = Path("./artifacts") / dataset
            self.artifacts_dir.mkdir(parents=True, exist_ok=True)

        self.domain_utility = CICDomainFeatures()
        # Features canônicas sem as colunas sem variância removidas explicitamente
        self.canonical_features: List[str] = [
            f for f in self.domain_utility.raw if f not in self.EXPLICIT_DROP_COLUMNS
        ]

        # Estado interno do preprocessor
        self.scaler: Optional[RobustScaler] = None
        self.label_encoder: Optional[LabelEncoder] = None
        self.feature_names: List[str] = list(self.canonical_features)
        self.log1p_features: List[str] = []
        self.feature_medians_: Dict[str, float] = {}
        self.dropped_variance_columns: List[str] = list(self.EXPLICIT_DROP_COLUMNS)
        self._target_column: Optional[str] = None
        self._is_fitted: bool = False
        self._fit_audit: Optional[Dict[str, Any]] = None
        self.class_weights: Optional[Dict[int, float]] = None

        self.dataset: Optional[pd.DataFrame] = self.load_dataset() if auto_load else None

    @property
    def target_column(self) -> str:
        if self._target_column is not None:
            return self._target_column
        if self.dataset_name == "CIC-BCCC-NRC-2024":
            return "Attack Name"
        return "Label"

    @target_column.setter
    def target_column(self, val: str) -> None:
        self._target_column = val

    @property
    def n_features(self) -> int:
        return len(self.feature_names)

    @property
    def n_classes(self) -> int:
        if self.label_encoder is not None:
            return len(self.label_encoder.classes_)
        return 0

    @property
    def classes(self) -> List[str]:
        if self.label_encoder is not None:
            return [str(c) for c in self.label_encoder.classes_]
        return []

    def threat_classification(self, level: Literal[0, 1, 2] = 2) -> Dict[str, str]:
        """
        Retorna o mapeamento hierárquico das classes de ataque.
        level=0: Classes brutas/granulares originais do dataset.
        level=1: Famílias intermediárias de ataque.
        level=2: Meta-categorias consolidadas.
        """
        ds = self.dataset_name
        is_improved = "improved" in ds or ds in ("CSECICIDS2018_improved", "CSECICIDS2018_improved.parquet")

        if is_improved:
            if level == 0:
                attacks = [
                    'BENIGN', 'DoS Hulk', 'Botnet Ares', 'DDoS-HOIC', 'SSH-BruteForce',
                    'Infiltration - NMAP Portscan', 'DDoS-LOIC-HTTP', 'DoS GoldenEye',
                    'DoS Slowloris', 'DDoS-LOIC-UDP', 'Infiltration - Communication Victim Attacker',
                    'Web Attack - Brute Force', 'Web Attack - XSS', 'Infiltration - Dropbox Download',
                    'Web Attack - SQL'
                ]
                return {a: a for a in attacks}
            elif level == 1:
                return {
                    'BENIGN':                                       'BENIGN',
                    'DoS Hulk':                                     'DoS-Hulk',
                    'Botnet Ares':                                  'Botnet',
                    'DDoS-HOIC':                                    'DDoS-HOIC',
                    'SSH-BruteForce':                               'SSH-BruteForce',
                    'Infiltration - NMAP Portscan':                 'Infiltration - NMAP Portscan',
                    'DDoS-LOIC-HTTP':                               'DDoS-LOIC-HTTP',
                    'DoS GoldenEye':                                'DoS-GoldenEye',
                    'DoS Slowloris':                                'DoS-Slowloris',
                    'DDoS-LOIC-UDP':                                'DDoS-LOIC-UDP',
                    'Infiltration - Communication Victim Attacker': 'Infiltration - Communication Victim Attacker',
                    'Web Attack - Brute Force':                     'WebAttack-BruteForce',
                    'Web Attack - XSS':                             'WebAttack-XSS',
                    'Infiltration - Dropbox Download':              'Infiltration - Dropbox Download',
                    'Web Attack - SQL':                             'WebAttack-SQL_Injection',
                }
            else:
                return {
                    # 1. BENIGN
                    'BENIGN':                                       'BENIGN',
                    'Benign':                                       'BENIGN',
                    # 2. Botnet
                    'Botnet Ares':                                  'Botnet',
                    'Bot':                                          'Botnet',
                    # 3. SSH-BruteForce
                    'SSH-BruteForce':                               'SSH-BruteForce',
                    'SSH-Bruteforce':                               'SSH-BruteForce',
                    # 4. DoS (agrupando DoS Hulk, Slowloris, SlowHTTPTest, GoldenEye, etc.)
                    'DoS Hulk':                                     'DoS',
                    'DoS GoldenEye':                                'DoS',
                    'DoS Slowloris':                                'DoS',
                    'DoS SlowHTTPTest':                             'DoS',
                    'DoS attacks-Hulk':                             'DoS',
                    'DoS attacks-GoldenEye':                        'DoS',
                    'DoS attacks-Slowloris':                        'DoS',
                    'DoS attacks-SlowHTTPTest':                     'DoS',
                    # 5. DDoS (agrupando DDoS LOIC-HTTP, LOIC-UDP, HOIC, etc.)
                    'DDoS-HOIC':                                    'DDoS',
                    'DDoS-LOIC-HTTP':                               'DDoS',
                    'DDoS-LOIC-UDP':                                'DDoS',
                    'DDOS attack-HOIC':                             'DDoS',
                    'DDoS attacks-LOIC-HTTP':                       'DDoS',
                    'DDOS attack-LOIC-UDP':                         'DDoS',
                    # 6. Web Attack (agrupando Brute Force Web, XSS, SQL Injection, etc.)
                    'Web Attack - Brute Force':                     'Web Attack',
                    'Web Attack - XSS':                             'Web Attack',
                    'Web Attack - SQL':                             'Web Attack',
                    'Brute Force -Web':                             'Web Attack',
                    'Brute Force -XSS':                             'Web Attack',
                    'SQL Injection':                                'Web Attack',
                    # 7, 8, 9... (mantendo as variações de Infiltração individualizadas conforme o dataset)
                    'Infiltration - NMAP Portscan':                 'Infiltration - NMAP Portscan',
                    'Infiltration - Communication Victim Attacker': 'Infiltration - Communication Victim Attacker',
                    'Infiltration - Dropbox Download':              'Infiltration - Dropbox Download',
                    'Infilteration':                                'Infiltration',
                }

        elif self.dataset_name == "CSE-CIC-IDS2018":
            if level == 0:
                attacks = [
                    'Benign', 'DDOS attack-HOIC', 'DDoS attacks-LOIC-HTTP', 'DDOS attack-LOIC-UDP',
                    'DoS attacks-Hulk', 'DoS attacks-SlowHTTPTest', 'DoS attacks-GoldenEye',
                    'DoS attacks-Slowloris', 'Bot', 'FTP-BruteForce', 'SSH-Bruteforce',
                    'Infilteration', 'Brute Force -Web', 'Brute Force -XSS', 'SQL Injection'
                ]
                return {a: a for a in attacks}
            elif level == 1:
                return {
                    'Benign': 'Benign',
                    'DDOS attack-HOIC': 'DDoS-HOIC',
                    'DDoS attacks-LOIC-HTTP': 'DDoS-LOIC-HTTP',
                    'DDOS attack-LOIC-UDP': 'DDoS-LOIC-UDP',
                    'DoS attacks-Hulk': 'DoS-Hulk',
                    'DoS attacks-SlowHTTPTest': 'DoS-SlowHTTPTest',
                    'DoS attacks-GoldenEye': 'DoS-GoldenEye',
                    'DoS attacks-Slowloris': 'DoS-Slowloris',
                    'Bot': 'Botnet',
                    'FTP-BruteForce': 'BruteForce-FTP',
                    'SSH-Bruteforce': 'BruteForce-SSH',
                    'Infilteration': 'Infiltration',
                    'Brute Force -Web': 'WebAttack-BruteForce_Web',
                    'Brute Force -XSS': 'WebAttack-BruteForce_XSS',
                    'SQL Injection': 'WebAttack-SQL_Injection',
                }
            else:
                return {
                    'Benign': 'Benign',
                    'DDOS attack-HOIC': 'DDoS',
                    'DDoS attacks-LOIC-HTTP': 'DDoS',
                    'DDOS attack-LOIC-UDP': 'DDoS',
                    'DoS attacks-Hulk': 'DoS',
                    'DoS attacks-SlowHTTPTest': 'DoS',
                    'DoS attacks-GoldenEye': 'DoS',
                    'DoS attacks-Slowloris': 'DoS',
                    'Bot': 'Botnet',
                    'FTP-BruteForce': 'BruteForce',
                    'SSH-Bruteforce': 'BruteForce',
                    'Infilteration': 'Infiltration',
                    'Brute Force -Web': 'WebAttack',
                    'Brute Force -XSS': 'WebAttack',
                    'SQL Injection': 'WebAttack',
                }

        elif self.dataset_name == "CIC-UNSW-NB15":
            classes = ['Benign', 'Exploits', 'Fuzzers', 'Reconnaissance', 'Generic', 'DoS', 'Shellcode', 'Backdoor', 'Analysis', 'Worms']
            return {c: c for c in classes}

        elif self.dataset_name == "CIC-BCCC-NRC-2024":
            if level == 0:
                return {
                    'Benign Traffic': 'Benign Traffic',
                    'DDoS RSTFIN Flood': 'DDoS RSTFIN Flood',
                    'DDoS PSHACK Flood': 'DDoS PSHACK Flood',
                    'DDoS ACK Fragmentation': 'DDoS ACK Fragmentation',
                    'DDoS TCP SYN Flood': 'DDoS TCP SYN Flood',
                    'DDoS HTTP Flood': 'DDoS HTTP Flood',
                    'DDoS ICMP Fragmentation': 'DDoS ICMP Fragmentation',
                    'DDoS UDP Flood': 'DDoS UDP Flood',
                    'DDoS ICMP Flood': 'DDoS ICMP Flood',
                    'ACK Flood': 'ACK Flood',
                    'DoS TCP Flood': 'DoS TCP Flood',
                    'DoS SYN Flood': 'DoS SYN Flood',
                    'DoS UDP Flood': 'DoS UDP Flood',
                    'DoS ICMP Flood': 'DoS ICMP Flood',
                    'DoS DNS Flood': 'DoS DNS Flood',
                    'SYN Flood': 'SYN Flood',
                    'Sparta SSH Brute Force': 'Sparta SSH Brute Force',
                    'MQTT Brute Force': 'MQTT Brute Force',
                    'Recon Port Scan': 'Recon Port Scan',
                    'XSS': 'XSS',
                    'Backdoor': 'Backdoor',
                    'MQTT DDoS Publish Flood': 'MQTT DDoS Publish Flood',
                    'MQTT DoS Connect Flood': 'MQTT DoS Connect Flood',
                    'Password Attack': 'Password Attack',
                    'Recon OS Scan': 'Recon OS Scan',
                    'MITM': 'MITM',
                    'Recon Vulnerability Scan': 'Recon Vulnerability Scan',
                    'Recon Ping Sweep': 'Recon Ping Sweep',
                    'Scan Aggressive': 'Scan Aggressive',
                    'Dictionary Brute Force': 'Dictionary Brute Force',
                    'MITM ARP Spoofing': 'MITM ARP Spoofing',
                    'Ransomware': 'Ransomware',
                    'Scan UDP Attack': 'Scan UDP Attack',
                    'Mirai ACK Flood': 'Mirai ACK Flood',
                    'Port Scanning': 'Port Scanning',
                    'Scan Port OS': 'Scan Port OS',
                    'Uploading Attack': 'Uploading Attack',
                    'SQL Injection': 'SQL Injection',
                    'Scan Host Port': 'Scan Host Port',
                    'Vulnerability Scanner': 'Vulnerability Scanner',
                    'Mirai HTTP Flood': 'Mirai HTTP Flood',
                    'Mirai Host Brute Force': 'Mirai Host Brute Force',
                    'MQTT Malformed': 'MQTT Malformed',
                    'Mirai UDP Plain': 'Mirai UDP Plain',
                    'Mirai UDP Flood': 'Mirai UDP Flood',
                    'MQTT DoS Publish Flood': 'MQTT DoS Publish Flood',
                    'Telnet Brute Force': 'Telnet Brute Force',
                    'Recon Host Discovery': 'Recon Host Discovery',
                    'OS Fingerprinting': 'OS Fingerprinting',
                }
            elif level == 1:
                return {
                    'Benign Traffic':               'Benign Traffic',
                    'DDoS RSTFIN Flood':            'Volumetric Flooding',
                    'DDoS PSHACK Flood':            'TCP State Flooding',
                    'DDoS ACK Fragmentation':       'Fragmented Flooding',
                    'DDoS TCP SYN Flood':           'Volumetric Distributed DoS',
                    'DDoS HTTP Flood':              'Layer-7 Web Flooding',
                    'DDoS ICMP Fragmentation':      'ICMP Fragment Attack',
                    'DDoS UDP Flood':               'Distributed UDP Flood',
                    'DDoS ICMP Flood':              'Distributed ICMP Flood',
                    'ACK Flood':                    'TCP State Flooding',
                    'DoS TCP Flood':                'Volumetric DoS',
                    'DoS SYN Flood':                'Volumetric DoS',
                    'DoS UDP Flood':                'UDP Flooding',
                    'DoS ICMP Flood':               'ICMP Flooding',
                    'DoS DNS Flood':                'DNS Amplification/Flood',
                    'SYN Flood':                    'Connection State Exhaustion',
                    'Sparta SSH Brute Force':       'Credential Brute Force',
                    'MQTT Brute Force':             'IoT Protocol Attack',
                    'Recon Port Scan':              'Reconnaissance / Discovery',
                    'XSS':                          'Web Application Attack',
                    'Backdoor':                     'Persistent Malware',
                    'MQTT DDoS Publish Flood':      'IoT Application Flooding',
                    'MQTT DoS Connect Flood':       'IoT Session Flooding',
                    'Password Attack':              'Authentication Brute Force',
                    'Recon OS Scan':                'Reconnaissance / Fingerprinting',
                    'MITM':                         'Man-in-the-Middle',
                    'Recon Vulnerability Scan':     'Vulnerability Assessment',
                    'Recon Ping Sweep':             'Host Probing',
                    'Scan Aggressive':              'Active Scanning',
                    'Dictionary Brute Force':       'Credential Attack',
                    'MITM ARP Spoofing':            'Layer-2 Poisoning',
                    'Ransomware':                   'Malware Payload',
                    'Scan UDP Attack':              'UDP Port Scanning',
                    'Mirai ACK Flood':              'IoT Botnet Flooding',
                    'Port Scanning':                'Service Probing',
                    'Scan Port OS':                 'Service & OS Probing',
                    'Uploading Attack':             'Web Exploit / Shell Upload',
                    'SQL Injection':                'Database Injection',
                    'Scan Host Port':               'Host/Port Scanning',
                    'Vulnerability Scanner':        'Automated Tool Probe',
                    'Mirai HTTP Flood':             'Botnet Layer-7 Flood',
                    'Mirai Host Brute Force':       'Botnet Propagation',
                    'MQTT Malformed':               'Protocol Fuzzing / Exploit',
                    'Mirai UDP Plain':              'Botnet UDP Flooding',
                    'Mirai UDP Flood':              'Botnet UDP Flooding',
                    'MQTT DoS Publish Flood':       'IoT Broker Flooding',
                    'Telnet Brute Force':           'Legacy Protocol Attack',
                    'Recon Host Discovery':         'Network Mapping',
                    'OS Fingerprinting':            'Active TCP Fingerprinting',
                }
            else:
                return {
                    'Benign Traffic':               'Benign Traffic',
                    'Backdoor':                     'Botnet/Malware',
                    'Ransomware':                   'Botnet/Malware',
                    'Mirai ACK Flood':              'Botnet/Malware',
                    'Mirai HTTP Flood':             'Botnet/Malware',
                    'Mirai Host Brute Force':       'Botnet/Malware',
                    'Mirai UDP Plain':              'Botnet/Malware',
                    'Mirai UDP Flood':              'Botnet/Malware',
                    'Sparta SSH Brute Force':       'BruteForce',
                    'Password Attack':              'BruteForce',
                    'Dictionary Brute Force':       'BruteForce',
                    'Telnet Brute Force':           'BruteForce',
                    'DDoS RSTFIN Flood':            'DDoS',
                    'DDoS PSHACK Flood':            'DDoS',
                    'DDoS ACK Fragmentation':       'DDoS',
                    'DDoS TCP SYN Flood':           'DDoS',
                    'DDoS HTTP Flood':              'DDoS',
                    'DDoS ICMP Fragmentation':      'DDoS',
                    'DDoS UDP Flood':               'DDoS',
                    'DDoS ICMP Flood':              'DDoS',
                    'ACK Flood':                    'DoS',
                    'DoS TCP Flood':                'DoS',
                    'DoS SYN Flood':                'DoS',
                    'DoS UDP Flood':                'DoS',
                    'DoS ICMP Flood':               'DoS',
                    'DoS DNS Flood':                'DoS',
                    'SYN Flood':                    'DoS',
                    'MQTT Brute Force':             'IoT/MQTT',
                    'MQTT DDoS Publish Flood':      'IoT/MQTT',
                    'MQTT DoS Connect Flood':       'IoT/MQTT',
                    'MQTT Malformed':               'IoT/MQTT',
                    'MQTT DoS Publish Flood':       'IoT/MQTT',
                    'MITM':                         'MITM',
                    'MITM ARP Spoofing':            'MITM',
                    'Recon OS Scan':                'Reconnaissance',
                    'Recon Vulnerability Scan':     'Reconnaissance',
                    'Recon Ping Sweep':             'Reconnaissance',
                    'Scan Aggressive':              'Reconnaissance',
                    'Recon Port Scan':              'Reconnaissance',
                    'Scan UDP Attack':              'Reconnaissance',
                    'Port Scanning':                'Reconnaissance',
                    'Scan Port OS':                 'Reconnaissance',
                    'Scan Host Port':               'Reconnaissance',
                    'Vulnerability Scanner':        'Reconnaissance',
                    'Recon Host Discovery':         'Reconnaissance',
                    'OS Fingerprinting':            'Reconnaissance',
                    'Uploading Attack':             'WebAttack',
                    'SQL Injection':                'WebAttack',
                    'XSS':                          'WebAttack',
                }
        else:
            return {}

    def _align_dataframe_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Alinha qualquer DataFrame bruto com as features canônicas e a coluna alvo."""
        target_col_found = None
        for cand in [self.target_column, "Label", "label", "Attack Name", "attack_name"]:
            if cand in df.columns:
                target_col_found = cand
                break

        feature_cols_in_df = [c for c in df.columns if c != target_col_found]
        missing_canonical = [c for c in self.domain_utility.raw if c not in df.columns]
        if missing_canonical and len(feature_cols_in_df) >= len(self.domain_utility.raw):
            try:
                matched_cols = self.domain_utility.match_columns(feature_cols_in_df)
                rename_map = {orig: canon for orig, canon in zip(matched_cols, self.domain_utility.raw)}
                cols_to_keep = matched_cols + ([target_col_found] if target_col_found else [])
                df = df[cols_to_keep].copy()
                df.rename(columns=rename_map, inplace=True)
            except Exception as e:
                print(f"[Preprocessor] Aviso no alinhamento de colunas: {e}")

        # Remove explicitamente colunas sem variância
        to_drop = [c for c in self.EXPLICIT_DROP_COLUMNS if c in df.columns]
        if to_drop:
            df = df.drop(columns=to_drop)

        if target_col_found and target_col_found != self.target_column:
            df.rename(columns={target_col_found: self.target_column}, inplace=True)

        return df

    def load_dataset(self) -> pd.DataFrame:
        """
        Carrega o arquivo do dataset (.parquet ou .csv), alinha as colunas com os nomes canônicos
        e descarta atributos irrelevantes ou de variância zero.
        """
        if not self.dataset_path.exists():
            raise FileNotFoundError(f"Arquivo do dataset não encontrado em: {self.dataset_path}")

        print(f"[Preprocessor] Carregando dataset a partir de: {self.dataset_path}...")
        if str(self.dataset_path).endswith(".parquet"):
            df_raw = pd.read_parquet(self.dataset_path)
        else:
            df_raw = pd.read_csv(self.dataset_path, low_memory=False)
        return self._clean_raw_dataset(df_raw)

    def _clean_raw_dataset(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Executa sanitização preliminar do DataFrame bruto:
        - Alinha colunas canônicas
        - Remove colunas sem variância (explicitamente: Fwd URG Flags, Bwd URG Flags, URG Flag Count e outras de variância zero)
        - Substitui infinitos por NaNs
        - Imputa NaNs pela mediana condicional por classe (com fallback para mediana global)
        - Converte colunas de atributos para float32
        - Remove instâncias com rótulo nulo
        """
        df = self._align_dataframe_columns(df)
        target = self.target_column
        if target in df.columns:
            df = df.dropna(subset=[target])

        # Detecção e remoção de colunas adicionais sem variância (apenas se houver amostras suficientes)
        if len(df) >= 100:
            zero_var_detected = []
            for col in list(self.canonical_features):
                if col in df.columns:
                    s_clean = pd.to_numeric(df[col], errors="coerce").replace([np.inf, -np.inf], np.nan)
                    if s_clean.nunique(dropna=True) <= 1:
                        zero_var_detected.append(col)

            if zero_var_detected:
                print(f"[Preprocessor] Removendo colunas adicionais sem variância detectadas: {zero_var_detected}")
                df.drop(columns=zero_var_detected, inplace=True, errors="ignore")
                for c in zero_var_detected:
                    if c not in self.dropped_variance_columns:
                        self.dropped_variance_columns.append(c)
                self.canonical_features = [c for c in self.canonical_features if c not in zero_var_detected]
                self.feature_names = list(self.canonical_features)

        # Sanitiza atributos numéricos e trata infinitos / NaNs via mediana condicional
        has_target = target in df.columns
        for col in self.canonical_features:
            if col in df.columns:
                s = pd.to_numeric(df[col], errors="coerce")
                s = s.replace([np.inf, -np.inf], np.nan)

                if s.isna().any():
                    if has_target:
                        median_cond = df.groupby(target)[col].transform("median")
                        s = s.fillna(median_cond)
                    global_med = s.median()
                    if pd.isna(global_med):
                        global_med = 0.0
                    s = s.fillna(global_med)
                    self.feature_medians_[col] = float(global_med)
                else:
                    med = s.median()
                    self.feature_medians_[col] = 0.0 if pd.isna(med) else float(med)

                df[col] = s.astype(np.float32)

        return df

    def _sanitize_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Sanitização garantindo que todas as features canônicas existam e sejam finitas."""
        df = df.copy()
        target = self.target_column if self.target_column in df.columns else None

        for col in self.canonical_features:
            if col not in df.columns:
                df[col] = np.float32(self.feature_medians_.get(col, 0.0))
            else:
                s = pd.to_numeric(df[col], errors="coerce").replace([np.inf, -np.inf], np.nan)
                if s.isna().any():
                    if target is not None:
                        median_cond = df.groupby(target)[col].transform("median")
                        s = s.fillna(median_cond)
                    fallback = self.feature_medians_.get(col, s.median())
                    if pd.isna(fallback):
                        fallback = 0.0
                    s = s.fillna(fallback)
                df[col] = s.astype(np.float32)
        return df

    def _select_log1p_features(self, df: pd.DataFrame) -> List[str]:
        """Identifica features com assimetria acentuada (|skew| > threshold) e min >= 0."""
        candidates = []
        for col in self.canonical_features:
            if col in df.columns:
                s = df[col].dropna()
                if len(s) > 0 and s.min() >= 0:
                    skew_val = float(s.skew())
                    if abs(skew_val) > self.skew_threshold:
                        candidates.append(col)
        return candidates

    def _apply_log1p(self, df: pd.DataFrame) -> pd.DataFrame:
        """Aplica log1p com proteção não-negativa às colunas selecionadas."""
        if not self.log1p_features:
            return df
        df = df.copy()
        for col in self.log1p_features:
            if col in df.columns:
                df[col] = np.log1p(np.maximum(df[col].to_numpy(dtype=np.float64), 0.0)).astype(np.float32)
        return df

    def compute_class_weights(
        self,
        y: np.ndarray,
        strategy: Literal["none", "sqrt", "balanced"] = "sqrt",
    ) -> Optional[Dict[int, float]]:
        """
        Calcula pesos balanceados de classes para a Focal Loss:
        - strategy='sqrt': w_c = sqrt(N / (C * N_c)), atenuando extremos
        - strategy='balanced': w_c = N / (C * N_c)
        """
        if strategy == "none":
            return None

        classes, counts = np.unique(y, return_counts=True)
        total_samples = len(y)
        n_classes = len(classes)

        weights = {}
        for c, count in zip(classes, counts):
            if strategy == "sqrt":
                w = np.sqrt(total_samples / (n_classes * float(count)))
            else:
                w = total_samples / (n_classes * float(count))
            weights[int(c)] = float(w)

        return weights

    def get_domain_indices(self) -> Dict[str, List[int]]:
        """
        Retorna os índices das features ativas para cada um dos 5 especialistas neurais,
        garantindo compatibilidade com o fatiamento via SliceLayer mesmo após a remoção
        de colunas sem variância.
        """
        xg, xs, xv, xf, xt, _ = self.domain_utility
        return {
            "dnn": [self.feature_names.index(f) for f in xg if f in self.feature_names],
            "cnn": [self.feature_names.index(f) for f in xs if f in self.feature_names],
            "gru": [self.feature_names.index(f) for f in xv if f in self.feature_names],
            "cae": [self.feature_names.index(f) for f in xf if f in self.feature_names],
            "lstm": [self.feature_names.index(f) for f in xt if f in self.feature_names],
        }

    def fit(self, train_df: pd.DataFrame) -> "Preprocessor":
        """
        Ajusta o preprocessor exclusivamente no conjunto de treino:
        1. Aplica mapeamento de ameaças se threat_level estiver configurado
        2. Identifica features candidatas ao log1p (skewness)
        3. Ajusta RobustScaler
        4. Ajusta LabelEncoder
        5. Calcula class_weights para Focal Loss
        """
        train_df = train_df.copy()
        lvl = self._threat_level_used if self._threat_level_used is not None else self.threat_level
        if lvl is not None and self.target_column in train_df.columns:
            self.threat_level = lvl
            self._threat_level_used = lvl
            mapping = self.threat_classification(level=lvl)
            if mapping:
                train_df[self.target_column] = train_df[self.target_column].map(mapping).fillna(train_df[self.target_column])

        df_clean = self._sanitize_features(train_df)

        # Atualiza medianas de referência calculadas estritamente no treino
        for col in self.canonical_features:
            if col in train_df.columns:
                s = pd.to_numeric(train_df[col], errors="coerce").replace([np.inf, -np.inf], np.nan)
                med = float(s.median())
                self.feature_medians_[col] = 0.0 if np.isnan(med) else med

        # 1. Detecção de skewness
        self.log1p_features = self._select_log1p_features(df_clean)
        df_log = self._apply_log1p(df_clean)

        # 2. Ajuste do RobustScaler
        self.scaler = RobustScaler(quantile_range=(25.0, 75.0))
        X_train_raw = df_log[self.canonical_features].to_numpy(dtype=np.float32)
        self.scaler.fit(X_train_raw)

        # 3. Ajuste do LabelEncoder
        self.label_encoder = LabelEncoder()
        target_series = train_df[self.target_column].astype(str).str.strip()
        y_train_enc = self.label_encoder.fit_transform(target_series)

        # 4. Cálculo de pesos de classe
        self.class_weights = self.compute_class_weights(y_train_enc, strategy="sqrt")

        self.feature_names = list(self.canonical_features)
        self._is_fitted = True
        self._fit_audit = _runtime_audit()

        return self

    def transform(self, df: pd.DataFrame) -> Tuple[np.ndarray, Optional[np.ndarray]]:
        """Transforma um DataFrame aplicando log1p, scaler e encoding do target."""
        if not self._is_fitted or self.scaler is None or self.label_encoder is None:
            raise RuntimeError("Preprocessor não ajustado. Execute fit() primeiro.")

        df = df.copy()
        lvl = self._threat_level_used if self._threat_level_used is not None else self.threat_level
        if lvl is not None and self.target_column in df.columns:
            mapping = self.threat_classification(level=lvl)
            if mapping:
                df[self.target_column] = df[self.target_column].map(mapping).fillna(df[self.target_column])

        df_clean = self._sanitize_features(df)
        df_log = self._apply_log1p(df_clean)

        X = self.scaler.transform(df_log[self.canonical_features].to_numpy(dtype=np.float32)).astype(np.float32)

        y = None
        if self.target_column in df.columns:
            target_series = df[self.target_column].astype(str).str.strip()
            classes_known = set(self.label_encoder.classes_)
            benign_cls = next((c for c in self.label_encoder.classes_ if "benign" in str(c).lower()), self.label_encoder.classes_[0])
            target_safe = target_series.apply(lambda s: s if s in classes_known else benign_cls)
            y = self.label_encoder.transform(target_safe).astype(np.int32)

        return X, y

    def transform_features(self, raw_data: Union[Dict[str, Any], pd.DataFrame, pd.Series]) -> np.ndarray:
        """
        Método de alta performance para inferência em produção.
        Converte registros brutos (dict, Series ou DataFrame) na matriz tabular escalonada (N, D).
        """
        if not self._is_fitted or self.scaler is None:
            raise RuntimeError("Preprocessor não ajustado ou artefatos não carregados.")

        if isinstance(raw_data, dict):
            df = pd.DataFrame([raw_data])
        elif isinstance(raw_data, pd.Series):
            df = pd.DataFrame([raw_data.to_dict()])
        elif isinstance(raw_data, pd.DataFrame):
            df = raw_data.copy()
        else:
            raise TypeError(f"Tipo não suportado em transform_features: {type(raw_data)}")

        # Verifica se as colunas precisam ser mapeadas via match_columns
        missing_canonical = [c for c in self.canonical_features if c not in df.columns]
        if missing_canonical and len(df.columns) >= len(self.canonical_features):
            try:
                matched = self.domain_utility.match_columns(list(df.columns))
                rename_map = {orig: canon for orig, canon in zip(matched, self.domain_utility.raw)}
                df = df[matched].rename(columns=rename_map)
            except Exception:
                pass

        # Remove colunas excluídas
        to_drop = [c for c in self.dropped_variance_columns if c in df.columns]
        if to_drop:
            df = df.drop(columns=to_drop)

        df_clean = self._sanitize_features(df)
        df_log = self._apply_log1p(df_clean)
        X = self.scaler.transform(df_log[self.canonical_features].to_numpy(dtype=np.float32)).astype(np.float32)
        return X

    def generate_train_val_test(
        self,
        stratify: bool = True,
        threat_level: Optional[Literal[0, 1, 2]] = None,
        deduplicate: bool = True,
        refit: bool = False,
    ) -> Tuple[Tuple[np.ndarray, np.ndarray], Tuple[np.ndarray, np.ndarray], Tuple[np.ndarray, np.ndarray]]:
        """
        Gera as partições de treino, validação e teste com divisão estratificada e sem vazamento de dados.
        """
        if self.dataset is None:
            self.dataset = self.load_dataset()

        df = self.dataset.copy()

        # 1. Agrupamento de ameaças
        lvl = threat_level if threat_level is not None else (
            self._threat_level_used if self._threat_level_used is not None else self.threat_level
        )
        if lvl is not None:
            self.threat_level = lvl
            self._threat_level_used = lvl
            mapping = self.threat_classification(level=lvl)
            if mapping:
                df[self.target_column] = df[self.target_column].map(mapping).fillna(df[self.target_column])
                print(f"[Preprocessor] Agrupamento threat_level={lvl} aplicado. Classes ativas ({df[self.target_column].nunique()}): {sorted(df[self.target_column].unique())}")

        # 2. Deduplicação opcional
        if deduplicate:
            initial_count = len(df)
            df = df.drop_duplicates(subset=self.canonical_features)
            print(f"[Preprocessor] Deduplicação: {initial_count - len(df)} linhas redundantes removidas. Restantes: {len(df)}.")

        # 3. Split treino+validação vs teste
        strat = df[self.target_column] if stratify else None
        train_val_df, test_df = train_test_split(
            df,
            train_size=self.train_val_size,
            test_size=self.test_size,
            random_state=self.random_state,
            stratify=strat,
        )

        # 4. Split interno treino vs validação
        strat_tv = train_val_df[self.target_column] if stratify else None
        train_df, val_df = train_test_split(
            train_val_df,
            train_size=1.0 - self.val_size,
            test_size=self.val_size,
            random_state=self.random_state,
            stratify=strat_tv,
        )

        # 5. Fit exclusivamente no treino (prevenção absoluta de data leakage)
        if not self._is_fitted or refit:
            self.fit(train_df)
        else:
            print("[Preprocessor] Pipeline já ajustado (artefatos carregados). Re-fit ignorado para preservar integridade.")

        # 6. Transformação consistente
        X_train, y_train = self.transform(train_df)
        X_val, y_val = self.transform(val_df)
        X_test, y_test = self.transform(test_df)

        print(f"[Preprocessor] Splits gerados com sucesso:")
        print(f"  Treino:    X={X_train.shape}, y={y_train.shape}")
        print(f"  Validação: X={X_val.shape}, y={y_val.shape}")
        print(f"  Teste:     X={X_test.shape}, y={y_test.shape}")
        print(f"  Classes ({self.n_classes}): {self.classes}")

        return (X_train, y_train), (X_val, y_val), (X_test, y_test)

    def save_artifacts(
        self,
        filepath: Optional[Union[str, Path]] = None,
        suffix: str = "",
    ) -> Tuple[Path, Path]:
        """Salva artefatos de forma atômica (.pkl binário e .json inspecionável)."""
        if not self._is_fitted:
            raise RuntimeError("Não há artefatos para salvar. Execute fit() primeiro.")

        prefix = f"{self.dataset_name}{f'_{suffix}' if suffix else ''}"
        if filepath is None:
            pkl_path = self.artifacts_dir / f"{prefix}_artifacts.pkl"
            json_path = self.artifacts_dir / f"{prefix}_metadata.json"
        else:
            pkl_path = Path(filepath)
            json_path = pkl_path.with_suffix(".json")

        pkl_path.parent.mkdir(parents=True, exist_ok=True)

        # Binário pickle
        artifacts = {
            "scaler": self.scaler,
            "label_encoder": self.label_encoder,
            "feature_names": self.feature_names,
            "canonical_features": self.canonical_features,
            "log1p_features": self.log1p_features,
            "feature_medians": self.feature_medians_,
            "dropped_variance_columns": self.dropped_variance_columns,
            "domain_indices": self.get_domain_indices(),
            "dataset_name": self.dataset_name,
            "target_column": self.target_column,
            "threat_level_used": self._threat_level_used,
            "random_state": self.random_state,
            "class_weights": self.class_weights,
            "audit": self._fit_audit or _runtime_audit(),
        }

        fd, tmp_path = tempfile.mkstemp(dir=pkl_path.parent, suffix=".tmp")
        try:
            with os.fdopen(fd, "wb") as f:
                pickle.dump(artifacts, f, protocol=pickle.HIGHEST_PROTOCOL)
            os.replace(tmp_path, pkl_path)
        except Exception:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
            raise

        # Metadados JSON legíveis
        metadata = {
            "dataset_name": self.dataset_name,
            "target_column": self.target_column,
            "n_features": self.n_features,
            "n_classes": self.n_classes,
            "feature_names": self.feature_names,
            "log1p_features": self.log1p_features,
            "dropped_variance_columns": self.dropped_variance_columns,
            "class_mapping": {
                int(i): str(label)
                for i, label in enumerate(self.label_encoder.classes_)
            },
            "class_weights": self.class_weights,
            "threat_level_used": self._threat_level_used,
            "random_state": self.random_state,
            "audit": self._fit_audit or _runtime_audit(),
        }

        fd_j, tmp_j = tempfile.mkstemp(dir=json_path.parent, suffix=".tmp")
        try:
            with os.fdopen(fd_j, "w", encoding="utf-8") as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            os.replace(tmp_j, json_path)
        except Exception:
            if os.path.exists(tmp_j):
                os.unlink(tmp_j)
            raise

        print(f"[Preprocessor] Artefatos persistidos:\n  PKL:  {pkl_path}\n  JSON: {json_path}")
        return pkl_path, json_path

    def load_artifacts(
        self,
        filepath: Optional[Union[str, Path]] = None,
        suffix: str = "",
    ) -> "Preprocessor":
        """Restaura o pipeline a partir de artefatos persistidos."""
        prefix = f"{self.dataset_name}{f'_{suffix}' if suffix else ''}"
        if filepath is None:
            pkl_path = self.artifacts_dir / f"{prefix}_artifacts.pkl"
        else:
            pkl_path = Path(filepath)

        if not pkl_path.exists():
            raise FileNotFoundError(f"Artefato pickle não encontrado em: {pkl_path}")

        with open(pkl_path, "rb") as f:
            artifacts = pickle.load(f)

        self.scaler = artifacts["scaler"]
        self.label_encoder = artifacts["label_encoder"]
        self.feature_names = artifacts["feature_names"]
        self.canonical_features = artifacts.get("canonical_features", self.feature_names)
        self.log1p_features = artifacts.get("log1p_features", [])
        self.feature_medians_ = artifacts.get("feature_medians", {})
        self.dropped_variance_columns = artifacts.get("dropped_variance_columns", list(self.EXPLICIT_DROP_COLUMNS))
        self.domain_indices = artifacts.get("domain_indices", self.get_domain_indices())
        self.dataset_name = artifacts.get("dataset_name", self.dataset_name)
        self.target_column = artifacts.get("target_column", self.target_column)
        self._threat_level_used = artifacts.get("threat_level_used")

        # Fallback de inferência de threat_level_used caso venha nulo de artefatos legados
        if self._threat_level_used is None and self.label_encoder is not None:
            n_cls = len(self.label_encoder.classes_)
            if self.dataset_name == "CIC-BCCC-NRC-2024":
                self._threat_level_used = 0 if n_cls == 49 else (1 if n_cls > 9 else 2)
            elif "CIC" in self.dataset_name:
                self._threat_level_used = 0 if n_cls >= 14 else 2
            else:
                self._threat_level_used = 0

        self.threat_level = self._threat_level_used
        self.class_weights = artifacts.get("class_weights")
        self._fit_audit = artifacts.get("audit")
        self._is_fitted = True

        print(f"[Preprocessor] Artefatos carregados com sucesso de: {pkl_path}")
        print(f"  Features: {len(self.feature_names)} | Classes: {len(self.label_encoder.classes_)} | Threat Level: {self._threat_level_used}")
        return self
