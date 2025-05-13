import streamlit as st
import requests
import json

# Page setup
st.set_page_config(page_title="Smartest AI Nutrition Assistant", layout="centered")
st.title("The Smartest AI Nutrition Assistant")

# IBM Cloud API Key
API_KEY = "LTxz3YZ5y_6Hv1nyPvrgUqzawDSlEjUgNkcxQJJuRbwE"
ROLE = "user"

# Input area
content = st.text_area(" Enter your query to Smart Assistant :", height=100, value="")

# Submit button
if st.button(" Submit"):
    if not content.strip():
        st.warning("Please enter a message.")
    else:
        try:
            with st.spinner("Getting IBM access token..."):
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

            with st.spinner("Sending request to IBM Watson..."):
                response_scoring = requests.post(
                    'https://eu-de.ml.cloud.ibm.com/ml/v4/deployments/224b60a0-1a71-44ff-8a09-c6af388d9182/ai_service?version=2021-05-01',
                    json=payload_scoring,
                    headers=headers
                )

            st.success("Raw JSON Response from IBM Watson:")

            try:
                result = response_scoring.json()
                st.code(json.dumps(result, indent=2))

                # Attempt to auto-detect the most likely text field
                extracted = None

                if isinstance(result, dict):
                    for key in ["generated_text", "text", "output", "result"]:
                        if key in result:
                            extracted = result[key]
                            break
                    if not extracted:
                        # Try first value if it's a simple structure
                        extracted = next(iter(result.values()), "Could not auto-detect output.")
                else:
                    extracted = str(result)

                st.markdown("####  Final Result:")
                st.markdown(f"<pre>{extracted}</pre>", unsafe_allow_html=True)

            except ValueError:
                st.error("❌ Could not parse response as JSON.")
                st.text(response_scoring.text)
            except Exception as e:
                st.error(f"Unexpected error: {e}")

        except requests.exceptions.RequestException as e:
            st.error(f"Network error: {e}")
        except Exception as e:
            st.error(f" Error: {e}")
