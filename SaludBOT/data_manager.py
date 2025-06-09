import os
import pandas as pd
import streamlit as st
from datetime import datetime

# Ruta de los archivos CSV
DATA_DIR = "data"
TURNOS_CSV = os.path.join(DATA_DIR, "turnos.csv")
RECLAMOS_CSV = os.path.join(DATA_DIR, "reclamos.csv")
RCP_CSV = os.path.join(DATA_DIR, "rcp.csv")

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

def guardar_turno(datos):
    os.makedirs(DATA_DIR, exist_ok=True)
    nuevo = pd.DataFrame([{
        "nombre": datos["nombre"],
        "dni": datos["dni"],
        "email": datos["email"],
        "especialidad": datos["especialidad"],
        "fecha": datos["fecha"],
        "hora": datos["hora"],
        "timestamp": datetime.now().isoformat()
    }])
    if os.path.exists(TURNOS_CSV):
        df = pd.read_csv(TURNOS_CSV)
        df = pd.concat([df, nuevo], ignore_index=True)
    else:
        df = nuevo
    df.to_csv(TURNOS_CSV, index=False)

def guardar_reclamo(reclamo, contacto):
    os.makedirs(DATA_DIR, exist_ok=True)
    nuevo = pd.DataFrame([{
        "tipo": reclamo["tipo"],
        "descripcion": reclamo["descripcion"],
        "nombre": contacto["nombre"],
        "email": contacto["email"],
        "telefono": contacto["telefono"],
        "nro_caso": f"RCL-{datetime.now().strftime('%H%M')}",
        "timestamp": datetime.now().isoformat()
    }])
    if os.path.exists(RECLAMOS_CSV):
        df = pd.read_csv(RECLAMOS_CSV)
        df = pd.concat([df, nuevo], ignore_index=True)
    else:
        df = nuevo
    df.to_csv(RECLAMOS_CSV, index=False)

def guardar_inscripcion_rcp(nombre, dni, email):
    os.makedirs(DATA_DIR, exist_ok=True)
    nuevo = pd.DataFrame([{
        "nombre": nombre,
        "dni": dni,
        "email": email,
        "fecha_clase": "2024-05-30",
        "hora": "17:00",
        "timestamp": datetime.now().isoformat()
    }])
    if os.path.exists(RCP_CSV):
        df = pd.read_csv(RCP_CSV)
        df = pd.concat([df, nuevo], ignore_index=True)
    else:
        df = nuevo
    df.to_csv(RCP_CSV, index=False)

def obtener_turnos_por_dni_o_email(valor):
    if not os.path.exists(TURNOS_CSV):
        return []
    df = pd.read_csv(TURNOS_CSV)
    return df[(df["dni"] == valor) | (df["email"] == valor)].to_dict(orient="records")

def buscar_turnos_por_identificacion(valor):
    """Devuelve turnos guardados por DNI o email"""
    if not os.path.exists(TURNOS_CSV):
        return []

    df = pd.read_csv(TURNOS_CSV)
    resultado = df[(df["dni"].astype(str) == str(valor)) | (df["email"].str.lower() == str(valor).lower())]
    return resultado.to_dict(orient="records")

def buscar_reclamos_por_identificacion(valor):
    if not os.path.exists(RECLAMOS_CSV):
        return []
    df = pd.read_csv(RECLAMOS_CSV)
    return df[(df["dni"].astype(str) == str(valor)) | (df["email"].str.lower() == str(valor).lower())].to_dict(orient="records")

def buscar_clases_rcp_por_identificacion(valor):
    if not os.path.exists(RCP_CSV):
        return []
    df = pd.read_csv(RCP_CSV)
    return df[(df["dni"].astype(str) == str(valor)) | (df["email"].str.lower() == str(valor).lower())].to_dict(orient="records")
