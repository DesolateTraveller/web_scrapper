import streamlit as st
from transformers import CLIPTextModel, CLIPTokenizer
from diffusers import StableDiffusionPipeline
import torch
from PIL import Image
from io import BytesIO

# Load the Stable Diffusion model from Hugging Face
model_id = "CompVis/stable-diffusion-v1-4"
pipe = StableDiffusionPipeline.from_pretrained(model_id)
pipe = pipe.to("cuda" if torch.cuda.is_available() else "cpu")

# Streamlit App Layout
st.set_page_config(page_title="Text-to-Image Generator", layout="wide")
st.title("Text-to-Image Generator with Hugging Face")
st.markdown("For best view of the app, please 'zoom-out' to 75%")

# Input Text Area
prompt = st.text_area("Enter a description for the image:", placeholder="Describe the image you want to generate...")

if st.button("Generate Image"):
    if prompt:
        with st.spinner("Generating image..."):
            # Generate the image
            try:
                image = pipe(prompt).images[0]
                
                # Display the image
                st.image(image, caption='Generated Image', use_column_width=True)
            except Exception as e:
                st.error(f"Error occurred while generating image: {e}")
    else:
        st.error("Please enter a prompt to generate an image.")
