import streamlit as st
from datetime import datetime

def mostrar_mensaje(remitente, contenido):
    if remitente == "bot":
        st.session_state.historial.append(f"**🤖 SaludBOT:** {contenido}")
    else:
        st.session_state.historial.append(f"**🧑 Usuario:** {contenido}")

def mostrar_mensajes():
    for mensaje in st.session_state.historial:
        st.markdown(mensaje)