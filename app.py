import streamlit as st
import google.generativeai as genai

# CONFIGURACIÓN DE SEGURIDAD
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Falta la configuración de la API Key en los Secretos de Streamlit.")

# INSTRUCCIONES PARA EL TUTOR (Enfoque académico y fonético)
instruction = (
    "Eres 'L'Atelier Français AI', un tutor de francés para universitarios. "
    "REGLA 1: Siempre incluye la transcripción fonética IPA entre corchetes [ ] para cada palabra en francés. "
    "REGLA 2: Usa un tono académico y profesional. "
    "REGLA 3: Proporciona ejemplos y citas en formato APA 7ma edición si es necesario."
)

# INTERFAZ
st.set_page_config(page_title="L'Atelier Français AI", page_icon="🇫🇷")
st.title("🇫🇷 L'Atelier Français AI")
st.markdown("### Tu asistente académico de francés con fonética IPA")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Escribe tu pregunta sobre francés aquí..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Configuración del modelo (Ajustado para evitar el error 404)
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash", 
        system_instruction=instruction
    )
    
    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error de conexión: {e}")
