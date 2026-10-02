---
id: artigo_022
title: 'Laccolith: Hypervisor-Based Adversary Emulation With Anti-Detection'
authors:
- Vittorio Orbinato
- Marco Carlo Feliciano
- Domenico Cotroneo
- Roberto Natella
year: 2024
bibtex_key: laccolith2024
doi: 10.1109/tdsc.2024.3376129
venue: IEEE Transactions on Dependable and Secure Computing, 21(6), 5374-5387
keywords:
- Adversary Emulation
- Hypervisor-based Security
- Anti-Detection
- Red Teaming
- MITRE ATT&CK
- EDR Evaluation
area: Adversary Emulation / System Security / Virtualization / Anti-Detection
datasets:
- Cenários de emulação de técnicas MITRE ATT&CK em Windows e Linux hóspedes
models:
- Virtual Machine Introspection (VMI)
- Hypervisor-level System Call Injection
- Memory Forensics Parsing
aliases:
- 'Laccolith: Hypervisor-Based Adversary Emulation With Anti-Detection'
- laccolith2024
- artigo_022
tags:
- bibliografia
- alf-moe
- artigo
---

# Laccolith: Hypervisor-Based Adversary Emulation With Anti-Detection

> **Citação ABNT Sugerida:** ORBINATO, V.; FELICIANO, M. C.; COTRONEO, D.; NATELLA, R.. Laccolith: Hypervisor-Based Adversary Emulation With Anti-Detection. In: **IEEE Transactions on Dependable and Secure Computing, 21(6), 5374-5387**, 2024.
> **Chave BibTeX:** `laccolith2024` | **Arquivo TXT:** `Laccolith__Hypervisor-Based_Adversary_Emulation_with_Anti-Detection_2024.txt` | **DOI:** `10.1109/tdsc.2024.3376129`

---

## 📌 Metadados e Classificação
| Atributo | Detalhe |
| :--- | :--- |
| **Identificador** | `artigo_022` |
| **Ano** | 2024 |
| **Área de Pesquisa** | Adversary Emulation / System Security / Virtualization / Anti-Detection |
| **Veículo de Publicação** | IEEE Transactions on Dependable and Secure Computing, 21(6), 5374-5387 |
| **Datasets Utilizados** | Cenários de emulação de técnicas MITRE ATT&CK em Windows e Linux hóspedes |
| **Modelos / Algoritmos** | Virtual Machine Introspection (VMI), Hypervisor-level System Call Injection, Memory Forensics Parsing |
| **Palavras-Chave** | Adversary Emulation, Hypervisor-based Security, Anti-Detection, Red Teaming, MITRE ATT&CK, EDR Evaluation |

## 🎯 Problema Abordado
Ferramentas tradicionais de emulação de adversários operam dentro do sistema operacional alvo (in-guest agents), deixando rastros artificiais de processos e arquivos que acionam defesas com base no agente emulador em vez do comportamento da técnica maliciosa real.

## 🔬 Metodologia
Arquitetura Laccolith operando no nível do hipervisor (fora do sistema operacional da máquina virtual hóspede); utilização de Virtual Machine Introspection (VMI) e manipulação transparente de memória/registradores da VM para disparar técnicas do framework MITRE ATT&CK de forma totalmente furtiva e indetectável.

## 🏆 Principais Resultados e Contribuições
**Resultados Principais:**
O Laccolith executou 100% das técnicas de adversários avaliadas sem ser detectado por soluções comerciais de EDR e NIDS baseadas em assinatura de agentes, garantindo que o teste avalie estritamente a telemetria do ataque.

**Contribuições Centrais:**
- Primeira plataforma de emulação de adversários transparente baseada inteiramente em hipervisor.
- Eliminação sistemática de artefatos de teste em sistemas avaliados.
- Validação empírica contra soluções de ponta de detecção de intrusão e EDR.

## ⚠️ Limitações Identificadas
Exige controle completo da infraestrutura de virtualização e suporte a extensões de virtualização de hardware (Intel VT-x / AMD-V).

