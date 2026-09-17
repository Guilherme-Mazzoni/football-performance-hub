import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from mplsoccer import Pitch
import matplotlib.pyplot as plt
from src.data.data_loader import get_player_stats, load_eventos_df

def render_elenco():
    st.title("Análise de Elenco")
    
    try:
        df_stats = get_player_stats()
        df_linha = df_stats[df_stats['posicao'] != 'Goleiro']
        
        if df_linha.empty:
            st.warning("Sem dados de jogadores de linha.")
            return

        # Sidebar filter
        st.sidebar.subheader("Filtro de Atleta")
        jogador_nome = st.sidebar.selectbox("Selecione um Jogador:", df_linha['nome'].sort_values())
        
        atleta_data = df_linha[df_linha['nome'] == jogador_nome].iloc[0]
        atleta_id = atleta_data['id']
        
        # Profile Card
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown(f"""
            <div class="player-card">
                <h3>{atleta_data['nome']}</h3>
                <p>#{atleta_data['numero']} | {atleta_data['posicao']}</p>
                <hr>
                <p>Idade: {atleta_data['idade']}</p>
                <p>Minutos: {atleta_data['minutos_jogados']}</p>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.subheader("Métricas Absolutas")
            m1, m2, m3 = st.columns(3)
            m1.metric("Gols", int(atleta_data['gols']), f"xG: {atleta_data['xg_total']:.2f}")
            m2.metric("Assistências", int(atleta_data['assistencias']), f"xA: {atleta_data['xa_total']:.2f}")
            m3.metric("Chutes", int(atleta_data['chutes']))
            
        st.markdown("---")
        
        # Viz avançada
        st.subheader("Deep Dive Analítico")
        v1, v2 = st.columns(2)
        
        with v1:
            st.markdown("#### Radar de Desempenho vs Média da Liga (por 90')")
            
            # Media do time
            media_time = df_linha[['gols_90', 'assist_90', 'xg_90', 'xa_90']].mean()
            
            fig = go.Figure()
            categories = ['Gols', 'Assist.', 'xG', 'xA']
            
            fig.add_trace(go.Scatterpolar(
                  r=[atleta_data['gols_90'], atleta_data['assist_90'], atleta_data['xg_90'], atleta_data['xa_90']],
                  theta=categories,
                  fill='toself',
                  name=atleta_data['nome'],
                  line_color='#D4AF37'
            ))
            fig.add_trace(go.Scatterpolar(
                  r=[media_time['gols_90'], media_time['assist_90'], media_time['xg_90'], media_time['xa_90']],
                  theta=categories,
                  fill='toself',
                  name='Média do Elenco',
                  line_color='#888888'
            ))
            
            fig.update_layout(
              polar=dict(
                radialaxis=dict(visible=True, range=[0, max(atleta_data[['gols_90', 'assist_90', 'xg_90', 'xa_90']].max(), 0.5) * 1.2]),
                bgcolor='rgba(0,0,0,0)'
              ),
              showlegend=True,
              paper_bgcolor="rgba(0,0,0,0)",
              font=dict(color="#E0E0E0")
            )
            st.plotly_chart(fig, use_container_width=True)
            
        with v2:
            st.markdown("#### Mapa de Finalizações (Shot Map)")
            eventos = load_eventos_df()
            # Puxar chutes do atleta
            chutes_atleta = eventos[(eventos['jogador_id'] == atleta_id) & (eventos['tipo'].isin(['Chute', 'Gol']))]
            
            if chutes_atleta.empty:
                st.info("O jogador não possui registros de chutes no campeonato.")
            else:
                pitch = Pitch(pitch_type='statsbomb', pitch_color='#1e1e1e', line_color='#E0E0E0', half=True)
                fig_pitch, ax = pitch.draw(figsize=(6, 4))
                fig_pitch.set_facecolor('#121212')
                
                for _, row in chutes_atleta.iterrows():
                    color = '#D4AF37' if row['tipo'] == 'Gol' else '#888888'
                    size = row['xg'] * 500 if pd.notnull(row['xg']) else 100
                    pitch.scatter(row['x'], row['y'], s=size, c=color, alpha=0.8, edgecolors='#121212', ax=ax, label=row['tipo'])
                    
                st.pyplot(fig_pitch)
                st.caption("O tamanho do círculo representa o xG (expectativa de gol). Dourado indica Gol.")
                
    except Exception as e:
        st.error(f"Erro ao carregar os dados de elenco: {e}")
