import streamlit as st
import os

# Configuração da Página - DEVE SER O PRIMEIRO COMANDO STREAMLIT
st.set_page_config(
    page_title="Performance Hub - Inteligência Esportiva",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

def load_css():
    css_path = os.path.join(os.path.dirname(__file__), "assets", "custom.css")
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Injetar o CSS
load_css()

import pandas as pd
from src.data.data_loader import get_player_stats

# Header - Logo do Clube usando o arquivo SVG local
col_logo, col_title = st.columns([1, 8])

with col_logo:
    try:
        import base64
        with open("assets/photos/atletico.svg", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
            st.markdown(
                f'''
                <div style="text-align: center;">
                    <img src="data:image/svg+xml;base64,{encoded_string}" width="70" style="filter: drop-shadow(0px 0px 5px rgba(255,255,255,0.3)); margin-top: 10px;">
                </div>
                ''', 
                unsafe_allow_html=True
            )
    except FileNotFoundError:
        st.markdown("🛡️")
    except:
        st.markdown("🛡️")

with col_title:
    st.title("Galo Performance Hub")
    st.markdown("Dashboard tático e estatístico desenvolvido com dados avançados e Inteligência Artificial.")

st.markdown("---")

# Navegação Principal (Substituindo Tabs para controle dinâmico da Sidebar)
menu_selecionado = st.radio(
    "Navegação",
    ["📊 Visão Geral", "🏃‍♂️ Análise de Elenco", "🧤 Defesa e Goleiros"],
    horizontal=True,
    label_visibility="collapsed"
)

st.markdown("---")

df_stats = get_player_stats()
jogador_selecionado = None

# A Sidebar (Perfil do Jogador) só aparece na Análise de Elenco
if menu_selecionado == "🏃‍♂️ Análise de Elenco":
    if not df_stats.empty:
        df_linha = df_stats[df_stats['posicao'] != 'GK']
        if df_linha.empty:
            df_linha = df_stats
            
        st.sidebar.subheader("Filtro de Atleta")
        jogador_selecionado = st.sidebar.selectbox("Selecione um Jogador:", df_linha['nome'].sort_values(), key="global_player")
        
        # Renderizar Foto
        base_photo_path = f"assets/photos/{jogador_selecionado}"
        extensions = [".png", ".webp", ".jpg", ".jpeg"]
        
        photo_path = None
        for ext in extensions:
            if os.path.exists(base_photo_path + ext):
                photo_path = base_photo_path + ext
                break
        
        # Dicionário de números dos jogadores do Galo
        numeros_camisa = {
            'Hulk': 7, 'Paulinho': 10, 'Gustavo Scarpa': 6, 'Guilherme Arana': 13,
            'Matías Zaracho': 15, 'Rodrigo Battaglia': 21, 'Otávio': 5, 'Alan Franco': 23,
            'Bruno Fuchs': 3, 'Renzo Saravia': 26, 'Igor Gomes': 17, 'Eduardo Vargas': 11,
            'Alisson': 45, 'Everson': 22
        }
        numero = numeros_camisa.get(jogador_selecionado, 99)
        
        if photo_path:
            import base64
            with open(photo_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode()
                mime_type = "image/" + photo_path.split('.')[-1].replace('jpg', 'jpeg')
                img_html = f'''
                <div class="profile-wrapper">
                    <div class="profile-ring"><img src="data:{mime_type};base64,{encoded_string}"></div>
                    <div class="profile-number">{numero}</div>
                </div>
                '''
        else:
            # Silhueta de Fallback
            img_html = f'''
            <div class="profile-wrapper">
                <div class="profile-ring"><span class="profile-ring-fallback">👤</span></div>
                <div class="profile-number">{numero}</div>
            </div>
            '''
                
        st.sidebar.markdown(img_html, unsafe_allow_html=True)
        st.sidebar.markdown("---")
        st.sidebar.caption("Adicione fotos em PNG recortadas na pasta `assets/photos/` para customizar!")

# Roteamento das views baseado no menu selecionado
if menu_selecionado == "📊 Visão Geral":
    from src.views.visao_geral import render_visao_geral
    render_visao_geral()

elif menu_selecionado == "🏃‍♂️ Análise de Elenco":
    from src.views.elenco import render_elenco
    # Passamos o jogador selecionado
    render_elenco(jogador_selecionado if not df_stats.empty else None)

elif menu_selecionado == "🧤 Defesa e Goleiros":
    from src.views.defesa_goleiros import render_defesa_goleiros
    render_defesa_goleiros()
