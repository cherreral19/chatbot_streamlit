import streamlit as st
import requests

# Título de la aplicación
st.title("Chat con API usando Streamlit")

# Variable para almacenar el historial del chat
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []  # Inicializar historial

# 1. Crear un Thread ID para el chat
st.subheader("Crear Sesión")
if st.button("Crear nueva Sesión"):
    try:
        # Realizar la petición al endpoint
        thread = "https://cr-lab-chatbot-legal-624205664083.us-central1.run.app/api/chatbot/create_thread"
        response = requests.post(thread)
        response.raise_for_status()
        respuesta_json = response.json()

        if respuesta_json.get("success"):
            thread_id = respuesta_json["data"].get("thread_id", "")
            st.session_state["thread_id"] = thread_id
            st.success(f"Nueva sesión creada")
        else:
            st.error(f"Error en la respuesta: {respuesta_json.get('message', 'Desconocido')}")
    except Exception as e:
        st.error(f"Error al crear nueva sesión: {e}")

# Verificar si el Thread ID está disponible
if "thread_id" in st.session_state:
    thread_id = st.session_state["thread_id"]

    # 2. Enviar mensajes al chat
    st.subheader("Interacción con el chat")
    user_message = st.text_input("Escribe tu pregunta:")

    if st.button("Enviar mensaje"):
        if user_message.strip() == "":
            st.warning("Por favor, ingresa una pregunta.")
        else:
            try:
                # Realizar la petición al endpoint de chat
                payload = {"thread_id": thread_id, "message": user_message}
                response = requests.post("https://cr-lab-chatbot-legal-624205664083.us-central1.run.app/api/chatbot/run_assistant", json=payload)
                response.raise_for_status()
                respuesta_json = response.json()

                if respuesta_json.get("success"):
                    bot_reply = respuesta_json["data"].get("result", "Sin respuesta")

                    # Actualizar historial de chat
                    st.session_state["chat_history"].append({"user": user_message, "bot": bot_reply})
                else:
                    st.error(f"Error en la respuesta: {respuesta_json.get('message', 'Desconocido')}")
            except Exception as e:
                st.error(f"Error al enviar pregunta: {e}")

    # Mostrar historial de chat
    st.subheader("Historial de chat")
    for chat in reversed(st.session_state["chat_history"]):
        st.write(f"**Tú**: {chat['user']}")
        st.write(f"**Bot**: {chat['bot']}")
        st.write("---")
else:
    st.info("Primero debes crear una sesión")
