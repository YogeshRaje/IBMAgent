import streamlit as st
import requests

# Set page layout
st.set_page_config(page_title="IBM Watson AI Chat", layout="centered")
st.title("💬 Welcome to IBM AI Agent")

# ✅ Hardcoded credentials
API_KEY = "Fk7n9-XR7UoWxUWiOaLcfvL6tyW7I8uWlqjG9Z6b-7HA"
ROLE = "user"  # Change to "Admin" or "system" if needed

# Text input for user message
content = st.text_area("Enter your message for IBM Watson:", height=100, value="what is Agentic AI")

# Submit button
if st.button("🚀 Submit to IBM Watson"):
    if not content:
        st.warning("Please enter a message.")
    else:
        try:
            with st.spinner("Authenticating with IBM Cloud..."):
                token_response = requests.post(
                    'https://iam.cloud.ibm.com/identity/token',
                    data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'}
                )
                token_response.raise_for_status()
                mltoken = token_response.json()["access_token"]

            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + mltoken
            }

            payload_scoring = {
                "messages": [
                    {"content": content, "role": ROLE}
                ]
            }

            with st.spinner("Sending message to AI model..."):
                response_scoring = requests.post(
                    'https://us-south.ml.cloud.ibm.com/ml/v4/deployments/e992616c-1334-47ab-a7b9-583a1a444a2f/ai_service?version=2021-05-01',
                    json=payload_scoring,
                    headers=headers
                )

            try:
                result = response_scoring.json()
                st.success("✅ Response from IBM Watson:")
                try:
    messages = result.get("messages", [])
    if messages:
        for msg in messages:
            st.write(f"{msg.get('role', 'AI').capitalize()}: {msg.get('content', '')}")
    else:
        st.write("No messages received from the AI.")
except Exception as e:
    st.error(f"⚠️ Failed to extract message content: {e}")
