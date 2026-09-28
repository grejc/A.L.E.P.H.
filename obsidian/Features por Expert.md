Foram consideradas apenas as features padrões de extração, ou seja, as que são a partir de `Flow Duration`;

|  #  | _Feature_                  | **DNN** | **CNN\*** | **GRU\*** | **CAE** | **LSTM\*** |
| :-: | :------------------------- | :-----: | :-----: | :-----: | :-----: | :------: |
|  0  | Flow duration              |    x    |         |    x    |    x    |          |
|  1  | Total Fwd Packet           |    x    |         |    x    |         |          |
|  2  | Total Bwd packets          |    x    |         |    x    |         |          |
|  3  | Total Length of Fwd Packet |    x    |         |    x    |         |          |
|  4  | Total Length of Bwd Packet |    x    |         |    x    |         |          |
|  5  | Fwd Packet Length Min      |         |    x    |         |         |          |
|  6  | Fwd Packet Length Max      |         |    x    |         |         |          |
|  7  | Fwd Packet Length Mean     |         |    x    |         |         |          |
|  8  | Fwd Packet Length Std      |         |    x    |         |         |          |
|  9  | Bwd Packet Length Min      |         |    x    |         |         |          |
| 10  | Bwd Packet Length Max      |         |    x    |         |         |          |
| 11  | Bwd Packet Length Mean     |         |    x    |         |         |          |
| 12  | Bwd Packet Length Std      |         |    x    |         |         |          |
| 13  | Flow Bytes/s               |    x    |         |         |    x    |          |
| 14  | Flow Packets/s             |    x    |         |    x    |    x    |          |
| 15  | Flow IAT Mean              |         |    x    |    x    |         |          |
| 16  | Flow IAT Std               |         |    x    |    x    |         |          |
| 17  | Flow IAT Max               |         |    x    |    x    |         |          |
| 18  | Flow IAT Min               |         |    x    |    x    |         |          |
| 19  | Fwd IAT Min                |         |         |    x    |         |          |
| 20  | Fwd IAT Max                |         |         |    x    |         |          |
| 21  | Fwd IAT Mean               |         |         |    x    |         |          |
| 22  | Fwd IAT Std                |         |         |    x    |         |          |
| 23  | Fwd IAT Total              |         |         |    x    |         |          |
| 24  | Bwd IAT Min                |         |         |    x    |         |          |
| 25  | Bwd IAT Max                |         |         |    x    |         |          |
| 26  | Bwd IAT Mean               |         |         |    x    |         |          |
| 27  | Bwd IAT Std                |         |         |    x    |         |          |
| 28  | Bwd IAT Total              |         |         |    x    |         |          |
| 29  | Fwd PSH flags              |    x    |         |         |         |          |
| 30  | Bwd PSH Flags              |         |         |         |         |          |
| 31  | Fwd URG Flags              |    x    |         |         |         |          |
| 32  | Bwd URG Flags              |         |         |         |         |          |
| 33  | Fwd Header Length          |    x    |         |         |         |          |
| 34  | Bwd Header Length          |    x    |         |         |         |          |
| 35  | FWD Packets/s              |         |         |    x    |         |          |
| 36  | Bwd Packets/s              |         |         |    x    |         |          |
| 37  | Packet Length Min          |         |    x    |         |         |          |
| 38  | Packet Length Max          |         |    x    |         |         |          |
| 39  | Packet Length Mean         |         |    x    |         |         |          |
| 40  | Packet Length Std          |         |    x    |         |         |          |
| 41  | Packet Length Variance     |         |    x    |    x    |         |          |
| 42  | FIN Flag Count             |    x    |         |         |         |          |
| 43  | SYN Flag Count             |    x    |         |         |         |          |
| 44  | RST Flag Count             |    x    |         |         |         |          |
| 45  | PSH Flag Count             |    x    |         |         |         |          |
| 46  | ACK Flag Count             |    x    |         |         |         |          |
| 47  | URG Flag Count             |    x    |         |         |         |          |
| 48  | CWR Flag Count             |    x    |         |         |         |          |
| 49  | ECE Flag Count             |    x    |         |         |         |          |
| 50  | Down/Up Ratio              |    x    |         |    x    |         |          |
| 51  | Average Packet Size        |    x    |         |         |         |          |
| 52  | Fwd Segment Size Avg       |         |         |         |         |          |
| 53  | Bwd Segment Size Avg       |         |         |         |         |          |
| 54  | Fwd Bytes/Bulk Avg         |         |         |         |         |          |
| 55  | Fwd Packet/Bulk Avg        |         |         |         |         |          |
| 56  | Fwd Bulk Rate Avg          |         |         |         |         |          |
| 57  | Bwd Bytes/Bulk Avg         |         |         |         |         |          |
| 58  | Bwd Packet/Bulk Avg        |         |         |         |         |          |
| 59  | Bwd Bulk Rate Avg          |         |         |         |         |          |
| 60  | Subflow Fwd Packets        |    x    |         |         |         |          |
| 61  | Subflow Fwd Bytes          |    x    |         |         |         |          |
| 62  | Subflow Bwd Packets        |    x    |         |         |         |          |
| 63  | Subflow Bwd Bytes          |    x    |         |         |         |          |
| 64  | Fwd Init Win bytes         |    x    |         |         |         |          |
| 65  | Bwd Init Win bytes         |    x    |         |         |         |          |
| 66  | Fwd Act Data Pkts          |    x    |         |         |         |          |
| 67  | Fwd Seg Size Min           |    x    |         |         |         |          |
| 68  | Active Min                 |         |         |    x    |         |          |
| 69  | Active Mean                |         |         |    x    |         |          |
| 70  | Active Max                 |         |         |    x    |         |          |
| 71  | Active Std                 |         |         |    x    |         |          |
| 72  | Idle Min                   |         |         |    x    |         |          |
| 73  | Idle Mean                  |         |         |    x    |         |          |
| 74  | Idle Max                   |         |         |    x    |         |          |
| 75  | Idle Std                   |         |         |    x    |         |          |

*\* Ordem das features importa. Depende do pré-processamento, ou organiza-las de forma que faça sentido.*
