import streamlit as st
from datetime import datetime

def inicializar_estado():
    if "estado" not in st.session_state:
        st.session_state.estado = "menu"  

    if "historial" not in st.session_state:
        st.session_state.historial = []

    if "datos" not in st.session_state:
        st.session_state.datos = {}

    if "bienvenida_mostrada" not in st.session_state:
        st.session_state.bienvenida_mostrada = False

    if "menu_opciones" not in st.session_state:
        st.session_state.menu_opciones = None

    if "consultas_guardadas" not in st.session_state:
        st.session_state.consultas_guardadas = []