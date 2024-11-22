import requests
import streamlit as st

st.title("Chatbol Legal - Dev")

# Configurar variables iniciales de la sesión
if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = None

if "messages" not in st.session_state:
    st.session_state.messages = []

# Crear nueva sesión (Thread ID)
st.subheader("Crear Sesión")
if st.button("Crear nueva Sesión"):
    try:
        # Llamada al endpoint para crear una nueva sesión
        create_thread_url = "https://cr-lab-chatbot-legal-624205664083.us-central1.run.app/api/chatbot/create_thread"
        response = requests.post(create_thread_url)
        response.raise_for_status()
        respuesta_json = response.json()

        if respuesta_json.get("success"):
            st.session_state["thread_id"] = respuesta_json["data"].get("thread_id")
            st.success(f"Nueva sesión creada con ID: {st.session_state['thread_id']}")
            st.session_state.messages = []  # Reiniciar historial de chat
        else:
            st.error(f"Error en la respuesta: {respuesta_json.get('message', 'Desconocido')}")
    except Exception as e:
        st.error(f"Error al crear nueva sesión: {e}")

# Verificar si el Thread ID está disponible
if st.session_state["thread_id"]:
    # Mostrar el historial de chat
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Interacción con el usuario
    if prompt := st.chat_input("Escribe tu pregunta:"):
        # Agregar el mensaje del usuario al historial
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        try:
            # Llamada al endpoint del chatbot para obtener la respuesta
            chat_url = "https://cr-lab-chatbot-legal-624205664083.us-central1.run.app/api/chatbot/run_assistant"
            payload = {"thread_id": st.session_state["thread_id"], "message": prompt}
            response = requests.post(chat_url, json=payload)
            response.raise_for_status()
            respuesta_json = response.json()

            if respuesta_json.get("success"):
                bot_reply = respuesta_json["data"].get("result", "Sin respuesta")
                st.session_state.messages.append({"role": "assistant", "content": bot_reply})

                # Mostrar respuesta del bot
                with st.chat_message("assistant"):
                    st.markdown(bot_reply)
            else:
                st.error(f"Error en la respuesta: {respuesta_json.get('message', 'Desconocido')}")
        except Exception as e:
            st.error(f"Error al procesar el mensaje: {e}")
else:
    st.info("Primero debes crear una sesión.")
