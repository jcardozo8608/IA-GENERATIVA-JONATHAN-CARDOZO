"""
Proyecto: Suite de IA Generativa Multiuso
Autor: [Tu Nombre]
Descripción: Aplicación web interactiva construida con Streamlit y la API oficial
de Google GenAI para tareas de redacción, código y conversación.
"""

import os
from google import genai
from google.genai import errors
import streamlit as st

# --- Configuración de la página ---
st.set_page_config(
    page_title="IA Generativa Pro", page_icon="🤖", layout="wide"
)

# --- Título y Descripción ---
st.title("🤖 Suite de IA Generativa con Python & Gemini")
st.caption(
    "Proyecto académico interactivo para procesamiento de lenguaje natural."
)

# --- Inicialización del Cliente y Memoria de API Key ---
st.sidebar.header("⚙️ Configuración")

# Guardar la API Key en el estado de la sesión para que no se borre al cambiar de pestaña
if "api_key" not in st.session_state:
  st.session_state.api_key = ""

api_key_input = st.sidebar.text_input(
    "🔑 API Key de Gemini:",
    value=st.session_state.api_key,
    type="password",
    placeholder="Pega aquí tu clave (AIza...)",
)

if api_key_input:
  st.session_state.api_key = api_key_input

api_key = st.session_state.api_key

if api_key:
  try:
    client = genai.Client(api_key=api_key)
  except Exception as e:
    st.error(f"Error al inicializar el cliente: {e}")
    st.stop()
else:
  st.info(
      "👈 Por favor, ingresa tu API Key de Gemini en la barra lateral para"
      " desbloquear la aplicación."
  )
  st.stop()

# --- Navegación en la Barra Lateral ---
st.sidebar.header("🕹️ Funcionalidades")
opcion = st.sidebar.radio(
    "Selecciona una herramienta:",
    [
        "✍️ Asistente de Redacción",
        "💻 Generador de Código",
        "💬 Chatbot con Memoria",
    ],
)

# ==========================================
# OPCIÓN 1: ASISTENTE DE REDACCIÓN
# ==========================================
if opcion == "✍️ Asistente de Redacción":
  st.subheader("✍️ Generador y Reescribidor de Texto")

  col1, col2 = st.columns(2)
  with col1:
    tema = st.text_area(
        "Ingresa la idea principal o borrador:",
        placeholder="Ej: Escribe un correo pidiendo plazo extra para entregar un trabajo...",
    )
  with col2:
    tono = st.selectbox(
        "Selecciona el tono del texto:",
        ["Profesional y Formal", "Persuasivo", "Académico", "Creativo y Divertido"],
    )
    longitud = st.select_slider(
        "Extensión aproximada:", ["Breve", "Mediana", "Detailed/Extensa"]
    )

  if st.button("🚀 Generar Texto", type="primary"):
    if tema:
      prompt = f"Actúa como un experto en redacción. Escribe sobre: {tema}. Tono: {tono}. Extensión: {longitud}."
      with st.spinner("La IA está redactando tu texto..."):
        try:
          response = client.models.generate_content(
              model="gemini-3.8-flash", contents=prompt
          )
          st.markdown("### 📄 Resultado:")
          st.write(response.text)
        except errors.APIError as e:
          st.error(f"Error en la API: {e}")
    else:
      st.warning("Por favor ingresa un tema o borrador.")

# ==========================================
# OPCIÓN 2: GENERADOR DE CÓDIGO
# ==========================================
elif opcion == "💻 Generador de Código":
  st.subheader("💻 Asistente de Programación")

  lenguaje = st.selectbox(
      "Lenguaje de programación:", ["Python", "JavaScript", "SQL", "C++", "Java"]
  )
  tarea = st.text_area(
      "Describe la función o script que necesitas:",
      placeholder="Ej: Una función que valide si un email tiene un formato correcto.",
  )

  if st.button("⚡ Generar y Explicar Código", type="primary"):
    if tarea:
      prompt = (
          f"Escribe un código en {lenguaje} para: {tarea}. Primero entrega el"
          " código limpio dentro de un bloque de código. Luego explica paso a"
          " paso cómo funciona."
      )
      with st.spinner("Escribiendo código..."):
        try:
          response = client.models.generate_content(
              model="gemini-3.8-flash", contents=prompt
          )
          st.markdown("### 🛠️ Código y Explicación:")
          st.markdown(response.text)
        except errors.APIError as e:
          st.error(f"Error en la API: {e}")
    else:
      st.warning("Escribe qué programa necesitas.")

# ==========================================
# OPCIÓN 3: CHATBOT CON MEMORIA
# ==========================================
elif opcion == "💬 Chatbot con Memoria":
  st.subheader("💬 Chatbot Conversacional")

  # Inicializar el historial de chat en la sesión de Streamlit
  if "chat_session" not in st.session_state:
    st.session_state.chat_session = client.chats.create(
        model="gemini-3.8-flash"
    )
    st.session_state.messages = []

  # Mostrar mensajes anteriores
  for message in st.session_state.messages:
    with st.chat_message(message["role"]):
      st.markdown(message["content"])

  # Entrada del usuario
  if user_input := st.chat_input("Escribe tu mensaje aquí..."):
    # Agregar mensaje del usuario a la pantalla
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
      st.markdown(user_input)

    # Enviar al modelo manteniendo la conversación activa
    with st.chat_message("assistant"):
      with st.spinner("Pensando..."):
        try:
          response = st.session_state.chat_session.send_message(user_input)
          st.markdown(response.text)
          st.session_state.messages.append(
              {"role": "assistant", "content": response.text}
          )
        except errors.APIError as e:
          st.error(f"Error en la API: {e}")