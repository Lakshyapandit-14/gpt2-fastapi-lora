from fastapi import FastAPI
from pydantic import BaseModel

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

app = FastAPI()

MODEL_PATH = "./gpt2_lora_model"

# load tokenizer
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
tokenizer.pad_token = tokenizer.eos_token

# load base model
base_model = AutoModelForCausalLM.from_pretrained("gpt2")

# load LoRA trained weights
model = PeftModel.from_pretrained(base_model, MODEL_PATH)

model.eval()

class Request(BaseModel):
    question: str


@app.get("/")
def home():
    return {"message": "GPT2 LoRA API running."}


@app.post("/generate")
def generate(req: Request):

    prompt = f"Instruction: {req.question}\nResponse:"

    inputs = tokenizer(prompt, return_tensors="pt")

    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_length=150,
            temperature=0.7,
            top_p=0.9
        )

    result = tokenizer.decode(output[0], skip_special_tokens=True)

    return {"answer": result}