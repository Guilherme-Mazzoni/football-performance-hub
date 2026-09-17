import streamlit as st
import plotly.express as px
from src.data.data_loader import get_kpis_gerais
from src.analytics.player_clustering import perform_clustering

def render_visao_geral():
    st.title("Visão Geral do Clube")
    st.markdown("Acompanhamento de KPIs Coletivos e Segmentação do Elenco")

    try:
        kpis = get_kpis_gerais()
        
        # Row 1: KPIs Ofensivos e Gerais
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Gols Pró", f"{kpis['gols']}")
        col2.metric("Assistências", f"{kpis['assistencias']}")
        col3.metric("Expectativa de Gols (xG)", f"{kpis['xg_total']}")
        col4.metric("Expectativa de Assist. (xA)", f"{kpis['xa_total']}")

        st.markdown("<br>", unsafe_allow_html=True)
        
        # Row 2: Campanha
        st.subheader("Desempenho no Campeonato")
        col_v, col_e, col_d, col_p = st.columns(4)
        col_v.metric("Vitórias", kpis['vitorias'])
        col_e.metric("Empates", kpis['empates'])
        col_d.metric("Derrotas", kpis['derrotas'])
        pontos = (kpis['vitorias'] * 3) + kpis['empates']
        col_p.metric("Pontos Ganhos", pontos)
        
        st.markdown("---")
        
        # Row 3: Inteligência / ML
        st.subheader("Segmentação de Elenco (K-Means Clustering)")
        st.write("Agrupamento de jogadores de linha por estilos de jogo com base na produção ofensiva por 90 minutos.")
        
        df_clusters = perform_clustering()
        if 'cluster' in df_clusters.columns:
            fig = px.scatter(
                df_clusters, x="xg_90", y="xa_90", 
                color="perfil_cluster", hover_name="nome",
                size="minutos_jogados",
                labels={"xg_90": "xG a cada 90 min", "xa_90": "xA a cada 90 min", "perfil_cluster": "Perfil"},
                title="Distribuição de Perfis Ofensivos no Elenco"
            )
            # Customizando para dark mode e tema do hub
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#E0E0E0")
            )
            st.plotly_chart(fig, use_container_width=True)
            
            with st.expander("Ver dados do modelo"):
                st.dataframe(df_clusters[['nome', 'posicao', 'minutos_jogados', 'xg_90', 'xa_90', 'perfil_cluster']].sort_values('xg_90', ascending=False))
        else:
            st.warning("Dados insuficientes para rodar o modelo de clustering.")

    except Exception as e:
        st.error(f"Erro ao carregar dados da visão geral: {e}")
        st.info("Execute o extrator de dados do FBref (src/data/etl_fbref.py) para popular o banco de dados local.")
