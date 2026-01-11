import streamlit as st
import google.generativeai as genai
import os

class LanguageTutor:
    def __init__(self):
        # Configuración desde Secrets de Streamlit
        self.api_key = st.secrets.get("GOOGLE_API_KEY")
        if not self.api_key:
            st.error("Missing API Key.")
            st.stop()
        genai.configure(api_key=self.api_key)
        
        # Parámetros avanzados del modelo
        self.generation_config = {
            "temperature": 0.7,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 1024,
        }
        
        # Modelo estable para evitar error 404
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash-latest",
            generation_config=self.generation_config
        )

    def get_response(self, user_prompt):
        # Instrucción de sistema inyectada directamente
        system_context = (
            "Eres un experto en lingüística y tutor de francés. "
            "Para cada respuesta: 1. Provee la traducción. "
            "2. Incluye la transcripción IPA entre corchetes [ ]. "
            "3. Explica la regla gramatical brevemente."
        )
        try:
            full_query = f"{system_context}\n\nStudent asks: {user_prompt}"
            response = self.model.generate_content(full_query)
            return response.text
        except Exception as e:
            return f"Runtime Error: {str(e)}"

# --- UI LAYER ---
st.set_page_config(page_title="Advanced Language AI", layout="wide")
tutor = LanguageTutor()

st.title("👨‍🏫 Atelier Français: Advanced Mode")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Chat input profesional
if prompt := st.chat_input("Analyze a French sentence..."):
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    response = tutor.get_response(prompt)
    st.session_state.chat_history.append({"role": "assistant", "content": response})

for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.markdown(chat["content"])
