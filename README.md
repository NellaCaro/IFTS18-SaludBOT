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

## ✨ Créditos

Proyecto educativo realizado como parte de la tecnicatura en IFTS 18.
