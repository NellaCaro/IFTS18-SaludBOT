import streamlit as st
from datetime import datetime

# Mostrar hora actual
hora_actual = datetime.now().strftime("%H:%M")
st.markdown(f"### 🕒 Son las {hora_actual}. SaludBot está disponible 24/7.")

# Título del bot
st.title("🤖 SaludBot - Clínica SanVida")

# Menú de opciones con botones
opcion = st.radio(
    "¿En qué puedo ayudarte hoy?",
    ("Sacar un turno", "Consultar estudios médicos", "Clases para embarazadas", "Hacer un reclamo")
)

# Lógica de cada opción
if opcion == "Sacar un turno":
    especialidad = st.selectbox("¿Para qué especialidad necesitás el turno?", ["Clínica médica", "Pediatría", "Ginecología", "Otra"])
    fecha = st.radio("¿Qué día te gustaría?", ["Mañana", "Elegir otra fecha"])
    horario = st.selectbox("Turnos disponibles:", ["10:00", "11:30", "13:00"])
    if st.button("Confirmar turno"):
        st.success(f"✅ Turno confirmado para {especialidad} el día {fecha} a las {horario} hs.")

elif opcion == "Consultar estudios médicos":
    tipo = st.radio("¿Qué tipo de estudios?", ["Chequeo general", "Chequeo completo SanVida"])
    if st.button("Ver detalles"):
        st.info(f"🧪 Información sobre {tipo}: incluye análisis de sangre, ECG, presión y consulta médica.")

elif opcion == "Clases para embarazadas":
    if st.button("Inscribirme en la clase"):
        st.success("✅ ¡Inscripción confirmada para el taller del jueves a las 18:00!")

elif opcion == "Hacer un reclamo":
    tipo_reclamo = st.selectbox("Tipo de reclamo:", ["Factura incorrecta", "Consulta no realizada", "Otro"])
    descripcion = st.text_area("Contanos qué pasó:")
    if st.button("Enviar reclamo"):
        st.success("✅ Reclamo registrado. Número de caso: RCL-001. Te responderemos a la brevedad.")
