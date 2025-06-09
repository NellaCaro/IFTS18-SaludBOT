import streamlit as st
from datetime import datetime
from utils import mostrar_mensaje
import re

def manejar_estado():
    estado = st.session_state.estado

    if estado == "inicio":
        if st.button("💬 Comenzar"):
            st.session_state.estado = "menu"
            st.rerun()

    elif estado == "menu":
        opciones = [
            "🗓️ Turno con especialista",
            "📋 Turno para estudios médicos",
            "❤️ Clases de RCP",
            "⚠️ Hacer un reclamo",
            "📚 Preguntas frecuentes",
            "🔍 Ver mis turnos"
        ]
        opcion = st.radio("Seleccioná una opción:", opciones, key="menu_opciones")
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
            elif "frecuentes" in opcion:
                st.session_state.estado = "faq"
            elif "Ver mis turnos" in opcion:
                st.session_state.estado = "ver_turnos"
            st.rerun()

    elif estado == "turno_especialidad":
        if "especialidad_confirmada" not in st.session_state:
            especialidad = st.radio("¿Para qué especialidad querés el turno?", ["Clínica médica", "Pediatría", "Ginecología"], key="esp")
            if st.button("📌 Confirmar especialidad"):
                mostrar_mensaje("user", especialidad)
                st.session_state.datos["especialidad"] = especialidad
                st.session_state.especialidad_confirmada = True
                st.rerun()
        else:
            st.session_state.estado = "turno_fecha"
            st.rerun()

    elif estado == "estudios_tipo":
        if "especialidad_confirmada" not in st.session_state:
            especialidad = st.radio("¿Qué estudio necesitás?", ["Laboratorio general", "ECG", "Radiografía", "Ecografía", "Chequeo completo"], key="estudio")
            if st.button("📌 Confirmar estudio"):
                mostrar_mensaje("user", especialidad)
                st.session_state.datos["especialidad"] = especialidad
                st.session_state.especialidad_confirmada = True
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
            dni = st.text_input("🪪 DNI", key="dni")
            email = st.text_input("📧 Correo electrónico", key="email")

            if st.button("📋 Confirmar turno"):
                if not re.match(r"^\d{7,8}$", dni):
                    st.error("DNI inválido. Ingresá solo números, entre 7 y 8 dígitos.")
                elif not re.match(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
                    st.error("Email inválido.")
                else:
                    st.session_state.datos["nombre"] = nombre
                    st.session_state.datos["dni"] = dni
                    st.session_state.datos["email"] = email
                    mostrar_mensaje("user", f"Nombre: {nombre}, DNI: {dni}, Email: {email}")
                    d = st.session_state.datos
                    mostrar_mensaje("bot", f"✅ Turno confirmado para **{d['nombre']}**, con la especialidad **{d['especialidad']}** el **{d['fecha']}** a las **{d['horario']} hs**. Se enviará un recordatorio a tu correo electrónico: **{d['email']}**. Te esperamos en Clínica SanVida.")
                    st.session_state.paciente_confirmado = True
                    st.session_state.estado = "reiniciar"
                    st.rerun()

    elif estado == "rcp_info":
        if "rcp_info_mostrada" not in st.session_state:
            mostrar_mensaje("bot", "🫀 La próxima clase de **RCP** será el **jueves 30 de mayo** en el **SUM de Clínica SanVida** a las **17:00 hs**. Aprenderás a asistir a una persona con paro cardiorrespiratorio, aplicar compresiones efectivas y utilizar un DEA.")
            st.session_state.rcp_info_mostrada = True
            st.rerun()

        elif "rcp_datos_pendientes" not in st.session_state:
            if st.button("📝 Inscribirme a la clase"):
                mostrar_mensaje("user", "Quiero inscribirme")
                st.session_state.rcp_datos_pendientes = True
                st.rerun()

        elif "rcp_confirmado" not in st.session_state:
            nombre = st.text_input("🧑 Nombre y apellido", key="rcp_nombre")
            dni = st.text_input("🪪 DNI", key="rcp_dni")
            email = st.text_input("📧 Correo electrónico", key="rcp_email")

            if st.button("📋 Confirmar inscripción"):
                if not re.match(r"^\d{7,8}$", dni):
                    st.error("DNI inválido.")
                elif not re.match(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
                    st.error("Email inválido.")
                else:
                    mostrar_mensaje("user", f"Nombre: {nombre}, DNI: {dni}, Email: {email}")
                    mostrar_mensaje("bot", f"✅ ¡Inscripción confirmada! Te esperamos el **jueves 30 de mayo** en el SUM de Clínica SanVida. Podés acercarte 10 minutos antes. Se enviará un recordatorio a **{email}**.")
                    st.session_state.rcp_confirmado = True
                    st.session_state.estado = "reiniciar"
                    st.rerun()

    elif estado == "reclamo_tipo":
        if "reclamo_mensaje" not in st.session_state:
            tipo = st.radio("Seleccioná el tipo de reclamo:", ["Factura incorrecta", "Consulta no realizada", "Otro"], key="tipo_reclamo")
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
                if not re.match(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
                    st.error("Email inválido.")
                elif not re.match(r"^\d{6,15}$", telefono):
                    st.error("Teléfono inválido. Ingresá solo números.")
                else:
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
            mostrar_mensaje("bot", f"✅ Reclamo registrado como **{reclamo['tipo']}**.\n\n📝 Detalle: {reclamo['descripcion']}\n\n👤 Contacto: {datos['nombre']} - {datos['email']} - {datos['telefono']}\n\n🔢 Número de caso: **{nro}**")
            st.session_state.estado = "reiniciar"
            st.rerun()

    elif estado == "faq":
        mostrar_mensaje("bot", "ℹ️ Preguntas frecuentes:")
        st.markdown("- ¿Cómo saco un turno? → Ingresá a 'Turno con especialista' o 'Estudios médicos'.")
        st.markdown("- ¿Dónde se dictan las clases de RCP? → En el SUM de Clínica SanVida.")
        st.markdown("- ¿Puedo cancelar un turno? → Por ahora no, pero se puede ignorar sin penalidad.")
        if st.button("🔁 Volver al menú"):
            st.session_state.estado = "menu"
            st.rerun()

    elif estado == "ver_turnos":
        doc = st.text_input("Ingresá tu DNI o Email para buscar tus registros:", key="buscar_turnos")
        if st.button("🔎 Buscar"):
            encontrados = []
            if "email" in st.session_state.datos and doc in st.session_state.datos.values():
                encontrados.append(f"📅 Turno: {st.session_state.datos.get('especialidad', 'Especialidad no registrada')} el {st.session_state.datos.get('fecha')} a las {st.session_state.datos.get('horario')} hs.")
            if "rcp_confirmado" in st.session_state and st.session_state.rcp_confirmado:
                encontrados.append("❤️ Clase de RCP: jueves 30 de mayo a las 17:00 hs en SUM SanVida.")
            if "reclamo_contacto" in st.session_state and doc in st.session_state.reclamo_contacto.values():
                encontrados.append(f"🧾 Reclamo registrado: {st.session_state.reclamo_mensaje.get('tipo')} - Caso #{datetime.now().strftime('%H%M')}")
            if encontrados:
                for item in encontrados:
                    mostrar_mensaje("bot", item)
            else:
                mostrar_mensaje("bot", "No se encontraron registros con ese dato.")
            st.session_state.estado = "reiniciar"
            st.rerun()

    elif estado == "reiniciar":
        if st.button("🔁 Hacer otra consulta"):
            st.session_state.estado = "inicio"
            st.session_state.datos = {}
            for key in list(st.session_state.keys()):
                if key not in ("estado", "datos", "historial"):
                    del st.session_state[key]
            st.rerun()
