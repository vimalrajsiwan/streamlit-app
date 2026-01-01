import streamlit as st
from openai import OpenAI

st.set_page_config("AI Chat App", page_icon="🤖")

client = OpenAI(api_key= st.secrets["OPENAI_API_KEY"])

if 'openai_model' not in st.session_state:
    st.session_state.openai_model = "gpt-4o"

if "messages" not in st.session_state:
    st.session_state.messages = [{
            "role": "system",
            "content": "You are an advanced AI assistant similar to ChatGPT. You help users by answering questions, writing and reviewing code, generating ideas, explaining complex topics simply, and assisting with decision-making. You think step by step when solving problems. You adapt your response style based on the user's expertise level. You never fabricate facts and clearly indicate uncertainty. You respect user privacy and follow ethical AI principles. Your responses are helpful, accurate, and easy to read."
        }
    ]


for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("Enter Your Query"):
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model= st.session_state.openai_model,
            messages= [
                { "role": m["role"], "content": m["content"] } for m in st.session_state.messages
            ],
            max_tokens= 1000,
            stream= True
        )

        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
