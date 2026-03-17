import os

import streamlit as st
import requests

# Page configuration
st.set_page_config(
    page_title="GPT-2 LoRA Assistant",
    page_icon="🤖",
    layout="centered"
)

# Custom CSS for better aesthetics
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #4CAF50;
        color: white;
    }
    .stTextInput>div>div>input {
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 GPT-2 LoRA Assistant")
st.markdown("Enter an instruction or question below to generate a response from your fine-tuned GPT-2 model.")

# Backend URL — override with BACKEND_URL env var when running inside Docker
BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000/generate")

# Text input
user_input = st.text_area("Your Instruction:", placeholder="e.g., Explain gravity in simple terms...", height=150)

if st.button("Generate Response"):
    if user_input.strip() == "":
        st.warning("Please enter some text.")
    else:
        with st.spinner("Model is thinking..."):
            try:
                # Prepare the payload
                payload = {"question": user_input}
                
                # Make request to FastAPI backend
                response = requests.post(BACKEND_URL, json=payload, timeout=60)
                
                if response.status_code == 200:
                    result = response.json()
                    st.success("Generation Complete!")
                    st.markdown("### Response:")
                    st.write(result.get("answer", "No answer received."))
                else:
                    st.error(f"Error: Backend returned status code {response.status_code}")
                    st.info("Make sure the FastAPI backend is running.")
            
            except Exception as e:
                st.error(f"Connection failed: {str(e)}")
                st.info("Is the FastAPI backend running at localhost:8000?")

st.divider()
st.caption("Powered by FastAPI + GPT-2 LoRA + Streamlit")
