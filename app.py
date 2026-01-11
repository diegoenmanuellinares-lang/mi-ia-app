import streamlit as st
import google.generativeai as genai

# Título de la App
st.set_page_config(page_title="Tutor de Francés")
st.title("🇫🇷 Tutor de Francés")

# Configurar la API Key desde los Secrets
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Por favor, agrega la GOOGLE_API_KEY en los Secrets de Streamlit.")

# Entrada de texto
prompt = st.text_input("Escribe tu pregunta (ej: ¿Cómo se dice hola en francés?)")

if st.button("Consultar"):
    if prompt:
        try:
            # Usamos el modelo más estable
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Le pedimos específicamente la fonética aquí en el mensaje
            full_query = f"{prompt}. Por favor, incluye la fonética IPA entre corchetes [ ]."
            
            response = model.generate_content(full_query)
            st.write("---")
            st.write(response.text)
        except Exception as e:
            st.error(f"Error técnico: {e}")
    else:
        st.warning("Por favor, escribe algo primero.")