## 🗺️ Mapa Conceitual
- **Conceitos-Chave:** `Emulação de Adversários`, `Hipervisor`, `Anti-Detecção`, `VMI`
- **Problemas Focais:** `Artefatos de agentes emuladores distorcem testes de segurança`, `Evasão de defesas`
- **Métodos Empregados:** `Introspecção de Máquina Virtual (VMI)`, `Injeção externa fora do SO hóspede`
- **Modelos e Arquiteturas:** `Laccolith Engine`
- **Bases de Dados:** `Táticas MITRE ATT&CK`
- **Resultados Chave:** `Execução 100% furtiva sem alerta falso gerado pelo framework de teste`
- **Limitações Reconhecidas:** `Requer acesso administrativo ao hipervisor hospedeiro`
- **Evidências Citáveis:** `EVID_022_01`

## 🔗 Relações na Base de Conhecimento

### Relações Ativas Declaradas (Outgoing)
- **Relacionado:**
  - [[artigo_012]] — *DeepStage: Learning Autonomous Defense Policies Against Multi-Stage APT Campaigns*
  - [[artigo_031]] — *Red Team Redemption: A Structured Comparison of Open-Source Tools for Adversary Emulation*
  - [[artigo_032]] — *Simulating Cyberattacks through a Breach Attack Simulation (BAS) Platform empowered by Security Chaos Engineering (SCE)*

### Citações e Relações Recebidas na Base (Incoming)
- **Relacionado:**
  - [[artigo_012]] — *DeepStage: Learning Autonomous Defense Policies Against Multi-Stage APT Campaigns*
  - [[artigo_031]] — *Red Team Redemption: A Structured Comparison of Open-Source Tools for Adversary Emulation*
  - [[artigo_032]] — *Simulating Cyberattacks through a Breach Attack Simulation (BAS) Platform empowered by Security Chaos Engineering (SCE)*
  - [[artigo_038]] — *The Procedural Semantics Gap in Structured CTI: A Measurement-Driven STIX Analysis for APT Emulation*

## 🎓 Integração com a Tese ALF-MoE

## 📖 Evidências Literais Extraídas (Fidelidade Rigorosa)

### `EVID_022_01` — METODOLÓGICA
> [!quote] EVID_022_01 (Relevância: 4/5 | Grau: Sustenta a afirmação)
> **Afirmação Sustentada:** A emulação de adversários fundamentada em frameworks estruturados (MITRE ATT&CK) deve minimizar artefatos operacionais espúrios para permitir avaliação fidedigna de defesas.
> **Localização:** Seção 1 (Introduction) e Seção 2 (Adversary Emulation Challenges), Páginas 5374-5376
>
> *"Realistic adversary emulation requires executing ATT&CK techniques with zero intrusive artifacts, ensuring that security sensors detect the underlying malicious procedural behavior rather than the testing tool itself."*
>
> **Aplicabilidade na Tese ALF-MoE:** Fundamenta a discussão metodológica sobre fidelidade na geração de tráfego de ataques e avaliação de NIDS sob cenários realistas de Red Teaming.

## 📦 Entrada BibTeX
```bibtex
@article{laccolith2024,
  title = {Laccolith: Hypervisor-Based Adversary Emulation With Anti-Detection},
  author = {Orbinato, Vittorio and Feliciano, Marco Carlo and Cotroneo, Domenico and Natella, Roberto},
  journal = {IEEE Transactions on Dependable and Secure Computing},
  year = {2024},
  doi = {10.1109/tdsc.2024.3376129},
  volume = {21},
  number = {6},
  pages = {5374-5387},
  publisher = {Institute of Electrical and Electronics Engineers (IEEE)}
}
```

## 🧭 Navegação
- ⬅️ [[00_Indice_Bibliografico|Índice Geral de Artigos]]
- 🧠 [[Conceitos_Centrais|Conceitos Centrais da Base]]
- ⚡ [[Contradicoes_e_Divergencias|Contradições e Divergências da Literatura]]
- 🕸️ [[Rede_Intelectual|Rede Intelectual e Cadeias Epistemológicas]]
- 📋 [[Afirmacoes_e_Claims|Afirmações e Claims Acadêmicos]]
- 📑 [[BASE_DE_CONHECIMENTO_COMPLETA|Dossiê Completo da Base]]
