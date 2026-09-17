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

st.sidebar.title("🛡️ Performance Hub")
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Navegação:",
    ["Visão Geral", "Análise de Elenco", "Defesa e Goleiros"]
)

st.sidebar.markdown("---")
st.sidebar.info("Dashboard desenvolvido com dados simulados e modelos de Machine Learning.")

# Rotear para as visões correspondentes
if menu == "Visão Geral":
    from src.views.visao_geral import render_visao_geral
    render_visao_geral()
elif menu == "Análise de Elenco":
    from src.views.elenco import render_elenco
    render_elenco()
elif menu == "Defesa e Goleiros":
    from src.views.defesa_goleiros import render_defesa_goleiros
    render_defesa_goleiros()
