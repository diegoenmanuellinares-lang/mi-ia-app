import streamlit as st
import google.generativeai as genai

# CONFIGURACIÓN DE SEGURIDAD (Usa los Secrets de Streamlit)
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Falta la configuración de la API Key en los Secretos de Streamlit.")

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

# Inicializar historial
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada de texto
if prompt := st.chat_input("Escribe tu duda en francés o español..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generar respuesta con el modelo Gemini
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=instruction
    )
    
    with st.chat_message("assistant"):
        response = model.generate_content(prompt)
        st.markdown(response.text)
        
    st.session_state.messages.append({"role": "assistant", "content": response.text})
