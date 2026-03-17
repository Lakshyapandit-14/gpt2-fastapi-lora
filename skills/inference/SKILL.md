---
name: model-inference
description: Skills for loading the LoRA model, running the FastAPI backend, and performing inference via Streamlit.
---

# Model Inference Skill

This skill provides instructions for managing and using the GPT-2 LoRA fine-tuned model.

## Model Setup
The model is located in `./gpt2_lora_model`. It consists of a base GPT-2 model with LoRA (Low-Rank Adaptation) weights.

### Loading Model (Python)
```python
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

MODEL_PATH = "./gpt2_lora_model"
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
base_model = AutoModelForCausalLM.from_pretrained("gpt2")
model = PeftModel.from_pretrained(base_model, MODEL_PATH)
model.eval()
```

## Running the API
The backend is built with FastAPI and can be started using:
```bash
python main.py
```
Or if using Uvicorn directly:
```bash
uvicorn main:app --reload
```

## Running the Frontend
The interactive UI is built with Streamlit:
```bash
streamlit run frontend.py
```

## Inference Logic
The generation logic uses standard Hugging Face `generate` method with LoRA weights active:
- `max_length`: 150
- `temperature`: 0.7
- `top_p`: 0.9
