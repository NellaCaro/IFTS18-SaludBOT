import streamlit as st
from datetime import datetime, timedelta
from utils import mostrar_mensaje
from data_manager import guardar_turno

def manejar_estado():
    estado = st.session_state.estado

    if estado == "inicio":
        pass  # el botón ya está en app.py

    elif estado == "menu":
        st.markdown("""
            <h3 style='text-align: center;'>🤖 SaludBOT | ¿Cómo puedo ayudarte hoy?</h3>
            <p style='text-align: center;'>🍺 <em>Clínica SanVida - Atención 24/7</em></p>
        """, unsafe_allow_html=True)

        opciones = [
            "🗓️ Turno con especialista",
            "📋 Turno para estudios médicos",
            "❤️ Clases de RCP",
            "⚠️ Hacer un reclamo"
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
            st.rerun()

    elif estado == "turno_especialidad":
        if "especialidad_confirmada" not in st.session_state:
            especialidad = st.radio("¿Para qué especialidad querés el turno?", ["Clínica médica", "Pediatría", "Ginecología"])
            if st.button("📌 Confirmar especialidad"):
                mostrar_mensaje("user", especialidad)
                st.session_state.datos["especialidad"] = especialidad
                st.session_state.especialidad_confirmada = True
                st.session_state.estado = "turno_fecha"
                st.rerun()
        else:
            st.session_state.estado = "turno_fecha"
            st.rerun()

    elif estado == "estudios_tipo":
        if "especialidad_confirmada" not in st.session_state:
            estudio = st.radio("¿Qué estudio necesitás?", ["Laboratorio general", "ECG", "Radiografía", "Ecografía", "Chequeo completo"])
            if st.button("📈 Confirmar estudio"):
                mostrar_mensaje("user", estudio)
                st.session_state.datos["especialidad"] = estudio
                st.session_state.especialidad_confirmada = True
                st.session_state.estado = "turno_fecha"
                st.rerun()
        else:
            st.session_state.estado = "turno_fecha"
            st.rerun()

    elif estado == "turno_fecha":
        if "fecha_confirmada" not in st.session_state:
            fecha = st.date_input("Seleccioná el día del turno:", min_value=datetime.now().date(), key="fecha_calendar")
            if st.button("📌 Confirmar fecha"):
                mostrar_mensaje("user", f"{fecha.strftime('%d/%m/%Y')}")
                st.session_state.datos["fecha"] = fecha.strftime("%d/%m/%Y")
                st.session_state.fecha_confirmada = True
                st.rerun()
        else:
            st.session_state.estado = "turno_horario"
            st.rerun()

    elif estado == "turno_horario":
        if "horario_confirmado" not in st.session_state:
            horario = st.radio("Seleccioná un horario:", ["10:00", "11:30", "13:00"], key="hora")
            if st.button("📌 Confirmar horario"):
                mostrar_mensaje("user", horario)
                st.session_state.datos["horario"] = horario
                st.session_state.horario_confirmado = True
                st.rerun()
        else:
            st.session_state.estado = "turno_datos_paciente"
            st.rerun()

    elif estado == "turno_datos_paciente":
        if "paciente_confirmado" not in st.session_state:
            nombre = st.text_input("🧑 Nombre y apellido", key="nombre")
            dni_input = st.text_input("🆔 DNI (sin puntos ni letras)", key="dni")
            email = st.text_input("📧 Correo electrónico", key="email")

            if dni_input.isdigit():
                dni_valido = True
            else:
                dni_valido = False
                st.error("El DNI debe contener solo números, sin puntos ni letras.")

            if st.button("📋 Confirmar turno"):
                if nombre and dni_valido and email:
                    st.session_state.datos["nombre"] = nombre
                    st.session_state.datos["dni"] = dni_input
                    st.session_state.datos["email"] = email
                    mostrar_mensaje("user", f"Nombre: {nombre}, DNI: {dni_input}, Email: {email}")
                    d = st.session_state.datos
                    mostrar_mensaje("bot", f"✅ Turno confirmado para **{d['nombre']}**, con la especialidad **{d['especialidad']}** el **{d['fecha']}** a las **{d['horario']} hs**. Se enviará un recordatorio a tu correo electrónico: **{d['email']}**. Te esperamos en Clínica SanVida.")

                    guardar_turno(st.session_state.datos)
        st.session_state.consultas_guardadas.append(st.session_state.datos.copy())
                    st.session_state.paciente_confirmado = True
                    st.session_state.estado = "reiniciar"
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
            mostrar_mensaje("bot", f"Su reclamo ha sido registrado como **{reclamo['tipo']}**.\nUn representante se pondrá en contacto a la brevedad.\n\n📝 Detalle: {reclamo['descripcion']}\n\n👤 Contacto: {datos['nombre']} - {datos['email']} - {datos['telefono']}\n\n🔹 Número de caso: **{nro}**")
            st.session_state.estado = "reiniciar"
            st.rerun()

    elif estado == "turno_especialidad":
        if "especialidad_confirmada" not in st.session_state:
            especialidad = st.radio("¿Para qué especialidad querés el turno?", ["Clínica médica", "Pediatría", "Ginecología"], key="esp")
            if st.button("📌 Confirmar especialidad"):
                mostrar_mensaje("user", especialidad)
                st.session_state.datos["especialidad"] = especialidad
                st.session_state.especialidad_confirmada = True
                st.session_state.estado = "turno_fecha"
                st.rerun()
        else:
            st.session_state.estado = "turno_fecha"
            st.rerun()

    elif estado == "estudios_tipo":
        if "especialidad_confirmada" not in st.session_state:
            estudio = st.radio("¿Qué estudio necesitás?", ["Laboratorio general", "ECG", "Radiografía", "Ecografía", "Chequeo completo"], key="estudio")
            if st.button("📌 Confirmar estudio"):
                mostrar_mensaje("user", estudio)
                st.session_state.datos["especialidad"] = estudio
                st.session_state.especialidad_confirmada = True
                st.session_state.estado = "turno_fecha"
                st.rerun()
        else:
            st.session_state.estado = "turno_fecha"
            st.rerun()

    elif estado == "turno_fecha":
        if "fecha_confirmada" not in st.session_state:
            fecha = st.date_input("Seleccioná el día del turno:", min_value=datetime.now().date(), key="fecha_calendar")
            if st.button("📌 Confirmar fecha"):
                mostrar_mensaje("user", f"{fecha.strftime('%d/%m/%Y')}")
                st.session_state.datos["fecha"] = fecha.strftime("%d/%m/%Y")
                st.session_state.fecha_confirmada = True
                st.rerun()
        else:
            st.session_state.estado = "turno_horario"
            st.rerun()

    elif estado == "turno_horario":
        if "horario_confirmado" not in st.session_state:
            horario = st.radio("Seleccioná un horario:", ["10:00", "11:30", "13:00"], key="hora")
            if st.button("📌 Confirmar horario"):
                mostrar_mensaje("user", horario)
                st.session_state.datos["horario"] = horario
                st.session_state.horario_confirmado = True
                st.rerun()
        else:
            st.session_state.estado = "turno_datos_paciente"
            st.rerun()

    elif estado == "turno_datos_paciente":
        if "paciente_confirmado" not in st.session_state:
            nombre = st.text_input("🧑 Nombre y apellido", key="nombre")
            dni_input = st.text_input("🆔 DNI (sin puntos ni letras)", key="dni")
            email = st.text_input("📧 Correo electrónico", key="email")

            if dni_input.isdigit():
                dni_valido = True
            else:
                dni_valido = False
                st.error("El DNI debe contener solo números, sin puntos ni letras.")

            if st.button("📋 Confirmar turno"):
                if nombre and dni_valido and email:
                    st.session_state.datos["nombre"] = nombre
                    st.session_state.datos["dni"] = dni_input
                    st.session_state.datos["email"] = email
                    mostrar_mensaje("user", f"Nombre: {nombre}, DNI: {dni_input}, Email: {email}")
                    d = st.session_state.datos
                    mostrar_mensaje("bot", f"✅ Turno confirmado para **{d['nombre']}**, con la especialidad **{d['especialidad']}** el **{d['fecha']}** a las **{d['horario']} hs**. Se enviará un recordatorio a tu correo electrónico: **{d['email']}**. Te esperamos en Clínica SanVida.")

                    guardar_turno(st.session_state.datos)
        st.session_state.consultas_guardadas.append(st.session_state.datos.copy())
                    st.session_state.paciente_confirmado = True
                    st.session_state.estado = "reiniciar"
                    st.rerun()

    elif estado == "rcp_info":
        if "rcp_info_mostrada" not in st.session_state:
            mostrar_mensaje("bot", "❤️ La próxima clase de **RCP** será el **jueves 30 de mayo** en el **SUM de Clínica SanVida** a las **17:00 hs**. Aprenderás a asistir a una persona con paro cardiorrespiratorio, aplicar compresiones efectivas y utilizar un DEA.")
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
                    mostrar_mensaje("user", f"Nombre: {nombre}, DNI: {dni}, Email: {email}")
                    mostrar_mensaje("bot", f"✅ ¡Inscripción confirmada! Te esperamos el **jueves 30 de mayo** en el SUM de Clínica SanVida. Se enviará un recordatorio a **{email}**.")
                    st.session_state.rcp_confirmado = True
                    st.session_state.estado = "reiniciar"
                    st.rerun()

    elif estado == "reiniciar":
        if st.button("🔁 Hacer otra consulta", key="boton_reiniciar"):
            st.session_state.estado = "menu"
            st.session_state.datos = {}
            st.session_state.menu_opciones = None
            st.session_state.historial = []

            for key in [
                "especialidad_confirmada",
                "fecha_confirmada",
                "horario_confirmado",
                "paciente_confirmado",
                "rcp_info_mostrada",
                "rcp_datos_pendientes",
                "rcp_confirmado",
                "reclamo_mensaje",
                "reclamo_contacto"
            ]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

        if st.button("📂 Ver todos mis turnos", key="ver_turnos_btn"):
            st.session_state.estado = "ver_turnos"
            st.session_state.historial = []
            st.rerun()

        if st.button("🚪 Salir del asistente"):
            st.session_state.estado = "salida"
            st.rerun()

    elif estado == "ver_turnos":
        st.markdown("### 🗓️ Turnos confirmados en esta sesión:")
        if st.session_state.consultas_guardadas:
            for i, cita in enumerate(st.session_state.consultas_guardadas, 1):
                st.markdown(
                    f"**Turno {i}:** {cita['especialidad']} el **{cita['fecha']}** a las **{cita['horario']} hs** para **{cita['nombre']}**"
                )
        else:
            st.info("Aún no se ha confirmado ningún turno.")

        st.markdown("---")
        if st.button("🔁 Hacer otra consulta", key="volver_menu_turnos"):
            st.session_state.estado = "menu"
            st.session_state.historial = []
            st.rerun()

        if st.button("🚪 Salir del asistente", key="salir_turnos"):
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