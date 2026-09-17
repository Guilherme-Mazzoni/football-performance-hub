import streamlit as st
import pandas as pd
import plotly.express as px
from src.data.data_loader import load_jogadores_df, load_eventos_df, load_partidas_df

def render_defesa_goleiros():
    st.title("Defesa & Goleiros")
    
    try:
        jogadores = load_jogadores_df()
        eventos = load_eventos_df()
        partidas = load_partidas_df()
        
        goleiros = jogadores[jogadores['posicao'] == 'Goleiro']
        
        if goleiros.empty:
            st.warning("Sem dados de goleiros disponíveis.")
            return
            
        # Calcular defesas por goleiro
        defesas = eventos[eventos['tipo'] == 'Defesa']
        stats_goleiros = defesas.groupby('jogador_id').size().reset_index(name='defesas')
        stats_goleiros = pd.merge(goleiros, stats_goleiros, left_on='id', right_on='jogador_id', how='left').fillna(0)
        
        # Calcular gols sofridos totais do time (assumindo todos do goleiro titular para simplificar mock)
        gols_sofridos = partidas['gols_contra'].sum()
        clean_sheets = partidas[partidas['gols_contra'] == 0].shape[0]
        
        # Row 1: KPIs do time
        st.subheader("Performance Defensiva (Coletivo)")
        col1, col2, col3 = st.columns(3)
        col1.metric("Gols Sofridos", gols_sofridos)
        col2.metric("Clean Sheets (Jogos sem Sofrer Gols)", clean_sheets)
        col3.metric("Total de Defesas (Saves)", int(stats_goleiros['defesas'].sum()))
        
        st.markdown("---")
        
        # Row 2: Goleiros
        st.subheader("Análise de Goleiros")
        
        fig = px.bar(
            stats_goleiros, x='nome', y='defesas', 
            text='defesas',
            labels={'nome': 'Goleiro', 'defesas': 'Nº de Defesas'},
            title="Volume de Defesas por Goleiro"
        )
        fig.update_traces(marker_color='#D4AF37')
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#E0E0E0")
        )
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Erro ao carregar os dados de defesa: {e}")
