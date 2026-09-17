import streamlit as st
import pandas as pd
import plotly.graph_objects as go
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
                fig_pitch = go.Figure()
                
                # Desenhando metade do campo com Plotly shapes (super leve)
                fig_pitch.add_shape(type="rect", x0=60, y0=0, x1=120, y1=80, line=dict(color="#E0E0E0", width=2), layer="below") # Campo
                fig_pitch.add_shape(type="line", x0=60, y0=0, x1=60, y1=80, line=dict(color="#E0E0E0", width=2), layer="below") # Meio campo
                fig_pitch.add_shape(type="circle", x0=50, y0=30, x1=70, y1=50, line=dict(color="#E0E0E0", width=2), layer="below") # Circulo central
                fig_pitch.add_shape(type="rect", x0=102, y0=18, x1=120, y1=62, line=dict(color="#E0E0E0", width=2), layer="below") # Grande area
                fig_pitch.add_shape(type="rect", x0=114, y0=30, x1=120, y1=50, line=dict(color="#E0E0E0", width=2), layer="below") # Pequena area
                fig_pitch.add_shape(type="circle", x0=107.5, y0=39.5, x1=108.5, y1=40.5, fillcolor="#E0E0E0", line_color="#E0E0E0", layer="below") # Marca do penalti
                fig_pitch.add_shape(type="path", path="M 102 30 C 95 30, 95 50, 102 50", line=dict(color="#E0E0E0", width=2), layer="below") # Meia lua
                
                # Adicionando os chutes
                cores = {'Gol': '#D4AF37', 'Chute': '#888888'}
                for tipo in ['Chute', 'Gol']:
                    chutes_tipo = chutes_atleta[chutes_atleta['tipo'] == tipo]
                    if not chutes_tipo.empty:
                        tamanhos = chutes_tipo['xg'].fillna(0.1) * 60 # Escala para Plotly
                        
                        fig_pitch.add_trace(go.Scatter(
                            x=chutes_tipo['x'], y=chutes_tipo['y'],
                            mode='markers',
                            name=tipo,
                            marker=dict(size=tamanhos, color=cores[tipo], opacity=0.8, line=dict(width=1, color='#121212')),
                            hovertext=[f"xG: {xg:.2f}" for xg in chutes_tipo['xg']],
                            hoverinfo="text+name"
                        ))
                
                fig_pitch.update_layout(
                    xaxis=dict(visible=False, range=[60, 122]),
                    yaxis=dict(visible=False, range=[-2, 82]),
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    margin=dict(l=0, r=0, t=10, b=10),
                    showlegend=True,
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                )
                
                st.plotly_chart(fig_pitch, use_container_width=True, config={'displayModeBar': False})
                st.caption("O tamanho do círculo representa o xG (expectativa de gol).")
                
    except Exception as e:
        st.error(f"Erro ao carregar os dados de elenco: {e}")
