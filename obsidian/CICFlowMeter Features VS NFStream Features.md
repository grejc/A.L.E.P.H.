| **CIC-BCCC-NRC-2024**      |     **CIC-UNSW-NB15**      | **CSE-CIC-IDS2018** | **_NFStream_**               |
| :------------------------- | :------------------------: | :-----------------: | :--------------------------- |
| Flow ID                    |          Flow ID           |                     | id                           |
| Src IP                     |           Src IP           |                     | src_ip                       |
| Src Port                   |          Src Port          |                     | src_port                     |
| Dst IP                     |           Dst IP           |                     | dst_ip                       |
| Dst Port                   |          Dst Port          |      Dst Port       | dst_port                     |
| Protocol                   |          Protocol          |      Protocol       | protocol                     |
| Timestamp                  |         Timestamp          |      Timestamp      | bidirectional_first_seen_ms  |
| Flow Duration              |       Flow Duration        |    Flow Duration    | bidirectional_duration_ms    |
| Total Fwd Packet           |      Total Fwd Packet      |    Tot Fwd Pkts     | src2dst_packets              |
| Total Bwd packets          |     Total Bwd packets      |    Tot Bwd Pkts     | dst2src_packets              |
| Total Length of Fwd Packet | Total Length of Fwd Packet |   TotLen Fwd Pkts   | src2dst_bytes                |
| Total Length of Bwd Packet | Total Length of Bwd Packet |   TotLen Bwd Pkts   | dst2src_bytes                |
| Fwd Packet Length Max      |   Fwd Packet Length Max    |   Fwd Pkt Len Max   | src2dst_max_ps               |
| Fwd Packet Length Min      |   Fwd Packet Length Min    |   Fwd Pkt Len Min   | src2dst_min_ps               |
| Fwd Packet Length Mean     |   Fwd Packet Length Mean   |  Fwd Pkt Len Mean   | src2dst_mean_ps              |
| Fwd Packet Length Std      |   Fwd Packet Length Std    |   Fwd Pkt Len Std   | src2dst_stddev_ps            |
| Bwd Packet Length Max      |   Bwd Packet Length Max    |   Bwd Pkt Len Max   | dst2src_max_ps               |
| Bwd Packet Length Min      |   Bwd Packet Length Min    |   Bwd Pkt Len Min   | dst2src_min_ps               |
| Bwd Packet Length Mean     |   Bwd Packet Length Mean   |  Bwd Pkt Len Mean   | dst2src_mean_ps              |
| Bwd Packet Length Std      |   Bwd Packet Length Std    |   Bwd Pkt Len Std   | dst2src_stddev_ps            |
| Flow Bytes/s               |        Flow Bytes/s        |     Flow Byts/s     | bytes_per_second\*           |
| Flow Packets/s             |       Flow Packets/s       |     Flow Pkts/s     | packets_per_second\*         |
| Flow IAT Mean              |       Flow IAT Mean        |    Flow IAT Mean    | bidirectional_mean_piat_ms   |
| Flow IAT Std               |        Flow IAT Std        |    Flow IAT Std     | bidirectional_stddev_piat_ms |
| Flow IAT Max               |        Flow IAT Max        |    Flow IAT Max     | bidirectional_max_piat_ms    |
| Flow IAT Min               |        Flow IAT Min        |    Flow IAT Min     | bidirectional_min_piat_ms    |
| Fwd IAT Total              |       Fwd IAT Total        |     Fwd IAT Tot     | src2dst_duration_ms          |
| Fwd IAT Mean               |        Fwd IAT Mean        |    Fwd IAT Mean     | src2dst_mean_piat_ms         |
| Fwd IAT Std                |        Fwd IAT Std         |     Fwd IAT Std     | src2dst_stddev_piat_ms       |
| Fwd IAT Max                |        Fwd IAT Max         |     Fwd IAT Max     | src2dst_max_piat_ms          |
| Fwd IAT Min                |        Fwd IAT Min         |     Fwd IAT Min     | src2dst_min_piat_ms          |
| Bwd IAT Total              |       Bwd IAT Total        |     Bwd IAT Tot     | dst2src_duration_ms          |
| Bwd IAT Mean               |        Bwd IAT Mean        |    Bwd IAT Mean     | dst2src_mean_piat_ms         |
| Bwd IAT Std                |        Bwd IAT Std         |     Bwd IAT Std     | dst2src_stddev_piat_ms       |
| Bwd IAT Max                |        Bwd IAT Max         |     Bwd IAT Max     | dst2src_max_piat_ms          |
| Bwd IAT Min                |        Bwd IAT Min         |     Bwd IAT Min     | dst2src_min_piat_ms          |
| Fwd PSH Flags              |       Fwd PSH Flags        |    Fwd PSH Flags    | src2dst_psh_packets          |
| Bwd PSH Flags              |       Bwd PSH Flags        |    Bwd PSH Flags    | dst2src_psh_packets          |
| Fwd URG Flags              |       Fwd URG Flags        |    Fwd URG Flags    | src2dst_urg_packets          |
| Bwd URG Flags              |       Bwd URG Flags        |    Bwd URG Flags    | dst2src_urg_packets          |
| Fwd Header Length          |     Fwd Header Length      |   Fwd Header Len    | fwd_header_length\*          |
| Bwd Header Length          |     Bwd Header Length      |   Bwd Header Len    | bwd_header_length\*          |
| Fwd Packets/s              |       Fwd Packets/s        |     Fwd Pkts/s      | fwd_packets_per_second\*     |
| Bwd Packets/s              |       Bwd Packets/s        |     Bwd Pkts/s      | bwd_packets_per_second\*     |
| Packet Length Min          |     Packet Length Min      |     Pkt Len Min     | bidirectional_min_ps         |
| Packet Length Max          |     Packet Length Max      |     Pkt Len Max     | bidirectional_max_ps         |
| Packet Length Mean         |     Packet Length Mean     |    Pkt Len Mean     | bidirectional_mean_ps        |
| Packet Length Std          |     Packet Length Std      |     Pkt Len Std     | bidirectional_stddev_ps      |
| Packet Length Variance     |   Packet Length Variance   |     Pkt Len Var     | packet_length_variance\*     |
| FIN Flag Count             |       FIN Flag Count       |    FIN Flag Cnt     | bidirectional_fin_packets    |
| SYN Flag Count             |       SYN Flag Count       |    SYN Flag Cnt     | bidirectional_syn_packets    |
| RST Flag Count             |       RST Flag Count       |    RST Flag Cnt     | bidirectional_rst_packets    |
| PSH Flag Count             |       PSH Flag Count       |    PSH Flag Cnt     | bidirectional_psh_packets    |
| ACK Flag Count             |       ACK Flag Count       |    ACK Flag Cnt     | bidirectional_ack_packets    |
| URG Flag Count             |       URG Flag Count       |    URG Flag Cnt     | bidirectional_urg_packets    |
| CWR Flag Count             |       CWR Flag Count       |   CWE Flag Count    | bidirectional_cwr_packets    |
| ECE Flag Count             |       ECE Flag Count       |    ECE Flag Cnt     | bidirectional_ece_packets    |
| Down/Up Ratio              |       Down/Up Ratio        |    Down/Up Ratio    | down_up_ratio\*              |
| Average Packet Size        |    Average Packet Size     |    Pkt Size Avg     | avg_bytes_per_packet\*       |
| Fwd Segment Size Avg       |    Fwd Segment Size Avg    |  Fwd Seg Size Avg   | fwd_segment_size_avg\*       |
| Bwd Segment Size Avg       |    Bwd Segment Size Avg    |  Bwd Seg Size Avg   | bwd_segment_size_avg\*       |
| Fwd Bytes/Bulk Avg         |     Fwd Bytes/Bulk Avg     |   Fwd Byts/b Avg    | fwd_bytes_bulk_avg\*         |
| Fwd Packet/Bulk Avg        |    Fwd Packet/Bulk Avg     |   Fwd Pkts/b Avg    | fwd_packet_bulk_avg\*        |
| Fwd Bulk Rate Avg          |     Fwd Bulk Rate Avg      |  Fwd Blk Rate Avg   | fwd_bulk_rate_avg\*          |
| Bwd Bytes/Bulk Avg         |     Bwd Bytes/Bulk Avg     |   Bwd Byts/b Avg    | bwd_bytes_bulk_avg\*         |
| Bwd Packet/Bulk Avg        |    Bwd Packet/Bulk Avg     |   Bwd Pkts/b Avg    | bwd_packet_bulk_avg\*        |
| Bwd Bulk Rate Avg          |     Bwd Bulk Rate Avg      |  Bwd Blk Rate Avg   | bwd_bulk_rate_avg\*          |
| Subflow Fwd Packets        |    Subflow Fwd Packets     |  Subflow Fwd Pkts   | subflow_fwd_packets\*        |
| Subflow Fwd Bytes          |     Subflow Fwd Bytes      |  Subflow Fwd Byts   | subflow_fwd_bytes\*          |
| Subflow Bwd Packets        |    Subflow Bwd Packets     |  Subflow Bwd Pkts   | subflow_bwd_packets\*        |
| Subflow Bwd Bytes          |     Subflow Bwd Bytes      |  Subflow Bwd Byts   | subflow_bwd_bytes\*          |
| FWD Init Win Bytes         |     FWD Init Win Bytes     |  Init Fwd Win Byts  | fwd_init_win_bytes\*         |
| Bwd Init Win Bytes         |     Bwd Init Win Bytes     |  Init Bwd Win Byts  | bwd_init_win_bytes\*         |
| Fwd Act Data Pkts          |     Fwd Act Data Pkts      |  Fwd Act Data Pkts  | fwd_act_data_pkts\*          |
| Fwd Seg Size Min           |      Fwd Seg Size Min      |  Fwd Seg Size Min   | fwd_seg_size_min\*           |
| Active Mean                |        Active Mean         |     Active Mean     | active_mean\*                |
| Active Std                 |         Active Std         |     Active Std      | active_std\*                 |
| Active Max                 |         Active Max         |     Active Max      | active_max\*                 |
| Active Min                 |         Active Min         |     Active Min      | active_min\*                 |
| Idle Mean                  |         Idle Mean          |      Idle Mean      | idle_mean\*                  |
| Idle Std                   |          Idle Std          |      Idle Std       | idle_std\*                   |
| Idle Max                   |          Idle Max          |      Idle Max       | idle_max\*                   |
| Idle Min                   |          Idle Min          |      Idle Min       | idle_min\*                   |
| Attack Name                |                            |                     |                              |
| Label                      |           Label            |        Label        |                              |

---

*Features com asterisco (`*`) são calculadas/agregadas via plugin customizado (`flow.udps`). As features sem asterisco são atributos nativos do objeto de fluxo (`flow`) extraídos diretamente pelo NFStream.*
