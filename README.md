# Cyberpunk Brand Generator

A Streamlit-based creative tool for generating a five-asset cyberpunk-corporate
brand pack for a startup rebrand brief. The app uses **Hugging Face Inference API** 
with `stabilityai/sdxl-turbo` for fast, serverless image generation focused on 
consistent prompt design across:

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

- ⚡ **Streamlit Web UI** with live image generation
- ✏️ **Editable prompts** for each deliverable  
- 🎨 **Shared negative prompt** to reduce common image artifacts
- 🖥️ **CLI entrypoint** for batch generation
- 🚀 **Serverless deployment** via Hugging Face Inference API
- 📦 **Cloud-ready** - Deploy on Streamlit Cloud instantly
- 💾 **Minimal dependencies** - Only 3 packages needed

## System Requirements

### Hardware
- **Any computer** - No GPU needed! 🎉
- RAM: 512 MB minimum (2GB+ recommended)
- Internet connection (for HF API)

### Software
- Python 3.8+
- pip or conda

### Performance

| Setup | Generation Time |
|-------|-----------------|
| **Local (Any machine)** | 30-60 seconds per image |
| **Streamlit Cloud** | 30-60 seconds per image |
| **Google Colab** | 30-60 seconds per image |

**✅ No GPU required!** All computation happens on Hugging Face serverless infrastructure.

## Installation

### 1. Clone or Download the Repository
```bash
git clone https://github.com/YOUR_USERNAME/cyberpunk_brand_generator.git
cd cyberpunk_brand_generator
```

### 2. Create Virtual Environment (Recommended)
```bash
python -m venv venv

# Activate it:
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

That's it! Only 3 packages:
- `streamlit` - Web UI framework
- `huggingface_hub` - Inference API client  
- `Pillow` - Image handling

### 4. Get Your Hugging Face Token

1. Go to https://huggingface.co/settings/tokens
2. Click **"New token"**
3. Select **"Read"** permission
4. Copy your token

### 5. Add Token (Choose One)

**Option A: Environment Variable**
```bash
# Windows PowerShell
$env:HF_TOKEN = "your_token_here"

# Windows CMD
set HF_TOKEN=your_token_here

# macOS/Linux
export HF_TOKEN=your_token_here
```

**Option B: Streamlit Secrets (Recommended for Streamlit Cloud)**

Create `.streamlit/secrets.toml`:
```toml
HF_TOKEN = "your_token_here"
```

## Run Locally

### Streamlit Web App
```bash
streamlit run streamlit_app.py
```

The app will open at `http://localhost:8501`

### CLI Batch Generation
```bash
python app.py
```

Generated images are saved in `generated_assets/`

## Deploy to Streamlit Cloud

See [STREAMLIT_DEPLOYMENT.md](STREAMLIT_DEPLOYMENT.md) for step-by-step instructions.

**TL;DR:**
1. Push to GitHub
2. Go to https://streamlit.io/cloud
3. Click "New app" and select this repo
4. Add `HF_TOKEN` in Secrets
5. Done! ✨

---

## Architecture

### How It Works

```
User Input (Streamlit UI)
    ↓
ImageGenerator Class
    ↓
Hugging Face Inference API
    ↓
Stable Diffusion SDXL-Turbo
    ↓
Generated Image (PNG)
    ↓
Save to generated_assets/
```

### Key Components

| File | Purpose |
|------|---------|
| `streamlit_app.py` | Interactive web UI |
| `app.py` | CLI batch generator |
| `src/generator.py` | HF Inference API client |
| `src/prompts.py` | Brand prompts & assets config |
| `src/utils.py` | Helper functions |

### Why Hugging Face Inference API?

✅ **No GPU needed** - Computation on HF servers  
✅ **Fast startup** - 10-15 seconds, no model download  
✅ **Scalable** - Works on any machine  
✅ **Free tier** - 1,000 API calls/month included  
✅ **Production-ready** - Works on Streamlit Cloud  

---

## Troubleshooting

### "HF_TOKEN not found"
Make sure you've set the token in either:
- Environment variable: `HF_TOKEN=your_token`
- Streamlit secrets: `.streamlit/secrets.toml`

### "Rate limit exceeded"
- You've hit the free tier limit (1,000 calls/month)
- Wait 1 hour or upgrade at https://huggingface.co/billing

### "Image generation failed"
- Check your HF token is valid: https://huggingface.co/settings/tokens
- Make sure you have internet connection
- Check HF service status: https://status.huggingface.co

### App shows "Running..." forever
- Check Streamlit logs for errors
- Verify `HF_TOKEN` is set correctly
- Try restarting the app

---

## File Structure

```
cyberpunk_brand_generator/
├── app.py                 # CLI entry point
├── streamlit_app.py       # Streamlit UI
├── main.py                # Alternative entry
├── requirements.txt       # Dependencies (3 packages)
├── README.md             # This file
├── STREAMLIT_DEPLOYMENT.md  # Cloud deployment guide
├── linkedin.md           # LinkedIn post template
├── interview.md          # Interview prep guide
├── generated_assets/     # Output folder (auto-created)
└── src/
    ├── generator.py      # HF Inference API wrapper
    ├── prompts.py        # Brand prompts configuration
    └── utils.py          # Helper functions
```

---

## License

MIT - Feel free to use and modify!

---

## Resources

- **Hugging Face Docs:** https://huggingface.co/docs/api-inference
- **Streamlit Docs:** https://docs.streamlit.io
- **Stable Diffusion:** https://huggingface.co/stabilityai/sdxl-turbo
- **Deployment Guide:** [STREAMLIT_DEPLOYMENT.md](STREAMLIT_DEPLOYMENT.md)

---

**Happy generating! 🚀**
