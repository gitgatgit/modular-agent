# Modular Agent

A modular research agent built with LangChain.

## Prerequisites

- Python 3.11+
- OpenAI API Key

## Setup

1. Clone the repository
2. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
3. Add your OpenAI API key to `.env`:
   ```
   OPENAI_API_KEY=your_actual_api_key_here
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

### Local Development

Run the application directly:
```bash
python main.py
```

### Docker

#### Using Docker Compose (Recommended)

1. Make sure your `.env` file is set up with your `OPENAI_API_KEY`
2. Build and run the container:
   ```bash
   docker-compose up --build
   ```
3. The application will start in interactive mode

#### Using Docker directly

1. Build the Docker image:
   ```bash
   docker build -t modular-agent .
   ```
2. Run the container with your API key:
   ```bash
   docker run -it --env-file .env modular-agent
   ```
   Or pass the API key directly:
   ```bash
   docker run -it -e OPENAI_API_KEY=your_api_key_here modular-agent
   ```

## Usage

Once running, you can interact with the research agent. Type your queries and the agent will process them. Type `exit` or `quit` to stop the application.

