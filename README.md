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
docker build -t hackgpt .
docker run --rm -p 8501:8501 -v $(pwd)/app:/app hackgpt
docker image rm hackgpt
```

Same goes for the Caddy image:

```bash
docker run --rm --name hackgpt-caddy -p 80:80 -p 443:443 -v $(pwd)/Caddyfile:/etc/caddy/Caddyfile caddy:2.6.4-alpine
```