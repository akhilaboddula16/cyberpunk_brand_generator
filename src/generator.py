import os
from pathlib import Path
from io import BytesIO

from huggingface_hub import InferenceClient
from PIL import Image

from src.utils import OUTPUT_DIR, create_output_directory, slugify_filename


def _get_hf_token():
    token = os.getenv("HF_TOKEN")
    if token:
        return token

    try:
        import streamlit as st
        from streamlit.errors import StreamlitSecretNotFoundError
    except ImportError:
        return None

    try:
        return st.secrets.get("HF_TOKEN")
    except StreamlitSecretNotFoundError:
        return None


def _ensure_output_directory():
    create_output_directory()


class ImageGenerator:
    """Uses Hugging Face Inference API for fast, scalable image generation."""

    def __init__(self, model_id: str = "stabilityai/sdxl-turbo"):
        hf_token = _get_hf_token()
        if not hf_token:
            raise RuntimeError(
                "Missing Hugging Face token. Set the HF_TOKEN environment variable "
                "or add HF_TOKEN to .streamlit/secrets.toml."
            )

        self.model_id = model_id
        self.client = InferenceClient(token=hf_token)
        _ensure_output_directory()

    def generate_image(
        self,
        prompt,
        negative_prompt,
        filename,
        width=1024,
        height=1024,
        num_inference_steps=4,
        guidance_scale=0.0
    ):
        """Generate image using Hugging Face Inference API."""
        try:
            # Call Hugging Face Inference API
            image = self.client.text_to_image(
                prompt=prompt,
                model=self.model_id,
                height=height,
                width=width,
            )

            output_name = self._normalize_filename(filename)
            save_path = OUTPUT_DIR / output_name

            # Save image
            if isinstance(image, bytes):
                Image.open(BytesIO(image)).save(save_path)
            else:
                image.save(save_path)

            return str(save_path)
        except Exception as e:
            raise RuntimeError(f"Image generation failed: {str(e)}")

    @staticmethod
    def _normalize_filename(filename: str) -> str:
        raw_name = Path(filename).stem
        extension = Path(filename).suffix or ".png"
        safe_name = slugify_filename(raw_name)
        return f"{safe_name}{extension}"
