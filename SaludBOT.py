import streamlit as st
from datetime import datetime, timedelta

# Configuración de la página
st.set_page_config(page_title="SaludBOT - Clínica SanVida", page_icon="🤖")

# Hora actual
hora_actual = datetime.now().strftime("%H:%M")
st.title("🤖 SaludBOT")
st.caption(f"🕒 Son las {hora_actual}. Estoy disponible para ayudarte las 24 horas.")

st.markdown("---")

# Menú principal
st.markdown("### ¿En qué puedo ayudarte hoy?")
opcion = st.radio(
    "Seleccioná una opción:",
    ("🗓️ Turnos para especialistas", "🧪 Turnos para estudios médicos", "🤰 Clases para embarazadas", "⚠️ Hacer un reclamo"),
    index=None,
    key="main_menu"
)

st.markdown("---")

# SACAR UN TURNO
if opcion == "🗓️ Turnos para especialistas":
    st.markdown("#### 📅 Reservá tu turno")

    especialidad = st.selectbox("Seleccioná la especialidad:", ["Clínica médica", "Pediatría", "Ginecología", "Otra"])

    opcion_fecha = st.radio("¿Qué día te gustaría?", ["Mañana", "Pasado mañana", "Otra fecha"])
    
    if opcion_fecha == "Mañana":
        fecha_turno = datetime.now() + timedelta(days=1)
    elif opcion_fecha == "Pasado mañana":
        fecha_turno = datetime.now() + timedelta(days=2)
    else:
        fecha_turno = st.date_input("Seleccioná una fecha:", min_value=datetime.now().date())

    horario = st.selectbox("Turnos disponibles:", ["10:00", "11:30", "13:00"])

    if st.button("Confirmar turno"):
        st.success(f"✅ Turno confirmado para **{especialidad}**, el día **{fecha_turno.strftime('%d/%m/%Y')}** a las **{horario} hs**. Te esperamos en Clínica SanVida.")

# 👉 TURNOS PARA ESTUDIOS MÉDICOS
elif opcion == "🧪 Turnos para estudios médicos":
    st.markdown("#### 🧪 Turnos para estudios médicos")

    estudio = st.selectbox("Seleccioná el tipo de estudio:", [
        "Análisis de sangre",
        "Electrocardiograma (ECG)",
        "Radiografía",
        "Ecografía abdominal",
        "Chequeo completo"
    ])

    opcion_fecha_estudio = st.radio("¿Qué día querés hacerte el estudio?", ["Mañana", "Pasado mañana", "Otra fecha"])
    
    if opcion_fecha_estudio == "Mañana":
        fecha_estudio = datetime.now() + timedelta(days=1)
    elif opcion_fecha_estudio == "Pasado mañana":
        fecha_estudio = datetime.now() + timedelta(days=2)
    else:
        fecha_estudio = st.date_input("Seleccioná una fecha para el estudio:", min_value=datetime.now().date(), key="estudio_fecha")

    horario_estudio = st.selectbox("Horarios disponibles:", ["08:00", "09:30", "11:00", "14:00"])

    if st.button("Confirmar turno de estudio"):
        st.success(f"✅ Turno confirmado para **{estudio}**, el día **{fecha_estudio.strftime('%d/%m/%Y')}** a las **{horario_estudio} hs**. Por favor, llegá 10 minutos antes.")

# CLASES PARA EMBARAZADAS
elif opcion == "🤰 Clases para embarazadas":
    st.markdown("#### 👶 Talleres de preparación al parto")

    modalidad = st.radio("¿Qué modalidad preferís?", ["Presencial", "Virtual"])
    if st.button("Inscribirme"):
        st.success(f"✅ ¡Inscripción confirmada! Taller modalidad **{modalidad}**, jueves 18:00 hs.")

# RECLAMOS
elif opcion == "⚠️ Hacer un reclamo":
    st.markdown("#### 📝 Ingresá tu reclamo")

    tipo_reclamo = st.selectbox("Tipo de reclamo:", ["Factura incorrecta", "Consulta no realizada", "Otro"])
    detalle = st.text_area("Comentanos brevemente qué ocurrió:")

    if st.button("Enviar reclamo"):
        numero_reclamo = f"RCL-{datetime.now().strftime('%H%M')}"
        st.success(f"✅ Reclamo registrado como **'{tipo_reclamo}'**.\nNúmero de caso: **{numero_reclamo}**.\nNos pondremos en contacto pronto.")
