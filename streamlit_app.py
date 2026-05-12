from pathlib import Path

import streamlit as st

from src.generator import ImageGenerator
from src.prompts import ASSETS, NEGATIVE_PROMPT
from src.utils import slugify_filename


BRAND_BRIEF = """
Create a cohesive five-asset brand pack for a tech startup rebrand using a
premium cyberpunk-corporate visual language. The outputs should feel polished,
high-contrast, futuristic, and consistent enough to live across a website,
social campaign, and product marketing deck.
"""

QUALITY_PRESETS = {
    "Ultra Fast": {
        "steps": 1,
        "scale": 0.4,
        "size_multiplier": 0.4,
    },
    "Fast Draft": {
        "steps": 1,
        "scale": 0.5,
        "size_multiplier": 0.5,
    },
    "Balanced": {
        "steps": 3,
        "scale": 0.8,
        "size_multiplier": 1.0,
    },
    "High Quality": {
        "steps": 5,
        "scale": 1.0,
        "size_multiplier": 1.0,
    },
}

MODEL_OPTIONS = {
    "CPU Fastest (SD-Turbo)": "stabilityai/sd-turbo",
    "Higher Quality (SDXL-Turbo)": "stabilityai/sdxl-turbo",
}

MODEL_TIME_PER_ASSET_SECONDS = {
    "stabilityai/sd-turbo": {
        "Ultra Fast": 35,
        "Fast Draft": 60,
        "Balanced": 110,
        "High Quality": 180,
    },
    "stabilityai/sdxl-turbo": {
        "Ultra Fast": 75,
        "Fast Draft": 120,
        "Balanced": 210,
        "High Quality": 360,
    },
}


st.set_page_config(
    page_title="Cyberpunk Brand Generator",
    layout="wide"
)


def build_default_assets():
    return [dict(asset) for asset in ASSETS]


def init_session_state():
    if "assets" not in st.session_state:
        st.session_state.assets = build_default_assets()
    if "generated_images" not in st.session_state:
        st.session_state.generated_images = []
    if "generator_model_id" not in st.session_state:
        st.session_state.generator_model_id = None


def load_generator(model_id: str):
    if (
        "generator" in st.session_state and
        st.session_state.generator_model_id == model_id
    ):
        return st.session_state.generator

    try:
        st.session_state.generator = ImageGenerator(model_id=model_id)
        st.session_state.generator_model_id = model_id
        return st.session_state.generator
    except RuntimeError as exc:
        st.error(str(exc))
        st.info(
            "Create `.streamlit/secrets.toml` with `HF_TOKEN = \"your_token\"` "
            "or set the `HF_TOKEN` environment variable before starting Streamlit."
        )
        st.stop()


def render_sidebar():
    st.sidebar.header("Project Brief")
    st.sidebar.write(BRAND_BRIEF.strip())

    st.sidebar.header("Generation Settings")
    negative_prompt = st.sidebar.text_area(
        "Negative Prompt",
        NEGATIVE_PROMPT,
        height=220
    )

    quality_preset = st.sidebar.selectbox(
        "Speed / Quality",
        options=list(QUALITY_PRESETS.keys()),
        index=2
    )

    model_label = st.sidebar.selectbox(
        "Model",
        options=list(MODEL_OPTIONS.keys()),
        index=0,
        help="Use SD-Turbo for faster CPU drafts, or SDXL-Turbo for better quality."
    )
    if model_label == "CPU Fastest (SD-Turbo)":
        st.sidebar.caption(
            "Recommended for local CPU use. Balanced or High Quality will be slower, but usually much clearer than Ultra Fast."
        )
    else:
        st.sidebar.caption(
            "Best when you have GPU access. On CPU this model can be very slow."
        )

    selected_asset_names = st.sidebar.multiselect(
        "Assets To Generate",
        options=[asset["name"] for asset in st.session_state.assets],
        default=[asset["name"] for asset in st.session_state.assets[:1]]
    )

    if st.sidebar.button("Reset Asset Prompts"):
        st.session_state.assets = build_default_assets()
        st.rerun()

    return negative_prompt, quality_preset, MODEL_OPTIONS[model_label], selected_asset_names


def estimate_generation_time(model_id: str, quality_preset: str, asset_count: int) -> str:
    per_asset_seconds = MODEL_TIME_PER_ASSET_SECONDS[model_id][quality_preset]
    total_seconds = per_asset_seconds * asset_count

    if total_seconds < 60:
        return f"Estimated time: about {total_seconds} seconds"

    minutes = total_seconds // 60
    seconds = total_seconds % 60

    if seconds == 0:
        return f"Estimated time: about {minutes} minute(s)"

    return f"Estimated time: about {minutes} minute(s) {seconds} second(s)"


