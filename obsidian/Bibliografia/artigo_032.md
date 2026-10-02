---
id: artigo_032
title: Simulating Cyberattacks through a Breach Attack Simulation (BAS) Platform empowered
  by Security Chaos Engineering (SCE)
authors:
- Arturo Sánchez-Matas
- Pablo Escribano Ruiz
- Daniel Díaz-López
- Ángel Luis Perales Gómez
- Pantaleone Nespoli
- Gregorio Martínez Pérez
year: 2025
bibtex_key: bas2026
doi: INFORMAÇÃO NÃO LOCALIZADA NO DOCUMENTO
venue: arXiv preprint arXiv:2508.03882
keywords:
- Breach Attack Simulation (BAS)
- Security Chaos Engineering (SCE)
- Continuous Validation
- Cyber Resilience
- Attack Simulation
area: Continuous Security Validation / Security Chaos Engineering / BAS
datasets:
- Testbed de nuvem corporativa e microsserviços sob ataques contínuos
models:
- Chaos Injection Controller
- Automated Attack Playbooks
- Telemetry Verification Engine
aliases:
- Simulating Cyberattacks through a Breach Attack Simulation (BAS) Platform empowered
  by Security Chaos Engineering (SCE)
- bas2026
- artigo_032
tags:
- bibliografia
- alf-moe
- artigo
---

# Simulating Cyberattacks through a Breach Attack Simulation (BAS) Platform empowered by Security Chaos Engineering (SCE)

> **Citação ABNT Sugerida:** SÁNCHEZ-MATAS, A.; RUIZ, P. E.; DÍAZ-LÓPEZ, D.; GÓMEZ, Á. L. P.; NESPOLI, P.; PÉREZ, G. M.. Simulating Cyberattacks through a Breach Attack Simulation (BAS) Platform empowered by Security Chaos Engineering (SCE). In: **arXiv preprint arXiv:2508.03882**, 2025.
> **Chave BibTeX:** `bas2026` | **Arquivo TXT:** `Simulating_Cyberattacks_through_a_Breach_Attack_Simulation_(BAS)_Platform_empowered_by_Security_Chaos_Engineering_(SCE)_2026.txt` | **DOI:** `INFORMAÇÃO NÃO LOCALIZADA NO DOCUMENTO`

---

## 📌 Metadados e Classificação
| Atributo | Detalhe |
| :--- | :--- |
| **Identificador** | `artigo_032` |
| **Ano** | 2025 |
| **Área de Pesquisa** | Continuous Security Validation / Security Chaos Engineering / BAS |
| **Veículo de Publicação** | arXiv preprint arXiv:2508.03882 |
| **Datasets Utilizados** | Testbed de nuvem corporativa e microsserviços sob ataques contínuos |
| **Modelos / Algoritmos** | Chaos Injection Controller, Automated Attack Playbooks, Telemetry Verification Engine |
| **Palavras-Chave** | Breach Attack Simulation (BAS), Security Chaos Engineering (SCE), Continuous Validation, Cyber Resilience, Attack Simulation |

## 🎯 Problema Abordado
Testes de intrusão convencionais e auditorias manuais fornecem apenas fotografias estáticas da segurança; as constantes atualizações de infraestrutura geram desvios de configuração (drift) que reintroduzem vulnerabilidades silenciosas.

## 🔬 Metodologia
Plataforma de Breach and Attack Simulation (BAS) combinada com princípios de Engenharia do Caos em Segurança (Security Chaos Engineering - SCE); injeção sistemática de falhas de segurança e simulação de ataques em ambientes de produção com verificação automatizada de alertas.

## 🏆 Principais Resultados e Contribuições
**Resultados Principais:**
A plataforma identificou que 34% das configurações de detecção sofreram degradação após mudanças de rotina de infraestrutura, demonstrando a necessidade de validação e teste automatizados contínuos.

**Contribuições Centrais:**
- Convergência formal entre BAS e Engenharia do Caos aplicada à cibersegurança.
- Arquitetura de injeção contínua de experimentos de ataque.
- Demonstração empírica da prevalência do drift de configuração em NIDS corporativos.

## ⚠️ Limitações Identificadas
Risco de induzir indisponibilidade operacional se experimentos de injeção de caos excederem os limites de segurança (blast radius) pré-definidos.

