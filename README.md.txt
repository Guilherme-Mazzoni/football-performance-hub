# 🛡️ Performance Hub: Inteligência Esportiva & Análise de Desempenho

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=flat&logo=plotly&logoColor=white)

Painel executivo de análise de desempenho da temporada de futebol, integrando métricas tradicionais (gols, assistências, cartões) a indicadores avançados de expectativa ($xG$, $xA$, saldo esperado e eficiência de finalização). O projeto replica a interface de departamentos profissionais de análise de desempenho e scouting.

---

## 📌 Arquitetura Visual e Módulos do Sistema

O hub divide-se em três visões analíticas navegáveis via menu lateral:

1. **Visão Geral (Coletivo):**
   - **Cartões de KPIs:** Gols, assistências, participações diretas, nota média, $xG$ total, $xA$ total e disciplina (amarelos/vermelhos).
   - **Campanha do Campeonato:** Vitórias, empates, derrotas, pontos, gols pró e contra.
   - **Ranking Interno:** Principais criadores e finalizadores por participações em gols.
   - **Eficiência Ofensiva:** Gráfico comparativo entre produção real (gols/assistências) versus expectativa ($xG$/$xA$).

2. **Elenco (Jogadores de Linha):**
   - Seletor dinâmico por atleta com card de identificação (foto, posição e número).
   - Métricas de volume: jogos disputados, gols, assistências e nota média.
   - Diagnóstico de letalidade: métricas de $xG$, $xA$, diferença de gols/$xG$ (over/underperformance) e assistências/$xA$.

3. **Defesa & Goleiros:**
   - Painel específico para a meta: defesas totais, média de defesas por partida, gols sofridos e *clean sheets* (jogos sem sofrer gols).

---

## 🏗️ Engenharia de Dados & ETL

### Fontes de Dados
- **Métricas Avançadas e Estatísticas:** Extraídas via `soccerdata` (módulo FBref/Opta) ou APIs de eventos consolidados (API-Football / Sofascore).
- **Mídia e Atributos Visuais:** Imagens de atletas, fotos institucionais e escudos indexados via links estáticos ou CDN local.

### Estrutura Relacional do Dataset

| Tabela / Estrutura | Finalidade | Campos-Chave |
| :--- | :--- | :--- |
| `dim_jogadores` | Cadastro do elenco | `id_jogador`, `nome`, `posicao`, `numero`, `foto_url` |
| `fato_desempenho_geral` | Métricas consolidadas da temporada | `id_jogador`, `jogos`, `gols`, `assistencias`, `xg`, `xa`, `nota_media` |
| `fato_goleiros` | Scouts de proteção de meta | `id_jogador`, `defesas`, `defesas_por_jogo`, `gols_sofridos`, `clean_sheets` |
| `dim_campanha` | Dados macro do clube no torneio | `vitorias`, `empates`, `derrotas`, `pontos`, `gols_pro`, `gols_contra` |

---

## 📂 Estrutura do Repositório

```text
performance-hub/
├── assets/
│   ├── logos/              # Escudos e marcas em alta definição
│   ├── players/            # Fotos dos atletas (formato PNG transparente)
│   └── custom.css          # Estilização CSS personalizada (dark gold theme)
├── data/
│   └── dados_temporada.json # Base consolidada de métricas do clube e atletas
├── src/
│   └── etl_pipeline.py     # Script de extração e higienização dos scouts
├── app.py                  # Aplicação modular Streamlit
├── requirements.txt
└── README.md