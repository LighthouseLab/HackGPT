# HackGPT

> A simple replica of ChatGPT, but with aimed at developers.

## Usage

### Docker Compose (recommended)

```bash
docker-compose up
docker-compose down
```

### Docker (manually)

```bash
docker run --rm -p 8501:8501 -v $(pwd)/app:/app -w /app python:3.9-slim bash -c "pip install -r requirements.txt && streamlit run app.py
```