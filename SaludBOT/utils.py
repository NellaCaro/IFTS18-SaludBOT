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

    if st.session_state.estado == "inicio" and not st.session_state.bienvenida_mostrada:
        hora = datetime.now().hour
        if 6 <= hora < 13:
            saludo = "¡Buenos días!"
        elif 13 <= hora < 20:
            saludo = "¡Buenas tardes!"
        else:
            saludo = "¡Buenas noches!"
        mostrar_mensaje("bot", f"{saludo} Soy **SaludBOT**, el asistente virtual de la **Clínica SanVida**. Estoy aquí para ayudarte a gestionar tus turnos y responder tus consultas.")
        st.session_state.bienvenida_mostrada = True