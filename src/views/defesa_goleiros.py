import streamlit as st
import pandas as pd
import plotly.express as px
from src.data.data_loader import get_player_stats, load_times_fbref

def render_defesa_goleiros():
    try:
        times = load_times_fbref()
        df_stats = get_player_stats()
        
        if times.empty or df_stats.empty:
            st.warning("Sem dados defensivos disponíveis. Execute o extrator do FBref.")
            return
            
        goleiros = df_stats[df_stats['posicao'].str.contains('GK', na=False)]
        
        # O FBref em sua extração standard foca mais em ações de linha. 
        # Para ter defesas precisas precisaríamos do stat_type="keepers".
        # Vamos focar na visão coletiva das equipes para o portfólio.
        
        # Identificando a coluna de gols contra no dataset do time
        cols = times.columns.tolist()
        col_ga = next((c for c in cols if c in ['goals_against', 'ga']), None)
        col_cs = next((c for c in cols if c in ['clean_sheets', 'cs']), None)
        
        gols_sofridos = int(times[col_ga].sum()) if col_ga else 0
        clean_sheets = int(times[col_cs].sum()) if col_cs else 0
        
        st.subheader("Performance Defensiva do Campeonato")
        col1, col2, col3 = st.columns(3)
        col1.metric("Gols Sofridos (Total Liga)", gols_sofridos)
        col2.metric("Clean Sheets (Total Liga)", clean_sheets)
        
        # Exibindo goleiros listados
        st.metric("Goleiros Registrados", len(goleiros))
        
        st.markdown("---")
        
        st.subheader("Gols Sofridos por Equipe")
        if col_ga:
            fig = px.bar(
                times.sort_values(by=col_ga, ascending=True), 
                x='team', y=col_ga, 
                text=col_ga,
                labels={'team': 'Equipe', col_ga: 'Gols Sofridos'},
                title="Ranking de Defesas Vazadas"
            )
            fig.update_traces(marker_color='#AAAAAA')
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#E0E0E0")
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Dado de gols sofridos por equipe não disponível nesta extração.")

    except Exception as e:
        st.error(f"Erro ao carregar os dados de defesa: {e}")
