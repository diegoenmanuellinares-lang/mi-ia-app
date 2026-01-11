import streamlit as st
from google import genai

# CONFIGURACIÓN DE SEGURIDAD
API_KEY = "AIzaSyBPC41Jg8SgFlELM9bAS0wY-a8A0ewyX0I"
client = genai.Client(api_key=API_KEY)

# INSTRUCCIONES ACADÉMICAS (Fonética IPA integrada)
instruction = (
    "Eres 'L'Atelier Français AI', un tutor de francés. "
    "REGLA 1: Siempre incluye la transcripción fonética IPA entre corchetes [ ] para cada palabra en francés. "
    "REGLA 2: Usa un tono académico y proporciona citas APA 7ma edición si es necesario."
)

# INTERFAZ DEL TUTOR
st.set_page_config(page_title="L'Atelier Français AI", page_icon="🇫🇷")
st.title("🇫🇷 L'Atelier Français AI")
st.subheader("Tu tutor de francés con fonética IPA")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("¿Qué quieres aprender hoy?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Llamada con la nueva librería para evitar el error 404
            response = client.models.generate_content(
                model="gemini-1.5-flash", 
                contents=prompt,
                config={'system_instruction': instruction}
            )
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error de conexión: {e}")