# 🤖 SaludBOT - Chatbot 24/7 para Clínica SanVida

SaludBOT es un asistente virtual conversacional desarrollado con Streamlit, diseñado para simular la atención digital de una clínica médica. Permite sacar turnos, hacer reclamos y anotarse a clases de RCP, todo con almacenamiento persistente en archivos `.csv`.

---

## 🩺 Funcionalidades

- 🗓️ **Turnos con especialistas**: Clínica médica, Pediatría, Ginecología.
- 📋 **Turnos para estudios médicos**: Laboratorio, ECG, Ecografías y más.
- ❤️ **Inscripción a clases de RCP**: con recordatorio y registro por email/DNI.
- ⚠️ **Gestión de reclamos**: el usuario describe el problema, deja sus datos y obtiene un número de caso.
- 🔍 **Consulta de turnos anteriores**: se puede buscar por DNI o email.
- 💾 **Datos persistentes**: toda la información se guarda en `saludbot/data/` como `.csv`.

---

## 🚀 ¿Cómo ejecutar el bot?

1. Cloná el repo o descargá el ZIP y descomprimilo:

```bash
git clone https://github.com/tu-usuario/SaludBOT.git
cd SaludBOT
```

2. Instalá las dependencias necesarias:

```bash
pip install -r requirements.txt
```

> Si no tenés `requirements.txt`, solo necesitás:

```bash
pip install streamlit pandas
```

3. Ejecutá la app con:

```bash
streamlit run app.py
```

---

## 📁 Estructura del proyecto

```
SaludBOT/
├── app.py
├── chatbot_logic.py
├── data_manager.py
├── utils.py
├── test_robot.py
└── saludbot/
    └── data/
        ├── turnos.csv
        ├── reclamos.csv
        └── rcp.csv
```

---

## 📂 Notas

- Los archivos CSV se crean automáticamente la primera vez que se confirman datos.
- Si desplegás en Streamlit Cloud, asegurate de tener permisos de escritura sobre `saludbot/data/`.
- El bot no requiere bases de datos externas ni backend adicional.

---

## ✨ Créditos

Proyecto educativo realizado como parte de la tecnicatura en IFTS 18.
