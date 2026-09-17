import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from src.data.data_loader import get_player_stats

def render_elenco(jogador_nome_externo=None):
    try:
        df_stats = get_player_stats()
        
        if df_stats.empty:
            st.warning("Nenhum dado de jogador encontrado.")
            return

        # Filtra apenas jogadores de linha
        df_linha = df_stats[df_stats['posicao'] != 'GK']
        if df_linha.empty:
            df_linha = df_stats

        if jogador_nome_externo is None:
            jogador_nome = st.selectbox("Selecione um Jogador:", df_linha['nome'].sort_values())
        else:
            jogador_nome = jogador_nome_externo
        
        atleta_data = df_linha[df_linha['nome'] == jogador_nome].iloc[0]
        
        # Profile Card
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown(f"""
            <div class="glass-card">
                <h3>{atleta_data['nome']}</h3>
                <p>{atleta_data['time']} | {atleta_data['posicao']}</p>
                <hr style="border-color: rgba(255,255,255,0.1)">
                <p>Idade: {atleta_data.get('idade', 'N/A')}</p>
                <p>Minutos: {atleta_data['minutos_jogados']}</p>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.subheader("Métricas Absolutas (Temporada)")
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Gols", int(atleta_data['gols']), f"xG: {atleta_data['xg_total']:.2f}")
            m2.metric("Assistências", int(atleta_data['assistencias']), f"xA: {atleta_data['xa_total']:.2f}")
            
            prgp = int(atleta_data.get('progress_passes', 0))
            prgc = int(atleta_data.get('progress_carries', 0))
            
            m3.metric("Passes Progressivos", prgp)
            m4.metric("Conduções Progressivas", prgc)
            
        st.markdown("---")
        
        # Viz avançada - Radar Expansion
        st.subheader("Radar de Desempenho (Métricas por 90 Minutos)")
        st.markdown("Comparativo do jogador selecionado contra a média geral dos jogadores de linha do campeonato.")
        
        media_liga = df_linha.mean(numeric_only=True)
        
        fig = go.Figure()
        
        # Selecionando as colunas que alimentam o radar
        # Verificando as que de fato vieram no dataframe
        cols_radar = []
        nomes_radar = []
        
        mapeamento = {
            'gols_90': 'Gols',
            'assist_90': 'Assistências',
            'xg_90': 'xG',
            'xa_90': 'xA',
            'progress_passes_90': 'Passes Progressivos',
            'progress_carries_90': 'Conduções Progressivas',
            'cards_yellow_90': 'Cartões Amarelos'
        }
        
        for k, v in mapeamento.items():
            if k in df_linha.columns:
                cols_radar.append(k)
                nomes_radar.append(v)
                
        if cols_radar:
            valores_atleta = [atleta_data[c] for c in cols_radar]
            valores_media = [media_liga[c] for c in cols_radar]
            
            fig.add_trace(go.Scatterpolar(
                  r=valores_atleta,
                  theta=nomes_radar,
                  fill='toself',
                  name=atleta_data['nome'],
                  line_color='#FFFFFF'
            ))
            fig.add_trace(go.Scatterpolar(
                  r=valores_media,
                  theta=nomes_radar,
                  fill='toself',
                  name='Média do Campeonato',
                  line_color='#888888'
            ))
            
            # Ajustando o visual do radar para o tema Dark Gold e centralizando na tela (bem maior e mais limpo)
            fig.update_layout(
              polar=dict(
                radialaxis=dict(visible=True, showline=False, gridcolor='#333333'),
                angularaxis=dict(gridcolor='#333333'),
                bgcolor='rgba(0,0,0,0)'
              ),
              showlegend=True,
              paper_bgcolor="rgba(0,0,0,0)",
              font=dict(color="#E0E0E0", size=14),
              height=600 # Altura maior para ficar mais imponente
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Métricas insuficientes para desenhar o Radar Chart. Tente extrair mais dados do FBref.")
                
    except Exception as e:
        st.error(f"Erro ao carregar os dados de elenco: {e}")
