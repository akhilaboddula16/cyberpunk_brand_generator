# Cyberpunk Brand Generator

A Streamlit-based creative tool for generating a five-asset cyberpunk-corporate
brand pack for a startup rebrand brief. The app uses `stabilityai/sdxl-turbo`
through Hugging Face Diffusers and focuses on consistent prompt design across:

- Logo concept
- Hero image
- Social media visual
- Icon set
- Dashboard mockup

## Project Goal

This project is designed around a creative brief where a tech startup needs
high-quality, brand-consistent visuals for web and social channels. Instead of
generic stock imagery, the output aims for a polished cyberpunk-corporate look
with a shared palette, lighting direction, and product-marketing tone.

## Features

- Streamlit UI for generating the full asset pack
- Editable prompts for each deliverable
- Shared negative prompt to reduce common image artifacts
- CLI entrypoint for batch generation
- Safer startup behavior when `HF_TOKEN` or output folders are missing

## System Requirements

### Hardware

**CPU (Local Setup)**
- Minimum: Intel i5 / AMD Ryzen 5 or equivalent
- Recommended: Multi-core processor for faster generation

**GPU (Recommended for faster performance)**
- NVIDIA GPU with CUDA support (e.g., RTX 3060, RTX 4090, Tesla T4)
- 6GB+ VRAM for image generation
- Not required, but significantly improves generation speed

**Memory (RAM)**
- Minimum: 8GB RAM
- Recommended: 16GB+ for smooth operation

### Software

- Python 3.8+
- CUDA 11.8+ (if using NVIDIA GPU)

### Performance Comparison

| Setup | Generation Time (per image) |
|-------|---------------------------|
| CPU only | 5-10 minutes |
| GPU (RTX 3060) | 30-60 seconds |
| Google Colab GPU (Tesla T4) | 1-2 minutes |

**Recommendation**: Use Google Colab for free GPU acceleration if you don't have a local GPU. See [GOOGLE_COLAB.md](GOOGLE_COLAB.md) for setup.

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Add your Hugging Face token using one of these options:

Option A: environment variable

```bash
set HF_TOKEN=your_token_here
```

Option B: Streamlit secrets file

Create `.streamlit/secrets.toml` with:

```toml
HF_TOKEN = "your_token_here"
```

## Run The Streamlit App

### Local Setup
```bash
streamlit run streamlit_app.py
```

### Google Colab (with GPU Support)

For faster image generation with GPU acceleration, run on Google Colab:

1. Upload your project files to Colab
2. Install dependencies
3. Set your Hugging Face token
4. Run with Streamlit headless mode

See [GOOGLE_COLAB.md](GOOGLE_COLAB.md) for detailed step-by-step instructions.

## Run The CLI Version

```bash
python app.py
```

## Output

Generated images are saved in the `generated_assets/` directory.

## Suggested Demo Flow

1. Launch the Streamlit app.
2. Review the brand brief in the sidebar.
3. Adjust prompts, filenames, or aspect ratios per asset if needed.
4. Generate the full five-image pack.
5. Download each asset from the results section.
