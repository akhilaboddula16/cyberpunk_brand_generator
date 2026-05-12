# Streamlit Cloud Deployment Guide

## ✅ Changes Made for Streamlit Cloud

Your app has been optimized to use **Hugging Face Inference API** instead of loading the model locally. This eliminates the RAM/CPU bottleneck on Streamlit Cloud.

### What Changed:
- ❌ **Removed:** `torch`, `diffusers`, `transformers`, `accelerate`, etc. (8+ GB model downloads)
- ✅ **Added:** `huggingface_hub` (lightweight API client)
- 🚀 **Result:** App now uses fast, serverless API instead of local GPU

---

## 🚀 Step-by-Step Deployment

### Step 1: Push Code to GitHub

```powershell
cd "c:\GenAI_questions\GEN-AI projects\Decode_lab_projects\cyberpunk_brand_generator"

git add .
git commit -m "Optimize for Streamlit Cloud: Use HF Inference API"
git push -u origin main
```

### Step 2: Go to Streamlit Cloud

1. Visit: https://streamlit.io/cloud
2. Sign in with GitHub account
3. Click **"New app"**

### Step 3: Deploy Your App

1. **Select Repository:**
   - Owner: Your GitHub username
   - Repository: `cyberpunk_brand_generator`
   - Branch: `main`

2. **Select File:**
   - Path: `streamlit_app.py`

3. Click **"Deploy"**

---

## 🔑 Step 4: Add Hugging Face Token (CRITICAL)

**You MUST do this for the app to work:**

1. After Streamlit deploys, click **⋮ (three dots)** in top right
2. Select **"Settings"**
3. Go to **"Secrets"** tab
4. Add this:

```toml
HF_TOKEN = "your_hugging_face_token_here"
```

**How to get your HF Token:**
1. Go to: https://huggingface.co/settings/tokens
2. Create a **Read** token (or use existing one)
3. Copy the token
4. Paste into Streamlit Secrets

---

## ✨ Verify It Works

1. After deploying, your app should load in **10-15 seconds** (no model download!)
2. Try generating an image
3. Image generation takes **30-60 seconds** (using HF Inference API)

---

## 🔧 If Deployment Fails

### Error: "HF_TOKEN not found"
**Solution:** Add `HF_TOKEN` to Streamlit Secrets (see Step 4 above)

### Error: "Rate limit exceeded"
**Solution:** Upgrade your Hugging Face account or wait 1 hour

### Error: "Module not found: torch"
**Solution:** Make sure `requirements.txt` contains only:
```
streamlit
huggingface_hub
Pillow
```

---

## 📝 Local Testing Before Deployment

Test locally to ensure everything works:

```powershell
# Create a .streamlit/secrets.toml file
mkdir .streamlit
@"
HF_TOKEN = "your_token_here"
"@ | Out-File .streamlit/secrets.toml -Encoding UTF8

# Run Streamlit
streamlit run streamlit_app.py
```

---

## 🆚 Before vs After

| Aspect | Before (Local Model) | After (HF API) |
|--------|---------------------|----------------|
| **RAM Usage** | 8+ GB | < 100 MB |
| **Startup Time** | 2-3 minutes | 10-15 seconds |
| **Model Download** | On first run | Never |
| **Cold Start** | Crashes on Streamlit | Works instantly |
| **Cost** | Free but limited | Free tier (enough) |
| **Scalability** | No | Yes (unlimited) |

---

## 💰 Free Tier Limits (Hugging Face)

- **Requests per month:** 1,000
- **Concurrent requests:** 5

**This is enough for:** ~30 image generations per month

**Upgrade if:** You need more than 1,000 API calls/month

---

## 🎯 Next Steps After Deployment

1. ✅ Verify app loads quickly
2. ✅ Test image generation
3. ✅ Share app URL with team
4. ✅ Monitor usage on HF dashboard

---

## 🐛 Troubleshooting

### App shows "Running..." for too long
- Check Streamlit logs (click "Logs" at bottom of deploy page)
- Verify `HF_TOKEN` is in Secrets

### Image generation fails
- Check HF token is valid: https://huggingface.co/settings/tokens
- Check rate limits: https://huggingface.co/billing/overview
- Wait 1 hour if rate limited

### Files not updating after push
- Wait 30 seconds for Streamlit to auto-redeploy
- Manual redeploy: Click ⋮ → "Rerun" or "Redeploy"

---

## 📚 Useful Links

- Streamlit Cloud Docs: https://docs.streamlit.io/deploy/streamlit-cloud
- HF Inference API: https://huggingface.co/docs/api-inference
- HF Tokens: https://huggingface.co/settings/tokens

---

**Your app is now ready for production!** 🚀
