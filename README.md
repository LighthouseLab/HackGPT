# HackGPT

Welcome to HackGPT, a powerful and customizable AI chatbot interface designed specifically for developers. With a ChatGPT-like experience, HackGPT brings a host of key features to enhance your hacking capabilities and empower your development process.

## Current Features

- **ChatGPT-like Interface**: Immerse yourself in a chat-like environment with streaming output and a typing effect. Enable or disable the typing effect based on your preference for quick responses.

- **Fine-tuning**: Tailor your HackGPT experience with the sidebar's range of options. Choose from different models like GPT-3, GPT-4, or specific models such as 'gpt-3.5-turbo'. Fine-tune model response parameters and configure API settings.

- **Set-up Prompt Selection**: Unlock more specific responses, results, and knowledge by selecting from a variety of preset set-up prompts. Additionally, craft your own custom set-up prompt for personalized interactions.

- **Knowledge Cut-off**: Utilize GPT-4's time-travel capabilities by setting a "knowledge cut-off" date. Limit the AI's knowledge to a specific time in the past and explore historical insights. Gain a greater understanding of historical events, cultural nuances, and prevailing trends.

- **On-demand Switching**: Seamlessly switch between models (GPT-3, GPT-4, etc.) and set-up prompts to unlock diverse and more dynamic AI-generated responses. Benefit from the advanced contextual understanding and improved transfer learning capabilities of different models.

## Getting Started

HackGPT is built using Python 3.9 and Streamlit. It can be easily deployed in a containerized environment using the included Docker Compose set-up.

To get started, follow the steps below:

### Docker Compose (recommended)

The easiest way to run HackGPT is to use Docker Compose. To do so, run:

```bash
docker-compose up # -d to run in background
```

To stop the container, press `Ctrl+C` in the terminal window, or run:

```bash
docker-compose stop
```

... in case you used the `-d` flag to run the container in the background.

To remove the container, run:

```bash
docker-compose down
```

### Docker (manually)

If you don't want to use Docker Compose, you can also run the container manually. To do so, run:

```bash
docker run --rm -p 8501:8501 -v $(pwd)/app:/app -w /app python:3.9-slim bash -c "pip install -r requirements.txt && streamlit run app.py"
```

### Local Python environment

If you don't want to use Docker, you can also run HackGPT in a local Python environment. To do so, run:

```bash
cd ./app
pip install -r requirements.txt
streamlit run app.py
```

## Feedback

We hope this initial release of HackGPT serves as a valuable tool for developers, encouraging exploration and experimentation with GPT-based models. Your feedback on HackGPT is highly appreciated as it will help us shape future versions of the project.

We're thrilled to have you join us in this journey of unleashing new possibilities and customizability for developers with HackGPT!

## License

This project is licensed under the terms of the ISC license. See [LICENSE](LICENSE) for more details.