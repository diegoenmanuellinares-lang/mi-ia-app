import streamlit as st
import google.generativeai as genai

# Configuración avanzada de la interfaz
st.set_page_config(page_title="L'Atelier Français AI", page_icon="🇫🇷", layout="wide")

# Conexión con la API Key desde tus Secrets
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Error: Configura tu API Key en los Secrets de Streamlit.")
    st.stop()

# Título Académico
st.title("🇫🇷 L'Atelier Français AI")
st.subheader("Tu tutor académico de francés con fonética IPA")

# Lógica del Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("¿En qué puedo ayudarte con tu francés hoy?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Nombre del modelo estable para evitar el error 404
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        
        # Instrucción del sistema para rigor académico
        system_instruction = (
            "Eres un tutor de francés para estudiantes universitarios. "
            "Reglas: 1. Siempre provee la transcripción IPA [ ]. "
            "2. Usa un tono profesional. 3. Cita reglas gramaticales."
        )
        
        with st.chat_message("assistant"):
            response = model.generate_content(f"{system_instruction}\n\nPregunta: {prompt}")
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
    except Exception as e:
        st.error(f"Hubo un problema técnico: {e}")
