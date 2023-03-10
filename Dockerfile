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

RUN apt-get update && apt-get -y full-upgrade -y && apt-get install -y python3-setuptools python3-dev python3-pip build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev wget libbz2-dev inetutils-ping

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip && \
pip install discord.py discord-py-slash-command discord-py-interactions && \
pip list

# Set the environment variable for the bot token
ENV BOT_TOKEN=${BOT_TOKEN}
ENV CHANNEL_ID=${CHANNEL_ID}

# Run app.py when the container launches
CMD ["python", "main.py"]