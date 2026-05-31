
import streamlit as st
import google.generativeai as genai

# 1. Setup the Page Layout
st.set_page_config(page_title="My AI Assistant", page_icon="🤖")
st.title("🤖 My Personal AI")
st.markdown("I'm powered by Google Gemini. Ask me anything!")

# 2. Securely get the API Key (we will set this up in the next step)
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    st.error("Missing API Key! Please add it to your Streamlit secrets.")
    st.stop()

genai.configure(api_key=api_key)

# 3. Load the AI Model (Gemini 1.5 Flash is the fastest free one)
model = genai.GenerativeModel('gemini-1.5-flash')

# 4. Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. Display Previous Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. Chat Input Logic
if prompt := st.chat_input("Type a message..."):
    # Display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate and display AI response
    with st.chat_message("assistant"):
        try:
            # We use a simple message call here
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Something went wrong: {e}")
