import streamlit as st
from datetime import datetime
from utils import mostrar_mensaje
from data_manager import guardar_turno, buscar_turnos_por_identificacion

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


    elif estado == "turno_especialidad":
        especialidad = st.radio("¿Para qué especialidad querés el turno?", ["Clínica médica", "Pediatría", "Ginecología"])
        if st.button("📌 Confirmar especialidad"):
            mostrar_mensaje("user", especialidad)
            st.session_state.datos = {"especialidad": especialidad}
            st.session_state.estado = "turno_fecha"
            st.rerun()

    elif estado == "estudios_tipo":
        estudio = st.radio("¿Qué estudio necesitás?", ["Laboratorio general", "ECG", "Radiografía", "Ecografía", "Chequeo completo"])
        if st.button("📈 Confirmar estudio"):
            mostrar_mensaje("user", estudio)
            st.session_state.datos = {"especialidad": estudio}
            st.session_state.estado = "turno_fecha"
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
            from data_manager import guardar_reclamo

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

    elif estado == "turno_fecha":
        fecha = st.date_input("📅 Seleccioná el día del turno:", min_value=datetime.now().date())
        if st.button("📌 Confirmar fecha"):
            mostrar_mensaje("user", fecha.strftime('%d/%m/%Y'))
            st.session_state.datos["fecha"] = fecha.strftime('%d/%m/%Y')
            st.session_state.estado = "turno_horario"
            st.rerun()

    elif estado == "turno_horario":
        hora = st.radio("🕒 Seleccioná un horario:", ["10:00", "11:30", "13:00"])
        if st.button("📌 Confirmar horario"):
            mostrar_mensaje("user", hora)
            st.session_state.datos["hora"] = hora
            st.session_state.estado = "turno_datos_paciente"
            st.rerun()

    elif estado == "turno_datos_paciente":
        nombre = st.text_input("🧑 Nombre y apellido")
        dni = st.text_input("🆔 DNI (solo números)")
        email = st.text_input("📧 Email")

        errores = []
        if dni and not dni.isdigit():
            errores.append("El DNI debe contener solo números.")
        if email and "@" not in email:
            errores.append("El email no parece válido.")

        for e in errores:
            st.error(e)

        if st.button("📋 Confirmar turno"):
            if nombre and dni.isdigit() and "@" in email:
                st.session_state.datos["nombre"] = nombre
                st.session_state.datos["dni"] = dni
                st.session_state.datos["email"] = email

                mostrar_mensaje("user", f"{nombre}, {dni}, {email}")
                guardar_turno(st.session_state.datos)

                d = st.session_state.datos
                mostrar_mensaje("bot", f"✅ Turno confirmado para **{d['nombre']}**, con la especialidad **{d['especialidad']}** el **{d['fecha']}** a las **{d['hora']} hs**. Se enviará un recordatorio a: **{d['email']}**")
                st.session_state.estado = "reiniciar"
                st.rerun()

    elif estado == "consulta_turnos":
        st.markdown("### 🔍 Consultá tus registros agendados")
        dato = st.text_input("Ingresá tu DNI o correo electrónico:")

        if st.button("📂 Buscar mis registros"):
            if dato:
                from data_manager import buscar_turnos_por_identificacion
                from data_manager import buscar_reclamos_por_identificacion
                from data_manager import buscar_clases_rcp_por_identificacion

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


    elif estado == "reiniciar":
        st.markdown("¿Querés hacer otra consulta?")
        if st.button("🔁 Volver al menú"):
            st.session_state.estado = "menu"
            st.session_state.datos = {}
            st.rerun()

    elif estado == "salida":
        st.markdown("<h4>👋 ¡Gracias por usar SaludBOT!</h4>", unsafe_allow_html=True)
        st.stop()
