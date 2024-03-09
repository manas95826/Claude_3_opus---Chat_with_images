import streamlit as st
import base64
import httpx
import anthropic
from dotenv import load_dotenv
import os

load_dotenv()

ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY')

# Set up Anthropc API
client = anthropic.Anthropic()

# Streamlit app
st.title("Anthropic Insight Generator")

# Image upload
image_uploaded = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

# Prompt input
prompt = st.text_input("Enter a prompt for analysis")

# Display uploaded image
if image_uploaded is not None:
    st.image(image_uploaded, caption="Uploaded Image", use_column_width=True)

# Generate insights button
if st.button("Generate Insights"):
    if image_uploaded is not None:
        # Convert image to base64
        image_data = base64.b64encode(image_uploaded.read()).decode('utf-8')

        # Send request to Anthropc API
        message = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/jpeg",
                                "data": image_data,
                            },
                        },
                        {
                            "type": "text",
                            "text": f"{prompt}",
                        },
                    ],
                }
            ],
        )

        # Display generated insights
        st.text("Generated Insights:")
        text_content = message.content[0].text
        st.write(text_content)

# Note: Make sure to replace "claude-3-opus-20240229" with the appropriate model ID from Anthropc.