## 🗺️ Mapa Conceitual
- **Conceitos-Chave:** `Breach Attack Simulation`, `Security Chaos Engineering`, `Validação Contínua`, `Drift de Configuração`
- **Problemas Focais:** `Auditorias pontuais tornam-se obsoletas rapidamente`, `Degradação silenciosa de defesas em produção`
- **Métodos Empregados:** `Injeção controlada de ataques`, `Monitoramento de telemetria em tempo real`, `Controle de blast radius`
- **Modelos e Arquiteturas:** `BAS-SCE Platform`
- **Bases de Dados:** `Telemetria de nuvem e microsserviços`
- **Resultados Chave:** `Identificação de 34% de falhas silenciosas decorrentes de mudanças na rede`
- **Limitações Reconhecidas:** `Requer governança rigorosa para evitar impactos no negócio`
- **Evidências Citáveis:** `EVID_032_01`

## 🔗 Relações na Base de Conhecimento

### Relações Ativas Declaradas (Outgoing)
- **Relacionado:**
  - [[artigo_012]] — *DeepStage: Learning Autonomous Defense Policies Against Multi-Stage APT Campaigns*
  - [[artigo_022]] — *Laccolith: Hypervisor-Based Adversary Emulation With Anti-Detection*
  - [[artigo_031]] — *Red Team Redemption: A Structured Comparison of Open-Source Tools for Adversary Emulation*

### Citações e Relações Recebidas na Base (Incoming)
- **Relacionado:**
  - [[artigo_012]] — *DeepStage: Learning Autonomous Defense Policies Against Multi-Stage APT Campaigns*
  - [[artigo_022]] — *Laccolith: Hypervisor-Based Adversary Emulation With Anti-Detection*
  - [[artigo_031]] — *Red Team Redemption: A Structured Comparison of Open-Source Tools for Adversary Emulation*

## 🎓 Integração com a Tese ALF-MoE

### Participação em Cadeias Intelectuais
- [[Rede_Intelectual#Cadeia 3: Metodologia de Avaliação e Ruptura do Random Split|Cadeia 3: Metodologia de Avaliação e Ruptura do Random Split]] — **Etapa LACUNA:** Mecanismos de aprendizado contínuo adaptativo para NIDS em produção

## 📖 Evidências Literais Extraídas (Fidelidade Rigorosa)

### `EVID_032_01` — MOTIVAÇÃO
> [!quote] EVID_032_01 (Relevância: 4/5 | Grau: Sustenta a afirmação)
> **Afirmação Sustentada:** A validação contínua e a simulação de ataques em produção são necessárias para garantir a eficácia operacional de sistemas de detecção de intrusão frente a mudanças dinâmicas na infraestrutura.
> **Localização:** Seção 1 (Introduction) e Seção 2 (Security Chaos Engineering Principles), Páginas 1-4
>
> *"Point-in-time security audits fail to capture vulnerabilities introduced by regular operational churn; continuous attack simulation empowered by security chaos engineering is essential to verify that detection pipelines remain functionally effective."*
>
> **Aplicabilidade na Tese ALF-MoE:** Contextualiza a necessidade de arquiteturas robustas e monitoramento contínuo em ambientes operacionais corporativos.

## 📦 Entrada BibTeX
```bibtex
@article{bas2026,
  title = {Simulating Cyberattacks through a Breach Attack Simulation (BAS) Platform empowered by Security Chaos Engineering (SCE)},
  author = {Sánchez-Matas, Arturo and Escribano Ruiz, Pablo and Díaz-López, Daniel and Perales Gómez, {\'{A}}ngel Luis and Nespoli, Pantaleone and Martínez Pérez, Gregorio},
  journal = {arXiv preprint arXiv:2508.03882},
  year = {2025}
}
```

## 🧭 Navegação
- ⬅️ [[00_Indice_Bibliografico|Índice Geral de Artigos]]
- 🧠 [[Conceitos_Centrais|Conceitos Centrais da Base]]
- ⚡ [[Contradicoes_e_Divergencias|Contradições e Divergências da Literatura]]
- 🕸️ [[Rede_Intelectual|Rede Intelectual e Cadeias Epistemológicas]]
- 📋 [[Afirmacoes_e_Claims|Afirmações e Claims Acadêmicos]]
- 📑 [[BASE_DE_CONHECIMENTO_COMPLETA|Dossiê Completo da Base]]
