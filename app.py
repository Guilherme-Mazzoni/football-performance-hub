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

# Header - Hero Section com Vídeo de Fundo
try:
    import base64
    # Carregando Logo
    with open("assets/photos/atletico.svg", "rb") as f_svg:
        svg_base64 = base64.b64encode(f_svg.read()).decode()
    
    # Carregando Vídeo (Animação)
    with open("assets/photos/galo.animacao.mp4", "rb") as f_vid:
        vid_base64 = base64.b64encode(f_vid.read()).decode()
        
    hero_html = f"""
<div style="position: relative; overflow: hidden; border-radius: 12px; margin-bottom: 25px; height: 160px; display: flex; align-items: center; padding: 0 30px; border: 1px solid rgba(255,255,255,0.1); box-shadow: 0 4px 15px rgba(0,0,0,0.5);">
    <!-- Video Background -->
    <video autoplay loop muted playsinline style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; z-index: 0; filter: brightness(0.6);">
        <source src="data:video/mp4;base64,{vid_base64}" type="video/mp4">
    </video>
    
    <!-- Content overlay -->
    <div style="position: relative; z-index: 1; display: flex; align-items: center; width: 100%;">
        <div style="margin-right: 25px;">
            <img src="data:image/svg+xml;base64,{svg_base64}" width="90" style="filter: drop-shadow(0px 0px 15px rgba(255,255,255,0.5));">
        </div>
        <div>
            <h1 style="margin: 0; padding: 0; font-size: 2.5rem; color: #fff; font-weight: 800; letter-spacing: -1px; text-shadow: 2px 2px 8px rgba(0,0,0,0.9);">Galo Performance Hub</h1>
            <p style="margin: 5px 0 0 0; padding: 0; font-size: 1rem; color: #ddd; font-weight: 400; text-shadow: 1px 1px 4px rgba(0,0,0,0.9);">Dashboard tático e estatístico desenvolvido com dados avançados e Inteligência Artificial.</p>
        </div>
    </div>
</div>
"""
    st.markdown(hero_html, unsafe_allow_html=True)
except Exception as e:
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
