import streamlit as st
from huggingface_hub import InferenceClient
from datetime import datetime

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_info" not in st.session_state:
    st.session_state.user_info = {}

def login():
    logo_url = "https://club.digistartelkom.id/static/media/logo-digistar.b1a6c9ae6199b9b8b663.png"
    st.markdown(f"""
        <img src="{logo_url}" class="Logo">
    """, unsafe_allow_html=True)
    st.title("Hello, Sobat MinClub!!!", text_alignment="center")
    st.caption("Please enter your details to log in to your account.", text_alignment="center")
    username = st.text_input("Username", placeholder="Input your Username")
    password = st.text_input("Password", type="password", placeholder="••••••••")
    
    if st.button("Login", use_container_width=True):
        if username == "admin" and password == "digistarclub2026":
            st.session_state.authenticated = True
            now = datetime.now()
            current_time = now.strftime("%d %b %Y, %H:%M WIB")
            st.session_state.user_info = {
                "name": "Ilham",
                "username": username,
                "role": "Product Lead",
                "login_time": current_time  
            }
            st.rerun()
        else:
            st.error("Username atau Password salah")

if not st.session_state.authenticated:
    login()
else:
    with st.sidebar:
        st.markdown("""
            <style>
            .profile-card {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 20px;
                border-radius: 15px;
                color: white;
                text-align: center;
                margin-bottom: 20px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            }
            .avatar {
                width: 80px;
                height: 80px;
                border-radius: 50%;
                border: 3px solid rgba(255,255,255,0.3);
                margin-bottom: 10px;
                object-fit: cover;
            }
            .status-badge {
                background-color: #2ecc71;
                color: white;
                padding: 2px 10px;
                border-radius: 20px;
                font-size: 10px;
                text-transform: uppercase;
                font-weight: bold;
            }
            .user-name {
                font-size: 18px;
                font-weight: 700;
                margin: 5px 0;
            }
            .user-role {
                font-size: 12px;
                opacity: 0.8;
                margin-bottom: 10px;
            }
            </style>
        """, unsafe_allow_html=True)

        avatar_url = "https://club.digistartelkom.id/logo-digiclub.png"
        
        st.markdown(f"""
            <div class="profile-card">
                <img src="{avatar_url}" class="avatar">
                <div class="user-name">{st.session_state.user_info['name']}</div>
                <div class="user-role">{st.session_state.user_info['role']}</div>
                <span class="status-badge">● Online</span>
            </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
            <div style="
                font-size: 0.8rem; 
                color: gray; 
                text-align: center; 
                margin-top: -10px; 
                margin-bottom: 10px;
            ">
                Logged in: {st.session_state.user_info['login_time']}
            </div>
        """, unsafe_allow_html=True)

        st.divider()

        if st.button("Sign Out", use_container_width=True, type="primary"):
            st.session_state.authenticated = False
            st.session_state.user_info = {}
            st.session_state.messages = []
            st.rerun()

    st.write("### Digistar Chat Assistant")
    st.caption("Digistar Chat Assistant is an AI that helps members get information about Digistar Club.")

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
