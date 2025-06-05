import streamlit as st
from datetime import datetime, timedelta
from utils import mostrar_mensaje, mostrar_mensajes
from chatbot_logic import manejar_estado
from data_manager import inicializar_estado

# Configuración de la página
st.set_page_config(page_title="SaludBOT - Clínica SanVida", page_icon="💬", layout="centered")

# Crear estado inicial "comenzar" si no existe
if "comenzar" not in st.session_state:
    st.session_state.comenzar = False

# Mostrar bienvenida si todavía no se ha hecho clic
if not st.session_state.comenzar:
    # Robot emoji centrado y más grande
    st.markdown(
        """<div style='text-align: center;'>
            <img src='https://img.icons8.com/emoji/96/robot-emoji.png' width='70'/>
        </div>""",
        unsafe_allow_html=True
    )

    # Título y subtítulo
    st.markdown("<h1 style='text-align: center; color: #4A90E2;'>💬 Bienvenido a SaludBOT</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center;'>Tu asistente virtual de la Clínica SanVida</h4>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    # Texto de bienvenida
    st.markdown("Estoy disponible **24/7** para ayudarte a gestionar turnos médicos, estudios, clases de RCP y reclamos.")
    st.markdown("Por favor, hacé clic en el botón para comenzar 😊")

    # Botón de comenzar (¡con buena indentación!)
    if st.button("👉 Comenzar"):
        st.session_state.comenzar = True
        st.rerun()

# Si ya hizo clic, mostrar el flujo normal del bot
if st.session_state.comenzar:

    # Si el usuario ya eligió salir, mostrar solo la despedida
    if "estado" in st.session_state and st.session_state.estado == "salida":
        st.markdown(
            """<div style='text-align: center;'>
                <img src='https://img.icons8.com/emoji/96/robot-emoji.png' width='70'/>
                <h2 style='color:#4A90E2;'>👋 ¡Gracias por usar SaludBOT!</h2>
                <p>Tu asistente virtual de la <strong>Clínica SanVida</strong>.</p>
                <p>Esperamos verte pronto. Podés cerrar esta ventana cuando quieras 😊</p>
            </div>""",
            unsafe_allow_html=True
        )
        st.stop()

    # Si no eligió salir, seguir flujo normal
    inicializar_estado()
    mostrar_mensajes()
    manejar_estado()