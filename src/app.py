import streamlit as st
import asyncio
import os
from agents import teamconfig, orchestrate

# Inicialización del estado de la sesión
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Diccionario centralizado de agentes, roles y avatares
AVATARS = {
    "**Writer**": ("ai", "assets/writer.png"),
    "**Content critic**": ("ai", "assets/content.png"),
    "**SEO Critic**": ("ai", "assets/seo.png"),
    "**User**": ("user", None),
    "**Termination": ("system", None),
}

def render_message(message):
    """Renderiza un mensaje en el chat basándose en su prefijo."""
    for prefix, (role, avatar) in AVATARS.items():
        if message.startswith(prefix):
            kwargs = {"avatar": avatar} if avatar else {}
            with st.chat_message(role, **kwargs):
                st.markdown(message)
            return

def ShowMessages(chat):
    """Renderiza el historial de mensajes al recargar la página."""
    for message in st.session_state.messages:
        render_message(message)


# Interfaz principal de Streamlit
st.title("Content Generation with Multiple Agents")

min_thresh = st.selectbox(
    'Select the minimum score threshold to stop the agents:',
    options=list(range(11)),
    index=9
)

chat = st.container()
ShowMessages(chat)

prompt = st.chat_input("Enter your content generation task here:")

if prompt:
    with chat:
        async def main():
            team = await teamconfig(min_score_thresh=min_thresh)
            
            # Cargar estado previo si existe
            if 'team_state' in st.session_state:
                await team.load_state(st.session_state.team_state)
            
            with chat:
                # Bucle asíncrono sobre el orquestador
                async for message in orchestrate(team, prompt):
                    st.session_state.messages.append(message)
                    render_message(message) # <-- Reutilización de la lógica
                    
                st.session_state.team_state = await team.save_state()

        with st.spinner("Generating content..."):    
            asyncio.run(main())
            st.success("Content generation completed!")