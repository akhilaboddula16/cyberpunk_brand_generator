# Running Cyberpunk Brand Generator on Google Colab

This guide explains how to run the Streamlit app on Google Colab with GPU support for faster image generation.

## Prerequisites

- Google account with Colab access
- Hugging Face token for model access
- Project files available

## Step 1: Check GPU Availability

Run this in a Colab cell to verify GPU support:

```python
import torch
print("CUDA available:", torch.cuda.is_available())
print("GPU:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "No GPU detected")
```

Expected output:
```
CUDA available: True
GPU: Tesla T4
```

## Step 2: Upload Project Files

1. Click the folder icon in the Colab sidebar
2. Use "Choose Files" to upload your project zip file
3. Extract the files:

```python
!unzip colab_upload_cyberpunk.zip -d /content/cybetounk_brand_generator
%cd /content/cybetounk_brand_generator
!ls
```

## Step 3: Install Dependencies

```bash
!pip install -q -r requirements.txt
```

## Step 4: Set Up Hugging Face Token

```python
import os
from getpass import getpass

os.environ["HF_TOKEN"] = getpass("Enter your Hugging Face token: ")
```

## Step 5: Run Streamlit with Colab

Use this command to run Streamlit headless with a public link:

```bash
!python -m streamlit run streamlit_app.py --server.headless true --server.port 8501 --server.enableCORS false --server.enableXsrfProtection false > streamlit.log 2>&1 &
```

## Step 6: Get the Access Link

After running Streamlit, get the proxy port link:

```python
from google.colab import output
print(output.eval_js("google.colab.kernel.proxyPort(8501)"))
```

Or check the output:

```bash
!tail -n 200 streamlit.log
```

Look for a link like: `https://8501-gpu-t4-s-kkb-euw4c2-2cc0h14vh7k90-c.europe-west4-2.prod.colab.dev`

## Troubleshooting

### Check Logs
If the app crashes, check the detailed logs:

```bash
!tail -n 200 streamlit.log
```

### Kill and Restart Streamlit
```bash
!pkill -f streamlit
!python -m streamlit run streamlit_app.py --server.headless true --server.port 8501 --server.enableCORS false --server.enableXsrfProtection false > streamlit.log 2>&1 &
```

### Connection Issues
If the link stops working, restart the Streamlit process and generate a new link.

## Performance Benefits

- **GPU Acceleration**: NVIDIA Tesla T4 GPU significantly speeds up image generation
- **Free Tier**: Google Colab offers free GPU access for development
- **No Local Setup**: Avoid driver and CUDA installation complexities

## Notes

- Colab sessions have usage limits (idle timeout, 12-hour max session)
- Generated assets are saved in `/content/cybetounk_brand_generator/generated_assets/`
- Download your assets before the session ends
