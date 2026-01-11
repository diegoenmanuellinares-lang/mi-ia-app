import streamlit as st
import google.generativeai as genai

# Configuración profesional de la página
st.set_page_config(page_title="L'Atelier Français AI", layout="wide")

# Conexión segura con la API
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Error: Configura tu API Key en los Secrets de Streamlit.")
    st.stop()

# Título con estilo académico
st.title("🇫🇷 L'Atelier Français AI: Tutor de Idiomas Avanzado")

# Inicialización de historial de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada de usuario
if prompt := st.chat_input("Escribe tu duda gramatical o de pronunciación..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # EL CAMBIO CLAVE: Nombre del modelo estable
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        
        # Contexto de sistema integrado
        system_context = (
            "Eres un tutor de francés experto. Para cada respuesta: "
            "1. Provee la traducción. 2. Incluye siempre la fonética IPA entre corchetes [ ]. "
            "3. Explica brevemente la regla gramatical involucrada."
        )
        
        with st.chat_message("assistant"):
            response = model.generate_content(f"{system_context}\n\nPregunta: {prompt}")
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
    except Exception as e:
        st.error(f"Error del sistema: {e}")
