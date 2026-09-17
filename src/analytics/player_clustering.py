import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from src.data.data_loader import get_player_stats
import streamlit as st

@st.cache_data(ttl=3600)
def perform_clustering():
    df = get_player_stats()
    
    # Filtrar jogadores com mínimo de minutos para evitar outliers irreais
    df_filtered = df[(df['minutos_jogados'] > 90) & (df['posicao'] != 'Goleiro')].copy()
    
    if len(df_filtered) < 5:
        # Não há jogadores suficientes para clustering
        return df_filtered
        
    # Features selecionadas para o K-Means (Métricas por 90 min)
    features = ['xg_90', 'xa_90', 'gols_90', 'assist_90']
    
    X = df_filtered[features]
    
    # Padronizar os dados
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Aplicar K-Means (K=4 para identificar 4 perfis distintos)
    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    df_filtered['cluster'] = kmeans.fit_predict(X_scaled)
    
    # Nomear os clusters baseado na análise das médias dos centróides
    # Ex: o cluster com maior xG_90 é o Finalizador, maior xA_90 é o Criador
    cluster_centers = pd.DataFrame(scaler.inverse_transform(kmeans.cluster_centers_), columns=features)
    
    # Estratégia simples de nomeação
    # Cluster com maior xg_90 = Finalizador Nato
    # Cluster com maior xa_90 = Criador de Jogadas
    # Cluster com menores métricas = Defensivo/Apoio
    # O restante = Box-to-Box / Equilibrado
    
    idx_finalizador = cluster_centers['xg_90'].idxmax()
    idx_criador = cluster_centers['xa_90'].idxmax()
    idx_defensivo = cluster_centers[['xg_90', 'xa_90']].sum(axis=1).idxmin()
    
    # Lógica simples para rotular
    labels = {}
    for i in range(4):
        if i == idx_finalizador:
            labels[i] = "Finalizador Nato"
        elif i == idx_criador:
            labels[i] = "Criador de Jogadas"
        elif i == idx_defensivo:
            labels[i] = "Base / Defensivo"
        else:
            labels[i] = "Apoio Ofensivo / Equilibrado"
            
    df_filtered['perfil_cluster'] = df_filtered['cluster'].map(labels)
    
    return df_filtered