def render_asset_editor():
    st.subheader("Creative Direction")
    st.write(
        "Review or refine each deliverable before generating the brand pack."
    )

    for index, asset in enumerate(st.session_state.assets):
        with st.expander(
            f"{index + 1}. {asset['name']} ({asset['width']}x{asset['height']})",
            expanded=index == 0
        ):
            asset["name"] = st.text_input(
                "Asset Name",
                value=asset["name"],
                key=f"asset_name_{index}"
            )
            asset["filename"] = st.text_input(
                "Output Filename",
                value=asset["filename"],
                key=f"asset_filename_{index}"
            )
            asset["prompt"] = st.text_area(
                "Prompt",
                value=asset["prompt"].strip(),
                key=f"asset_prompt_{index}",
                height=180
            )

            size_columns = st.columns(2)
            asset["width"] = size_columns[0].number_input(
                "Width",
                min_value=256,
                max_value=1536,
                step=64,
                value=int(asset["width"]),
                key=f"asset_width_{index}"
            )
            asset["height"] = size_columns[1].number_input(
                "Height",
                min_value=256,
                max_value=1536,
                step=64,
                value=int(asset["height"]),
                key=f"asset_height_{index}"
            )


def scale_dimension(value: int, multiplier: float) -> int:
    scaled = int(value * multiplier)
    return max(128, (scaled // 64) * 64)


def generate_assets(
    generator: ImageGenerator,
    negative_prompt: str,
    quality_preset: str,
    selected_asset_names: list[str]
):
    generated_images = []
    preset = QUALITY_PRESETS[quality_preset]
    selected_assets = [
        asset for asset in st.session_state.assets
        if asset["name"] in selected_asset_names
    ]

    if not selected_assets:
        st.warning("Select at least one asset to generate.")
        return

    progress_bar = st.progress(0, text="Preparing asset generation...")

    for index, asset in enumerate(selected_assets):
        status = f"Generating {asset['name']} ({index + 1}/{len(selected_assets)})"
        progress_bar.progress(index / len(selected_assets), text=status)

        filename = asset["filename"].strip() or f"{slugify_filename(asset['name'])}.png"
        width = scale_dimension(int(asset["width"]), preset["size_multiplier"])
        height = scale_dimension(int(asset["height"]), preset["size_multiplier"])

        with st.spinner(status):
            output_path = generator.generate_image(
                prompt=asset["prompt"].strip(),
                negative_prompt=negative_prompt.strip(),
                filename=filename,
                width=width,
                height=height,
                num_inference_steps=preset["steps"]
            )

        generated_images.append(
            {
                "name": asset["name"],
                "path": output_path,
                "prompt": asset["prompt"].strip(),
                "size": f"{width}x{height}",
                "preset": quality_preset,
                "model": generator.model_id
            }
        )

    progress_bar.progress(1.0, text="Generation complete.")
    st.session_state.generated_images = generated_images


def render_generated_assets():
    if not st.session_state.generated_images:
        return

    st.subheader("Generated Assets")

    for asset in st.session_state.generated_images:
        st.markdown(f"### {asset['name']}")
        st.caption(f"{asset['size']} output • {asset['preset']} • {asset['model']}")
        st.image(asset["path"], width=700)

        with open(asset["path"], "rb") as file:
            st.download_button(
                label=f"Download {asset['name']}",
                data=file,
                file_name=Path(asset["path"]).name,
                mime="image/png",
                key=f"download_{asset['path']}"
            )


def main():
    init_session_state()

    st.title("Cyberpunk Brand Generator")
    st.write(
        "Generate a five-asset cyberpunk-corporate brand pack for a tech startup rebrand using SDXL Turbo."
    )
    st.caption(
        "Deliverables: logo concept, hero image, social media visual, icon set, and dashboard mockup."
    )
    st.info(
        "For local CPU runs, start with Logo Concept only, use the CPU Fastest model, and keep Balanced or High Quality selected for clearer output."
    )

    negative_prompt, quality_preset, model_id, selected_asset_names = render_sidebar()
    render_asset_editor()

    st.info(
        estimate_generation_time(
            model_id,
            quality_preset,
            len(selected_asset_names)
        )
    )

    if st.button("Generate Brand Pack", type="primary", use_container_width=True):
        generator = load_generator(model_id)
        generate_assets(
            generator,
            negative_prompt,
            quality_preset,
            selected_asset_names
        )
        st.success("Images generated successfully.")

    render_generated_assets()


if __name__ == "__main__":
    main()
