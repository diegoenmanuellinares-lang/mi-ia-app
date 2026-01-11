import streamlit as st
import google.generativeai as genai

# Configuración básica de la página
st.set_page_config(page_title="Tutor de Francés AI", page_icon="🇫🇷")
st.title("🇫🇷 Tutor de Francés")
st.write("Escribe tu duda y te ayudaré con la traducción y fonética IPA.")

# Conexión con la API Key (usando tus Secrets de Streamlit)
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Error: No se encontró la API Key en los Secrets.")

# Entrada de usuario
user_input = st.text_input("¿Qué quieres aprender hoy?", placeholder="Ej: ¿Cómo se dice gracias?")

if st.button("Consultar"):
    if user_input:
        try:
            # EL CAMBIO CLAVE: Nombre del modelo actualizado
            model = genai.GenerativeModel('gemini-1.5-flash-latest')
            
            # Instrucción directa en el mensaje
            prompt_final = f"Actúa como tutor de francés académico. Responde a: '{user_input}'. Incluye siempre la fonética IPA entre corchetes [ ]."
            
            response = model.generate_content(prompt_final)
            
            st.markdown("---")
            st.markdown(response.text)
            
        except Exception as e:
            st.error(f"Error del sistema: {e}")
    else:
        st.warning("Escribe algo antes de presionar el botón.")
