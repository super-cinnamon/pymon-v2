# Use a base image with Python
FROM python:3.11

WORKDIR /app

COPY requirements.txt ./

RUN pip install --upgrade -r requirements.txt && \
    rm -rf /root/.cache/pip

COPY . .

RUN chmod +x entrypoint.sh

# Set default environment variables
# Discord bot token
ENV DISCORD_TOKEN=xxxx

# QDRANT collection
ENV QDRANT_URL=xxxx
ENV QDRANT_TOKEN=xxxx

# Gemini API key
ENV GEMINI_API_KEY=xxxx

# Set the entry point to the synchronization script
ENTRYPOINT ["/app/entrypoint.sh"]
