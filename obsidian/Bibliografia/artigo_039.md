---
id: artigo_039
title: 'Threat Modelling using Domain-Adapted Language Models: Empirical Evaluation
  and Insights'
authors:
- Saba Pourhanifeh
- Abdulaziz Abdulghaffar
- Ashraf Matrawy
year: 2026
bibtex_key: threatmodelling2025
doi: INFORMAÇÃO NÃO LOCALIZADA NO DOCUMENTO
venue: arXiv preprint arXiv:2605.10808
keywords:
- Threat Modelling
- Domain-Adapted LLMs
- STRIDE
- Empirical Evaluation
- Automated Security Analysis
- Prompt Engineering
area: Threat Modelling / Domain-Adapted NLP / Large Language Models
datasets:
- Repositórios abertos de modelos de ameaça STRIDE
- Documentação arquitetural de sistemas de software
models:
- Llama-3-Security-Adapted
- Mistral-7B-Instruct
- GPT-4 (baseline)
- STRIDE Rule Matcher
aliases:
- 'Threat Modelling using Domain-Adapted Language Models: Empirical Evaluation and
  Insights'
- threatmodelling2025
- artigo_039
tags:
- bibliografia
- alf-moe
- artigo
---

# Threat Modelling using Domain-Adapted Language Models: Empirical Evaluation and Insights

> **Citação ABNT Sugerida:** POURHANIFEH, S.; ABDULGHAFFAR, A.; MATRAWY, A.. Threat Modelling using Domain-Adapted Language Models: Empirical Evaluation and Insights. In: **arXiv preprint arXiv:2605.10808**, 2026.
> **Chave BibTeX:** `threatmodelling2025` | **Arquivo TXT:** `Threat_Modelling_using_Domain-Adapted_Language_Models__Empirical_Evaluation_and_Insights.txt` | **DOI:** `INFORMAÇÃO NÃO LOCALIZADA NO DOCUMENTO`

---

## 📌 Metadados e Classificação
| Atributo | Detalhe |
| :--- | :--- |
| **Identificador** | `artigo_039` |
| **Ano** | 2026 |
| **Área de Pesquisa** | Threat Modelling / Domain-Adapted NLP / Large Language Models |
| **Veículo de Publicação** | arXiv preprint arXiv:2605.10808 |
| **Datasets Utilizados** | Repositórios abertos de modelos de ameaça STRIDE, Documentação arquitetural de sistemas de software |
| **Modelos / Algoritmos** | Llama-3-Security-Adapted, Mistral-7B-Instruct, GPT-4 (baseline), STRIDE Rule Matcher |
| **Palavras-Chave** | Threat Modelling, Domain-Adapted LLMs, STRIDE, Empirical Evaluation, Automated Security Analysis, Prompt Engineering |

## 🎯 Problema Abordado
A modelagem de ameaças manual (como no framework STRIDE) consome muito tempo, exige especialistas seniores de segurança e frequentemente omite riscos sutis de arquitetura em sistemas corporativos complexos.

## 🔬 Metodologia
Adaptação e ajuste fino de modelos de linguagem de grande porte (LLMs) em corpus especializado de cibersegurança e arquiteturas de software; avaliação empírica da capacidade dos modelos em gerar diagramas de fluxo de dados (DFD) e mapear ameaças STRIDE automaticamente a partir de descrições textuais de sistemas.

## 🏆 Principais Resultados e Contribuições
**Resultados Principais:**
Modelos adaptados ao domínio atingiram precisão de 82.4% e revocação de 87.1% na identificação de ameaças STRIDE válidas, superando analistas humanos juniores em cobertura de riscos comuns de rede e autenticação.

**Contribuições Centrais:**
- Pipeline empírico de adaptação de LLMs para modelagem de ameaças STRIDE.
- Benchmark comparativo entre LLMs de código aberto e proprietários.
- Taxonomia de erros e alucinações em elicitação automatizada de segurança.

## ⚠️ Limitações Identificadas
Risco de alucinação de ameaças inexistentes em componentes arquiteturais não convencionais ou padrões criptográficos modernos.

## 🗺️ Mapa Conceitual
- **Conceitos-Chave:** `Modelagem de Ameaças`, `STRIDE`, `LLMs Especializados`, `Automação de Segurança`
- **Problemas Focais:** `Processo manual lento e propenso a omissões de segurança`
- **Métodos Empregados:** `Ajuste fino de LLMs em segurança`, `Engenharia de prompts estruturada`, `Validação por especialistas`
- **Modelos e Arquiteturas:** `Llama-3 Adaptado`, `Mistral`, `GPT-4`
- **Bases de Dados:** `Casos de teste STRIDE`
- **Resultados Chave:** `87.1% de revocação em ameaças de arquitetura`
- **Limitações Reconhecidas:** `Alucinações pontuais em componentes raros`
- **Evidências Citáveis:** `EVID_039_01`

## 🔗 Relações na Base de Conhecimento

### Relações Ativas Declaradas (Outgoing)
- **Relacionado:**
  - [[artigo_003]] — *AI-enabled scientific revolution in the age of generative AI: second NSF workshop report*
  - [[artigo_035]] — *TRACE: Timely Retrieval and Alignment for Cybersecurity Knowledge Graph Construction and Expansion*

### Citações e Relações Recebidas na Base (Incoming)
- **Relacionado:**
  - [[artigo_035]] — *TRACE: Timely Retrieval and Alignment for Cybersecurity Knowledge Graph Construction and Expansion*

## 🎓 Integração com a Tese ALF-MoE

## 📖 Evidências Literais Extraídas (Fidelidade Rigorosa)

### `EVID_039_01` — METODOLÓGICA
> [!quote] EVID_039_01 (Relevância: 4/5 | Grau: Sustenta a afirmação)
> **Afirmação Sustentada:** A modelagem sistemática de ameaças categoriza os riscos estruturais de sistemas cibernéticos e orienta a cobertura requerida por mecanismos de defesa e NIDS.
> **Localização:** Seção 2 (Background on Threat Modelling and STRIDE), Páginas 2-4
>
> *"Threat modelling frameworks systematically delineate adversarial objectives—such as spoofing, tampering, and denial-of-service—providing the foundational requirements against which anomaly detection architectures must be scoped."*
>
> **Aplicabilidade na Tese ALF-MoE:** Útil para contextualizar as categorias de ameaças abrangidas pelo NIDS no capítulo de introdução e fundamentação.

## 📦 Entrada BibTeX
```bibtex
@article{threatmodelling2025,
  title = {Threat Modelling using Domain-Adapted Language Models: Empirical Evaluation and Insights},
  author = {Pourhanifeh, Saba and Abdulghaffar, Abdulaziz and Matrawy, Ashraf},
  journal = {arXiv preprint arXiv:2605.10808},
  year = {2026}
}
```

## 🧭 Navegação
- ⬅️ [[00_Indice_Bibliografico|Índice Geral de Artigos]]
- 🧠 [[Conceitos_Centrais|Conceitos Centrais da Base]]
- ⚡ [[Contradicoes_e_Divergencias|Contradições e Divergências da Literatura]]
- 🕸️ [[Rede_Intelectual|Rede Intelectual e Cadeias Epistemológicas]]
- 📋 [[Afirmacoes_e_Claims|Afirmações e Claims Acadêmicos]]
- 📑 [[BASE_DE_CONHECIMENTO_COMPLETA|Dossiê Completo da Base]]
