import streamlit as st
from datetime import datetime

def inicializar_estado():
    if "estado" not in st.session_state:
        st.session_state.estado = "inicio"
        st.session_state.historial = []
        st.session_state.datos = {}
        st.session_state.bienvenida_mostrada = False
        st.session_state.menu_opciones = None