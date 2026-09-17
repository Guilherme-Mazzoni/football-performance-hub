import streamlit as st
import plotly.express as px
from src.data.data_loader import get_kpis_gerais
from src.analytics.player_clustering import perform_clustering

def render_visao_geral():
    try:
        kpis = get_kpis_gerais()
        
        # Row 1: KPIs Ofensivos e Gerais
        # KPIs com layout Premium Glassmorphism
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div class="glass-card">
                <p data-testid="stMetricLabel">Gols Pró</p>
                <p data-testid="stMetricValue">{kpis.get('gols', 0)}</p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f"""
            <div class="glass-card">
                <p data-testid="stMetricLabel">Expectativa de Gols (xG)</p>
                <p data-testid="stMetricValue">{kpis.get('xg', 0)}</p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="glass-card">
                <p data-testid="stMetricLabel">Assistências</p>
                <p data-testid="stMetricValue">{kpis.get('assistencias', 0)}</p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f"""
            <div class="glass-card">
                <p data-testid="stMetricLabel">Expectativa de Assist. (xA)</p>
                <p data-testid="stMetricValue">{kpis.get('xa', 0)}</p>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="glass-card">
                <p data-testid="stMetricLabel">Desempenho (Vitórias)</p>
                <p data-testid="stMetricValue">{kpis.get('vitorias', 0)}</p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f"""
            <div class="glass-card">
                <p data-testid="stMetricLabel">Derrotas</p>
                <p data-testid="stMetricValue">{kpis.get('derrotas', 0)}</p>
            </div>
            """, unsafe_allow_html=True)
            pontos = (kpis.get('vitorias', 0) * 3) + kpis.get('empates', 0)
            st.markdown(f"""
            <div class="glass-card">
                <p data-testid="stMetricLabel">Pontos Ganhos</p>
                <p data-testid="stMetricValue">{pontos}</p>
            </div>
            """, unsafe_allow_html=True)
        
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
