---
id: artigo_016
title: Empirical Analysis of Web Attacks
authors:
- Daljit Kaur
- Parminder Kaur
year: 2016
bibtex_key: webattacks2024
doi: 10.1016/j.procs.2016.02.057
venue: Procedia Computer Science 78 (2016) 298 – 306
keywords:
- Web Attacks
- SQL Injection
- Cross-Site Scripting (XSS)
- Empirical Analysis
- Vulnerability Assessment
- HTTP Traffic
area: Web Application Security / Empirical Attack Analysis
datasets:
- Logs reais de tráfego HTTP corporativo
- Bancos de dados de exploração controlada
models:
- Análise Estatística Descritiva
- Matching de Expressões Regulares
- Clustering Não Supervisionado
aliases:
- Empirical Analysis of Web Attacks
- webattacks2024
- artigo_016
tags:
- bibliografia
- alf-moe
- artigo
---

# Empirical Analysis of Web Attacks

> **Citação ABNT Sugerida:** KAUR, D.; KAUR, P.. Empirical Analysis of Web Attacks. In: **Procedia Computer Science 78 (2016) 298 – 306**, 2016.
> **Chave BibTeX:** `webattacks2024` | **Arquivo TXT:** `Empirical_Analysis_of_Web_Attacks.txt` | **DOI:** `10.1016/j.procs.2016.02.057`

---

## 📌 Metadados e Classificação
| Atributo | Detalhe |
| :--- | :--- |
| **Identificador** | `artigo_016` |
| **Ano** | 2016 |
| **Área de Pesquisa** | Web Application Security / Empirical Attack Analysis |
| **Veículo de Publicação** | Procedia Computer Science 78 (2016) 298 – 306 |
| **Datasets Utilizados** | Logs reais de tráfego HTTP corporativo, Bancos de dados de exploração controlada |
| **Modelos / Algoritmos** | Análise Estatística Descritiva, Matching de Expressões Regulares, Clustering Não Supervisionado |
| **Palavras-Chave** | Web Attacks, SQL Injection, Cross-Site Scripting (XSS), Empirical Analysis, Vulnerability Assessment, HTTP Traffic |

## 🎯 Problema Abordado
Aplicações web corporativas enfrentam constantes tentativas de exploração via injeção e manipulação de parâmetros nos cabeçalhos e URLs HTTP, necessitando de caracterização empírica de padrões de ataque.

## 🔬 Metodologia
Análise quantitativa de tráfego de requisições HTTP e logs de servidores web capturados em ambientes de produção e testes de invasão; categorização de ataques por vetor de entrada e perfil de carga.

## 🏆 Principais Resultados e Contribuições
**Resultados Principais:**
Identificação de que SQL Injection (SQLi) e Cross-Site Scripting (XSS) correspondem a mais de 65% das explorações web automatizadas, apresentando padrões periódicos repetitivos gerados por scanners automatizados (como sqlmap e Nikto).

**Contribuições Centrais:**
- Caracterização quantitativa empírica das principais classes de ataques a aplicações web.
- Demonstração do perfil comportamental gerado por ferramentas automatizadas de exploração.
- Análise da distribuição de frequência de requisições maliciosas.

## ⚠️ Limitações Identificadas
Foco restrito à camada de aplicação HTTP clássica sem considerar tráfego encapsulado em túneis TLS contemporâneos ou tráfego HTTP/2 e HTTP/3.

## 🗺️ Mapa Conceitual
- **Conceitos-Chave:** `Web Application Attacks`, `SQL Injection`, `XSS`, `Automated Scanning Patterns`
- **Problemas Focais:** `Vulnerabilidades prevalentes na camada web`, `Exploração automatizada em massa`
- **Métodos Empregados:** `Análise empírica de logs`, `Extração de padrões de URL/cabeçalho`
- **Modelos e Arquiteturas:** `Classificação estatística descritiva`
- **Bases de Dados:** `Logs de requisições HTTP`
- **Resultados Chave:** `SQLi e XSS dominam 65% dos incidentes web`, `Scanners exibem cadência periódica estrita`
- **Limitações Reconhecidas:** `Não examina tráfego cifrado opaco`
- **Evidências Citáveis:** `EVID_016_01`

## 🔗 Relações na Base de Conhecimento

### Relações Ativas Declaradas (Outgoing)
- **Relacionado:**
  - [[artigo_046]] — *Web Attacks Analysis and Mitigation Techniques*

### Citações e Relações Recebidas na Base (Incoming)
- **Relacionado:**
  - [[artigo_046]] — *Web Attacks Analysis and Mitigation Techniques*

## 🎓 Integração com a Tese ALF-MoE

## 📖 Evidências Literais Extraídas (Fidelidade Rigorosa)

### `EVID_016_01` — EMPÍRICA
> [!quote] EVID_016_01 (Relevância: 4/5 | Grau: Sustenta a afirmação)
> **Afirmação Sustentada:** Ataques e varreduras contra aplicações web gerados por ferramentas automatizadas manifestam ciclicidade e periodicidade evidente na taxa de requisições.
> **Localização:** Seção 4 (Empirical Observations and Analysis), Páginas 302-304
>
> *"Automated web application vulnerability scanners exhibit pronounced burstiness and periodic request patterns characterized by regular inter-request intervals during automated fuzzing campaigns."*
>
> **Aplicabilidade na Tese ALF-MoE:** Sustenta a caracterização no Capítulo 1 de que abusos web e varreduras apresentam ciclicidade e padrões espectrais identificáveis.

## 📦 Entrada BibTeX
```bibtex
@article{webattacks2024,
  title = {Empirical Analysis of Web Attacks},
  author = {Kaur, Daljit and Kaur, Parminder},
  journal = {Procedia Computer Science},
  year = {2016},
  doi = {10.1016/j.procs.2016.02.057},
  volume = {78},
  pages = {298-306},
  publisher = {Elsevier BV}
}
```

## 🧭 Navegação
- ⬅️ [[00_Indice_Bibliografico|Índice Geral de Artigos]]
- 🧠 [[Conceitos_Centrais|Conceitos Centrais da Base]]
- ⚡ [[Contradicoes_e_Divergencias|Contradições e Divergências da Literatura]]
- 🕸️ [[Rede_Intelectual|Rede Intelectual e Cadeias Epistemológicas]]
- 📋 [[Afirmacoes_e_Claims|Afirmações e Claims Acadêmicos]]
- 📑 [[BASE_DE_CONHECIMENTO_COMPLETA|Dossiê Completo da Base]]
