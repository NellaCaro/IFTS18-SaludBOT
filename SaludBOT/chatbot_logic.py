import streamlit as st
from datetime import datetime
from utils import mostrar_mensaje
from data_manager import guardar_turno, guardar_reclamo, buscar_turnos_por_identificacion, buscar_reclamos_por_identificacion, buscar_clases_rcp_por_identificacion

def manejar_estado():
    estado = st.session_state.estado

    if estado == "inicio":
        hora = datetime.now().hour
        if 6 <= hora < 13:
            saludo = "¡Buenos días!"
        elif 13 <= hora < 20:
            saludo = "¡Buenas tardes!"
        else:
            saludo = "¡Buenas noches!"

        if not st.session_state.get("bienvenida_mostrada", False):
            mostrar_mensaje("bot", f"{saludo} Soy SaludBOT y estoy disponible para ayudarte.")
            st.session_state.bienvenida_mostrada = True

    elif estado == "menu":
        st.markdown("""
            <h3 style='text-align: center;'>🤖 SaludBOT | ¿Cómo puedo ayudarte hoy?</h3>
            <p style='text-align: center;'><em>Clínica SanVida - Atención 24/7</em></p>
        """, unsafe_allow_html=True)

        opciones = [
            "🗓️ Turno con especialista",
            "📋 Turno para estudios médicos",
            "❤️ Clases de RCP",
            "⚠️ Hacer un reclamo",
            "📂 Ver mis registros"
        ]
        opcion = st.radio("Seleccioná una opción:", opciones)

        if st.button("✅ Confirmar selección"):
            mostrar_mensaje("user", opcion)
            if "especialista" in opcion:
                st.session_state.estado = "turno_especialidad"
            elif "estudios" in opcion:
                st.session_state.estado = "estudios_tipo"
            elif "RCP" in opcion:
                st.session_state.estado = "rcp_info"
            elif "reclamo" in opcion:
                st.session_state.estado = "reclamo_tipo"
            elif "Ver mis registros" in opcion:
                st.session_state.estado = "consulta_turnos"
            st.rerun()

    elif estado == "reclamo_tipo":
        if "reclamo_mensaje" not in st.session_state:
            tipo = st.radio("Seleccioná el tipo de reclamo:", [
                "Factura incorrecta",
                "Consulta no realizada",
                "Otro"
            ], key="tipo_reclamo")
            descripcion = st.text_area("Describí brevemente tu reclamo:", key="detalle_reclamo")

            if st.button("📨 Enviar reclamo"):
                if descripcion:
                    mostrar_mensaje("user", f"{tipo} - {descripcion}")
                    st.session_state.reclamo_mensaje = {
                        "tipo": tipo,
                        "descripcion": descripcion
                    }
                    st.rerun()

        elif "reclamo_contacto" not in st.session_state:
            nombre = st.text_input("🧑 Tu nombre", key="reclamo_nombre")
            email = st.text_input("📧 Tu correo electrónico", key="reclamo_email")
            telefono = st.text_input("📱 Tu número de contacto", key="reclamo_tel")

            if st.button("📋 Confirmar datos de contacto"):
                if nombre and email and telefono:
                    st.session_state.reclamo_contacto = {
                        "nombre": nombre,
                        "email": email,
                        "telefono": telefono
                    }
                    st.rerun()

        else:
            datos = st.session_state.reclamo_contacto
            reclamo = st.session_state.reclamo_mensaje
            nro = f"RCL-{datetime.now().strftime('%H%M')}"
            guardar_reclamo(reclamo, datos)

            mostrar_mensaje("bot", f"""✅ Reclamo registrado como **{reclamo['tipo']}**.
            📝 Detalle: {reclamo['descripcion']}
            📌 Contacto: {datos['nombre']} - {datos['email']} - {datos['telefono']}
            🆔 Número de caso: **{nro}**
            Un representante se comunicará con vos a la brevedad.
            """)
            st.session_state.estado = "reiniciar"
            st.rerun()
    elif estado == "estudios_tipo":
        estudio = st.radio("¿Qué estudio necesitás?", [
            "Laboratorio general", "ECG", "Radiografía", "Ecografía", "Chequeo completo"
        ])
        if st.button("📈 Confirmar estudio"):
            mostrar_mensaje("user", estudio)
            st.session_state.datos = {"especialidad": estudio}
            st.session_state.estado = "turno_fecha"
            st.rerun()

    elif estado == "consulta_turnos":
        st.markdown("### 🔍 Consultá tus registros agendados")
        dato = st.text_input("Ingresá tu DNI o correo electrónico:")

        if st.button("📂 Buscar mis registros"):
            turnos = buscar_turnos_por_identificacion(dato)
            reclamos = buscar_reclamos_por_identificacion(dato)
            clases = buscar_clases_rcp_por_identificacion(dato)

            if turnos:
                st.markdown("#### 📅 Turnos:")
                for i, t in enumerate(turnos, 1):
                    st.markdown(f"- **{t['especialidad']}** el {t['fecha']} a las {t['hora']} hs – {t['nombre']}")

            if reclamos:
                st.markdown("#### 📝 Reclamos:")
                for r in reclamos:
                    st.markdown(f"- {r['tipo']} – {r['descripcion']} (Caso: {r['nro_caso']})")

            if clases:
                st.markdown("#### ❤️ Clases de RCP:")
                for c in clases:
                    st.markdown(f"- {c['fecha_clase']} a las {c['hora']} hs – {c['nombre']}")

            if not turnos and not reclamos and not clases:
                st.info("🤖 No se encontraron registros con ese dato.")

        if st.button("🔁 Volver al menú principal"):
            st.session_state.estado = "menu"
            st.rerun()
    
    elif estado == "rcp_info":
        if "rcp_info_mostrada" not in st.session_state:
            mostrar_mensaje("bot", "❤️ La próxima clase de **RCP** será el **jueves 12 de junio** en el **SUM de Clínica SanVida** a las **17:00 hs**. Aprenderás a asistir a una persona con paro cardiorrespiratorio, aplicar compresiones efectivas y utilizar un DEA.")
            st.session_state.rcp_info_mostrada = True
            st.rerun()

        elif "rcp_datos_pendientes" not in st.session_state:
            if st.button("📝 Inscribirme a la clase"):
                mostrar_mensaje("user", "Quiero inscribirme")
                st.session_state.rcp_datos_pendientes = True
                st.rerun()

        elif "rcp_confirmado" not in st.session_state:
            nombre = st.text_input("🧑 Nombre y apellido", key="rcp_nombre")
            dni = st.text_input("🆔 DNI (sin puntos ni letras)", key="rcp_dni")
            email = st.text_input("📧 Correo electrónico", key="rcp_email")

            if dni and not dni.isdigit():
                st.error("El DNI debe contener solo números.")

            if st.button("📋 Confirmar inscripción", key="confirmar_rcp"):
                if nombre and dni.isdigit() and email:
                    from data_manager import guardar_inscripcion_rcp
                    guardar_inscripcion_rcp(nombre, dni, email)

                    mostrar_mensaje("user", f"Nombre: {nombre}, DNI: {dni}, Email: {email}")
                    mostrar_mensaje("bot", f"✅ ¡Inscripción confirmada! Te esperamos el **jueves 30 de mayo** en el SUM de Clínica SanVida. Se enviará un recordatorio a **{email}**.")
                    st.session_state.rcp_confirmado = True
                    st.session_state.estado = "reiniciar"
                    st.rerun()


    elif estado == "reiniciar":
        st.markdown("¿Querés hacer otra consulta?")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔁 Volver al menú"):
                st.session_state.estado = "menu"
                st.session_state.datos = {}
                st.rerun()
        with col2:
            if st.button("🚪 Salir del asistente"):
                st.session_state.estado = "salida"
                st.rerun()

    elif estado == "salida":
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
