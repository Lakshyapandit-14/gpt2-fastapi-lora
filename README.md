# GPT-2 LoRA FastAPI + Streamlit

Serve a LoRA-adapted GPT-2 model behind a FastAPI inference API and interact with it through a Streamlit UI. Includes Docker + docker-compose for easy local deployment.

## Features

- **FastAPI backend** exposing:
  - `GET /` health message
  - `POST /generate` text generation endpoint
- **LoRA fine-tuned weights** loaded via `peft.PeftModel`
- **Streamlit frontend** that calls the backend and displays responses
- **Dockerfile** and **docker-compose** to run backend + UI

## Repo layout

- `main.py` — FastAPI app + model loading + generation endpoint
- `frontend.py` — Streamlit UI
- `gpt2_lora_model/` — directory containing tokenizer files and LoRA adapter weights (expected at runtime)
- `Dockerfile` — container image for both services
- `docker-compose.yml` — runs `api` + `frontend` services
- `requirements.txt` — Python dependencies

## Requirements

- Python 3.9+ recommended
- (Optional) NVIDIA GPU + CUDA runtime for faster inference (Docker image is CUDA-enabled)

## Quickstart (local, no Docker)

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Ensure your LoRA adapter + tokenizer files exist in `./gpt2_lora_model`.

3. Start the API:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

4. In a new terminal, start the Streamlit app:

```bash
streamlit run frontend.py
```

5. Open the UI:

- Streamlit: `http://localhost:8501`
- API docs (Swagger): `http://localhost:8000/docs`

## Run with Docker Compose

```bash
docker compose up --build
```

Then open:

- Streamlit: `http://localhost:8501`
- API docs: `http://localhost:8000/docs`

> Note: `docker-compose.yml` currently runs `uvicorn main.py:app ...`. If you run into an import error, change it to `uvicorn main:app ...`.

## API usage

### Health

```bash
curl http://localhost:8000/
```

### Generate

```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"question": "Explain gravity in simple terms"}'
```

Response:

```json
{"answer": "..."}
```

## Configuration

- `MODEL_PATH` in `main.py` points to `./gpt2_lora_model`.
- Generation parameters are set in `main.py` (`max_length`, `temperature`, `top_p`).
- The Streamlit frontend calls `http://localhost:8000/generate` by default. If running **inside Docker**, you may want to switch it to `http://api:8000/generate`.

## Troubleshooting

- **Missing model files**: make sure `gpt2_lora_model/` contains the tokenizer and LoRA adapter artifacts.
- **Slow CPU inference**: consider using a GPU, reducing `max_length`, or using a smaller base model.
- **Docker + GPU**: you may need to configure the NVIDIA Container Toolkit and compose GPU settings.

## License

Add a license file if you plan to distribute this project.
