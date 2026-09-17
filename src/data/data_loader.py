import pandas as pd
import streamlit as st
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "performance.db")

@st.cache_data(ttl=3600)
def get_db_connection():
    return sqlite3.connect(DB_PATH)

@st.cache_data(ttl=3600)
def load_jogadores_fbref():
    conn = get_db_connection()
    try:
        query = "SELECT * FROM jogadores_fbref"
        df = pd.read_sql_query(query, conn)
        return df
    except Exception as e:
        st.error(f"Erro ao carregar banco de dados (Jogadores FBref): {e}")
        return pd.DataFrame()

@st.cache_data(ttl=3600)
def load_times_fbref():
    conn = get_db_connection()
    try:
        query = "SELECT * FROM times_fbref"
        df = pd.read_sql_query(query, conn)
        return df
    except Exception as e:
        st.error(f"Erro ao carregar banco de dados (Times FBref): {e}")
        return pd.DataFrame()

@st.cache_data(ttl=3600)
def get_kpis_gerais():
    times = load_times_fbref()
    jogadores = load_jogadores_fbref()
    
    if times.empty or jogadores.empty:
        return {"gols": 0, "assistencias": 0, "xg_total": 0, "xa_total": 0, "vitorias": 0, "empates": 0, "derrotas": 0}
        
    # Agregando dados de todos os times para os KPIs globais do campeonato (ou do primeiro time, dependendo da view)
    # Como o portfólio pode focar em análise do campeonato inteiro, vamos somar os totais
    
    # O FBref team stats tem colunas como 'goals', 'assists', 'xg', 'xg_assist' (ou 'xa')
    # O nome das colunas pode variar dependendo da extração, então tentamos os nomes mais comuns:
    
    def get_sum(df, possible_cols):
        for col in possible_cols:
            if col in df.columns:
                return df[col].sum()
        return 0

    gols = get_sum(times, ['goals', 'goals_for', 'gls'])
    assistencias = get_sum(times, ['assists', 'ast'])
    xg_total = get_sum(times, ['xg', 'expected_goals'])
    xa_total = get_sum(times, ['xg_assist', 'xa', 'xag'])
    
    vitorias = get_sum(times, ['wins', 'w'])
    empates = get_sum(times, ['draws', 'd'])
    derrotas = get_sum(times, ['losses', 'l'])
    
    return {
        "gols": int(gols),
        "assistencias": int(assistencias),
        "xg_total": round(xg_total, 2),
        "xa_total": round(xa_total, 2),
        "vitorias": int(vitorias),
        "empates": int(empates),
        "derrotas": int(derrotas)
    }

@st.cache_data(ttl=3600)
def get_player_stats():
    # Retorna o dataframe pronto para os gráficos
    df = load_jogadores_fbref()
    
    # Se não houver dados, retorna vazio
    if df.empty:
        return pd.DataFrame()
        
    # Garantir que as métricas principais existem com nomes padronizados para as views
    # Renomeando colunas padrão do fbref para o que as views esperam
    
    renames = {
        'player': 'nome',
        'position': 'posicao',
        'team': 'time',
        'age': 'idade',
        'minutes': 'minutos_jogados',
        'goals': 'gols',
        'assists': 'assistencias',
        'xg': 'xg_total',
        'xg_assist': 'xa_total',
        'xag': 'xa_total'
    }
    
    # Aplica renomeação caso a coluna exista
    for k, v in renames.items():
        if k in df.columns:
            df[v] = df[k]
            
    # Garantir colunas essenciais
    cols_to_fill = ['nome', 'posicao', 'minutos_jogados', 'gols', 'assistencias', 'xg_total', 'xa_total']
    for col in cols_to_fill:
        if col not in df.columns:
            df[col] = 0
            
    # Converter minutos para numérico
    df['minutos_jogados'] = pd.to_numeric(df['minutos_jogados'].replace(',', '', regex=True), errors='coerce').fillna(1)
    
    # Criação das colunas por 90 min (se não vierem prontas do FBref)
    df['minutos_jogados'] = df['minutos_jogados'].replace(0, 1)
    df['gols_90'] = (pd.to_numeric(df['gols'], errors='coerce').fillna(0) / df['minutos_jogados']) * 90
    df['assist_90'] = (pd.to_numeric(df['assistencias'], errors='coerce').fillna(0) / df['minutos_jogados']) * 90
    df['xg_90'] = (pd.to_numeric(df['xg_total'], errors='coerce').fillna(0) / df['minutos_jogados']) * 90
    df['xa_90'] = (pd.to_numeric(df['xa_total'], errors='coerce').fillna(0) / df['minutos_jogados']) * 90

    # Converter progress_passes, progress_carries e outras stats avançadas para numérico se existirem
    for c in ['progress_passes', 'progress_carries', 'tackles', 'cards_yellow', 'cards_red']:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)
            df[f'{c}_90'] = (df[c] / df['minutos_jogados']) * 90

    return df
