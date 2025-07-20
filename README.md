# Perplexity AI Automation via Browser Agent

A ready-to-deploy solution that lets you query Perplexity’s AI interface programmatically—even if you don’t have API access!

## Features

- **REST endpoint** to accept natural language prompts (`/search?prompt=your_question`)
- **Headless browser automation** (Playwright) mimics a real user to fetch answers
- **API-ready responses** for simple integration into your apps and automation flows
- Works with any prompt you can enter into Perplexity’s search bar

## How It Works

1. The FastAPI backend receives your request
2. Playwright launches a headless Chromium browser session
3. It navigates directly to Perplexity with the encoded search prompt
4. Extracts the main answer content and returns it as JSON

## Usage

curl "https://your-deployment-url.com/search?prompt=What%20is%20artificial%20intelligence%3F"

_RESPONSE:_.

{
"prompt": "What is artificial intelligence?",
"answer": "AI is the simulation of human intelligence processes by machines...",
"status": "success",
"method": "direct_url"
}

## Quick Start

1. Clone this repo
2. Add your details to the Dockerfile and requirements
3. Deploy on platforms like Render, Railway, or locally via Docker
4. Enjoy programmable AI answers via HTTP API!

## Technology

- FastAPI (Python)
- Playwright (Chromium-based browser automation)
- Docker

## Contributing

All feedback, ideas, and pull requests are welcome!


