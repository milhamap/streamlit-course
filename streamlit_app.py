import streamlit as st
from huggingface_hub import InferenceClient

st.write("Digistar Chat Assistant")

st.caption("Digistar Chat Assistant is an AI that helps other members get information about Digistar Club.")

client = InferenceClient(
    model="meta-llama/Llama-3.1-8B-Instruct",
    token=st.secrets["HF_TOKEN"]
)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "You are Digistar Chat Assistant. "
                "You help members get accurate information about Digistar Club. "
                "Digistar Club is an Official Community from Living in Telkom"
                "Always Say Hello, I am Digistar Chat Assistant"
            )
        }
    ]

for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

if prompt := st.chat_input("Ask about Digistar Club"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""

        stream = client.chat.completions.create(
            messages=st.session_state.messages,
            max_tokens=512,
            stream=True,
        )

        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                token = chunk.choices[0].delta.content
                full_response += token
                placeholder.markdown(full_response + "▌")

        placeholder.markdown(full_response)

    st.session_state.messages.append(
        {"role": "assistant", "content": full_response}
    )