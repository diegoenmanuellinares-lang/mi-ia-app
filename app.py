import streamlit as st
import google.generativeai as genai

# CONFIGURACIÓN DE SEGURIDAD (Carga la API Key desde los Secrets de Streamlit)
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Falta la configuración de la API Key en los Secretos de Streamlit.")

# INSTRUCCIONES ACADÉMICAS (Personalidad de la IA para idiomas)
# Estas instrucciones definen el comportamiento de tu tutor personalizado
instruction = (
    "Eres 'L'Atelier Français AI', un tutor de francés especializado para estudiantes universitarios. "
    "REGLA 1: Siempre incluye la transcripción fonética IPA entre corchetes [ ] para cada palabra o frase en francés. "
    "REGLA 2: Usa un tono académico, amable y profesional. "
    "REGLA 3: Proporciona ejemplos claros y, si es necesario, cita fuentes según la norma APA 7ma edición."
)

# INTERFAZ DE LA APLICACIÓN (Streamlit UI)
st.set_page_config(page_title="L'Atelier Français AI", page_icon="🇫🇷", layout="centered")

st.title("🇫🇷 L'Atelier Français AI")
st.markdown("### Tu asistente académico de francés con fonética IPA")
st.info("Este proyecto ha sido desarrollado para apoyar el aprendizaje de idiomas con rigor científico.")

# Inicializar el historial de conversación en la sesión
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar los mensajes previos del chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada de texto del usuario
if prompt := st.chat_input("Escribe tu pregunta sobre francés aquí..."):
    # Agregar mensaje del usuario al historial
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Configuración del modelo Gemini (Corrección del error NotFound)
    # Se usa el prefijo 'models/' para asegurar la ruta correcta en la API
    model = genai.GenerativeModel(
        model_name="models/gemini-1.5-flash",
        system_instruction=instruction
    )
    
    # Generar respuesta
    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
            # Agregar respuesta de la IA al historial
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Hubo un error al conectar con la IA: {e}")
