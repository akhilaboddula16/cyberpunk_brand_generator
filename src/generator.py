import os
from pathlib import Path

import torch
from diffusers import DiffusionPipeline

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

    def __init__(self, model_id: str = "stabilityai/sdxl-turbo"):
        hf_token = _get_hf_token()
        if not hf_token:
            raise RuntimeError(
                "Missing Hugging Face token. Set the HF_TOKEN environment variable "
                "or add HF_TOKEN to .streamlit/secrets.toml."
            )

        self.model_id = model_id
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        dtype = torch.float16 if self.device == "cuda" else torch.float32

        self.pipe = DiffusionPipeline.from_pretrained(
            self.model_id,
            token=hf_token,
            torch_dtype=dtype
        )

        self.pipe.to(self.device)

        _ensure_output_directory()

    def _cpu_tuned_settings(self, filename: str, num_inference_steps: int, guidance_scale: float):
        if self.device != "cpu":
            return num_inference_steps, guidance_scale

        normalized_name = Path(filename).stem.lower()
        tuned_steps = max(num_inference_steps, 4)
        tuned_guidance = max(guidance_scale, 0.8)

        if "logo" in normalized_name:
            tuned_steps = max(tuned_steps, 6)
            tuned_guidance = max(tuned_guidance, 1.2)

        return tuned_steps, tuned_guidance

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
        tuned_steps, tuned_guidance = self._cpu_tuned_settings(
            filename=filename,
            num_inference_steps=num_inference_steps,
            guidance_scale=guidance_scale
        )

        image = self.pipe(
            prompt=prompt,
            negative_prompt=negative_prompt,
            width=width,
            height=height,
            num_inference_steps=tuned_steps,
            guidance_scale=tuned_guidance
        ).images[0]

        output_name = self._normalize_filename(filename)
        save_path = OUTPUT_DIR / output_name

        image.save(save_path)

        return str(save_path)

    @staticmethod
    def _normalize_filename(filename: str) -> str:
        raw_name = Path(filename).stem
        extension = Path(filename).suffix or ".png"
        safe_name = slugify_filename(raw_name)
        return f"{safe_name}{extension}"
