# Use an official Python runtime as a parent image
FROM python:3.11.2-bullseye

#Set labels
LABEL org.opencontainers.image.source="https://github.com/simeononsecurity/discord-backdoors-and-breaches"
LABEL org.opencontainers.image.description="A Discord Bot for Backdoors and Breaches "
LABEL org.opencontainers.image.authors="simeononsecurity"

# Set the working directory to /app
WORKDIR /

# Copy the current directory contents into the container at /
COPY . /

RUN apt-get update && apt-get -y full-upgrade -y --no-install-recommends && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip && \
pip install --no-cache-dir discord.py discord-py-slash-command discord-py-interactions && \
pip list

# Set the environment variable for the bot token
ENV BOT_TOKEN=${BOT_TOKEN}
ENV CHANNEL_ID=${CHANNEL_ID}

# Make the entry point script executable
RUN chmod +x entrypoint.sh

# Define the default command to run when the container starts
CMD ["./entrypoint.sh"]
