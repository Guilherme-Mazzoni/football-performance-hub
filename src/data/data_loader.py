import pandas as pd
import streamlit as st
from sqlalchemy.orm import Session
from src.data.database import engine, Jogador, Partida, Evento
from sqlalchemy import text

@st.cache_data(ttl=3600)
def load_jogadores_df():
    query = "SELECT * FROM jogadores"
    df = pd.read_sql_query(query, engine)
    return df

@st.cache_data(ttl=3600)
def load_eventos_df():
    query = "SELECT * FROM eventos"
    df = pd.read_sql_query(query, engine)
    return df

@st.cache_data(ttl=3600)
def load_partidas_df():
    query = "SELECT * FROM partidas"
    df = pd.read_sql_query(query, engine)
    return df

@st.cache_data(ttl=3600)
def get_kpis_gerais():
    eventos = load_eventos_df()
    partidas = load_partidas_df()
    
    gols = len(eventos[eventos['tipo'] == 'Gol'])
    assistencias = len(eventos[eventos['tipo'] == 'Assistência'])
    
    xg_total = eventos['xg'].sum()
    xa_total = eventos['xa'].sum()
    
    vitorias = partidas['vitoria'].sum()
    empates = partidas['empate'].sum()
    derrotas = partidas['derrota'].sum()
    
    return {
        "gols": gols,
        "assistencias": assistencias,
        "xg_total": round(xg_total, 2),
        "xa_total": round(xa_total, 2),
        "vitorias": vitorias,
        "empates": empates,
        "derrotas": derrotas
    }

@st.cache_data(ttl=3600)
def get_player_stats():
    jogadores = load_jogadores_df()
    eventos = load_eventos_df()
    
    # Agregar eventos por jogador
    stats = eventos.groupby('jogador_id').agg(
        gols=('tipo', lambda x: (x == 'Gol').sum()),
        assistencias=('tipo', lambda x: (x == 'Assistência').sum()),
        chutes=('tipo', lambda x: (x == 'Chute').sum()),
        passes_chave=('tipo', lambda x: (x == 'Passe Chave').sum()),
        xg_total=('xg', 'sum'),
        xa_total=('xa', 'sum')
    ).reset_index()
    
    # Merge com os dados do jogador
    df_merged = pd.merge(jogadores, stats, left_on='id', right_on='jogador_id', how='left').fillna(0)
    
    # Calcular métricas por 90 min
    df_merged['minutos_jogados'] = df_merged['minutos_jogados'].replace(0, 1) # Evitar divisão por zero
    df_merged['xg_90'] = (df_merged['xg_total'] / df_merged['minutos_jogados']) * 90
    df_merged['xa_90'] = (df_merged['xa_total'] / df_merged['minutos_jogados']) * 90
    df_merged['gols_90'] = (df_merged['gols'] / df_merged['minutos_jogados']) * 90
    df_merged['assist_90'] = (df_merged['assistencias'] / df_merged['minutos_jogados']) * 90
    
    return df_merged
