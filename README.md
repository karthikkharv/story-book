
# 🧠 NLP-to-Image PDF Generation Pipeline

This project takes a text input (story or description), segments it into paragraphs, summarizes each, extracts keywords using a Large Language Model (LLM), generates images using Stable Diffusion based on those keywords, and finally builds a structured PDF combining images and text.

---

## 📖 Example Story Input

```
Peter is a tall guy with blond hair. Steven is a small guy with black hair. 
Peter and Steven walk together in New York when aliens attack the city. 
They are afraid and try to run for their lives. The army arrives and saves them.
```

---

## 📦 Output

- 📄 ![image](output/sample.png) — Folder containing all generated images based on each paragraph sample.
- 🖼️ ![image](output/output1.png) — A visually aligned PDF containing summarized paragraphs and generated images.

---

## 🧱 Pipeline Architecture

![architecture design](output/story-book.png)

1. **Input**  
   - User submits raw story text via Web UI or REST API.

2. **Text Segmentation**  
   - Divides input into logical paragraphs using a tailing algorithm.

3. **Summarization**  
   - Each paragraph is shortened while preserving the main meaning.

4. **Keyword Extraction**  
   - LLM extracts 3–5 visual keywords from each summary.

5. **Image Generation**  
   - Stable Diffusion generates a high-resolution image from each keyword set.

6. **PDF Layout Builder**  
   - Combines summaries and images into a clean vertical PDF layout.

7. **Serve Output**  
   - Returns download link for PDF and access to generated images.

---

## 🧪 How to Run

### Requirements

- Python 3.9+
- Pillow (PIL) — for image processing
- reportlab — for PDF generation and layout (canvas, pagesizes, units)
- stability-sdk — for Stable Diffusion API client
- google-generativeai — Google Generative AI SDK
- requests — for HTTP requests
- torch (PyTorch) with GPU support — for running Stable Diffusion models locally
- Standard Python libraries: os, json, re, io, time, warnings, random

---

### Setup

```bash
# Clone the repo
git clone https://github.com/your-repo/nlp-image-pdf-generator.git
cd nlp-image-pdf-generator

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

### API Key Configuration

You must provide API keys to run the summarization and image generation:

1. **LLM (Google Gemini)**  
   Set your Google Generative AI API key as an environment variable:
   ```bash
   export GEMINI_API_KEY="your_google_gemini_api_key"
   ```

2. **Image Generation (Stability AI)**  
   If GPU is available locally, place the SD model in model folder of stable-diffusion-webui
   for image generation .

   If GPU is not available locally, use the Stability AI API:
   ```bash
   export STABILITY_API_KEY="your_stability_ai_api_key"
   ```

---

### Run the Pipeline

```bash
python models/kartoon.py
```

The output PDF and generated images will be saved to the `output/` directory.

---

## ✨ Credits

- **Text Summarization**: Google Gemini or OpenAI GPT
- **Image Generation**: Stable Diffusion (local or Stability AI API)
- **PDF Creation**: reportlab
