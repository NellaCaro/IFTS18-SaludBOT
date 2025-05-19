import streamlit as st
from chatbot_logic import manejar_estado
from utils import mostrar_mensajes
from data_manager import inicializar_estado

st.set_page_config(page_title="SaludBOT - Clínica SanVida", page_icon="💬")

inicializar_estado()
mostrar_mensajes()
manejar_estado()