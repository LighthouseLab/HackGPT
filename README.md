# docker-streamlit

> Basic Docker image for creating Streamlit apps with Python 3.9. Uses Caddy as a reverse proxy to serve the app, but you can easily use Streamlit's built-in server instead.

## Usage

### Docker Compose (recommended)

```bash
docker-compose up
docker-compose down
```

### Docker (manually)

```bash
docker build -t your-streamlit-app .
docker run --rm -p 8501:8501 -v $(pwd)/app:/app your-streamlit-app
docker image rm your-streamlit-app
```

Same goes for the Caddy image:

```bash
docker run --rm --name your-streamlit-app-caddy -p 80:80 -p 443:443 -v $(pwd)/Caddyfile:/etc/caddy/Caddyfile caddy:2.6.4-alpine
```