
Para prevenção de "GIGO" (Garbage In, Garbage Out), o pipelina de pré-processamento gerou uma sample de cada dataset com suas próprias características, que serão detalhadas mais a frente;

## CIC-UNSW-NB15

No EDA deste dataset foi identificado uma discrepância muito alta entre fluxos de ataque e fluxos de trafego normal (Benign). Assim foi gerado uma _sample_ que preserva 100% dos fluxos de ataque e 50.000 amostras de fluxo da classe Benign mais informativas via amostragem estratificada multivariada de máxima cobertura comportamental e entropia.

Depois foi feita uma remoção de fluxos duplicados resultando em 125378 amostras.

Colunas identificadoras, sem variância e colineares foram removidas.

Para o treino, validação e teste do dataset foi feito a seguinte divisão:
(Treino 80% | Validação 20%) 80% | Teste 20%

- Treino: 80241 amostras
- Validação: 20061 amostras
- Teste: 25076 amostras

## CSE-CIC-IDS2018

Para esse dataset as colunas foram renomeadas para o padrão canônico CICFlowMeter.

Preservou-se todos os fluxos de ataque (2748235 fluxos) e manteve-se 10% dos fluxos da classe Benign (1348471 fluxos). Removendo os fluxos duplicados, obteve-se um total de 3712942 fluxos;

Acabei de descobrir que há um SOTA para o pré-processamento:
```
@inproceedings{liu2022error,
        title={Error Prevalence in NIDS datasets: A Case Study on CIC-IDS-2017 and CSE-CIC-IDS-2018},
        author={Liu, Lisa and Engelen, Gints and Lynar, Timothy and Essam, Daryl and Joosen, Wouter},
        booktitle={2022 IEEE Conference on Communications and Network Security (CNS)},
        pages={254--262},
        year={2022},
        organization={IEEE}
        }
@INPROCEEDINGS{9947235,
  author={Liu, Lisa and Engelen, Gints and Lynar, Timothy and Essam, Daryl and Joosen, Wouter},
  booktitle={2022 IEEE Conference on Communications and Network Security (CNS)}, 
  title={Error Prevalence in NIDS datasets: A Case Study on CIC-IDS-2017 and CSE-CIC-IDS-2018}, 
  year={2022},
  volume={},
  number={},
  pages={254-262},
  keywords={Documentation;Telecommunication traffic;Benchmark testing;Network security;Complexity theory;Labeling;Network intrusion;network intrusion detection;datasets;CIC-IDS-2017;CSE-CIC-IDS-2018},
  doi={10.1109/CNS56114.2022.9947235}}

```

Que concerta as falhas catastróficas de rotulação; 
> Conforme discutido em nosso artigo, optamos por utilizar o rótulo "Attempted" (Tentativa) para um ataque (por exemplo, DoS GoldenEye – Attempted) sempre que um fluxo destinado a fazer parte do ataque não apresentar qualquer comportamento malicioso. Os pesquisadores têm liberdade para decidir se desejam combinar os fluxos marcados como "Attempted" ao rótulo do ataque propriamente dito, uma vez que isso dependerá fortemente do método de pré-processamento de fluxos aplicado. Em caso de dúvida, recomendamos reclassificar todos os fluxos "Attempted" como benignos (a maneira mais simples de fazer isso é identificar todos os fluxos em que o atributo "Attempted Category" seja diferente de -1). Em hipótese alguma os fluxos "Attempted" devem ser tratados como um rótulo separado para o seu modelo de Aprendizado de Máquina!

Como eu estou na dúvida, vou rotular tudo para Benign. 

Com isso o ataque FTP-BruteForce foi completamente alterado para Benign, pois em ambos os dias que o ataque ocorreu, a porta 21 respondeu apenas pacotes \[RST, ACK\] sugerindo que a porta estava fechada, portanto houve apenas a tentativa de ataque.


## CIC-BCCC-NRC-2024

Esse dataset foi gerado juntando todos os sub-datasets em um único arquivo, preservando as colunas padrões do CICFlowMeter.

Devido ao tamanho do dataset e as limitações da minha máquina, uma sample de 15% do dataset original foi gerada, com retenção de 100% de todas as 14 classes raras e alocação Hare-Niemeyer nas 35 demais classes.

