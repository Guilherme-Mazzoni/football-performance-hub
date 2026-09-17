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

# Header Horizontal
col_logo, col_title = st.columns([1, 8])
with col_logo:
    try:
        st.image("assets/galo.png", width=80)
    except:
        st.markdown("🛡️")
with col_title:
    st.title("Galo Performance Hub")
    st.markdown("Dashboard tático e estatístico desenvolvido com dados avançados e Inteligência Artificial.")

st.markdown("---")

# Navegação Horizontal usando abas (tabs)
tab1, tab2, tab3 = st.tabs(["📊 Visão Geral", "🏃‍♂️ Análise de Elenco", "🧤 Defesa e Goleiros"])

with tab1:
    from src.views.visao_geral import render_visao_geral
    render_visao_geral()

with tab2:
    from src.views.elenco import render_elenco
    render_elenco()

with tab3:
    from src.views.defesa_goleiros import render_defesa_goleiros
    render_defesa_goleiros()
