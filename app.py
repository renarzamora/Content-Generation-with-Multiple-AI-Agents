import streamlit as st
import asyncio
from src.agents import teamconfig, orchestrate
import os
import asyncio


if 'message' not in st.session_state:
    st.session_state.messages = []

def ShowMessages(chat):
    for message in st.session_state.messages:
        if message.startswith("**Writer**"):
            with st.chat_message("ai",avatar ='assets/writer.png'):
                st.markdown(message)
        elif message.startswith("**Content critic**"):
            with st.chat_message("ai",avatar = 'assets/content.png'):
                st.markdown(message)
        elif message.startswith("**SEO Critic**"):
            with st.chat_message("ai",avatar = 'assets/seo.png'):
                st.markdown(message)
        elif message.startswith("**User**"):
            with st.chat_message("user"):
                st.markdown(message)
        elif message.startswith("**Termination"):
            with st.chat_message("system"):
                st.markdown(message)



st.title("Content Generation with Multiple Agents")
min_thresh = st.selectbox('Select the minimum score threshold to stop the agents:',
                          options=list(range(11)),
                          index=9)

chat = st.container()
ShowMessages(chat)


prompt = st.chat_input("Enter your content generation task here:")

if prompt:
    with chat:
        async def main():
            team = await teamconfig(min_score_thresh=min_thresh)
            if 'team_state' in st.session_state:
                await team.load_state(st.session_state.team_state)
            with chat:
                async for message in orchestrate(team, prompt):
                    st.session_state.messages.append(message)
                    if message.startswith("**Writer**"):
                        with st.chat_message("ai",avatar='assets/writer.png'):
                            st.markdown(message)
                    elif message.startswith("**Content critic**"):
                        with st.chat_message("ai",avatar='assets/content.png'):
                            st.markdown(message)
                    elif message.startswith("**SEO Critic**"):
                        with st.chat_message("ai",avatar='assets/seo.png'):
                            st.markdown(message)
                    elif message.startswith("**User**"):
                        with st.chat_message("user"):
                            st.markdown(message)
                    elif message.startswith("**Termination"):
                        with st.chat_message("system"):
                            st.markdown(message)
                st.session_state.team_state = await team.save_state()


        with st.spinner("Generating content..."):    
            asyncio.run(main())
            st.success("Content generation completed!")