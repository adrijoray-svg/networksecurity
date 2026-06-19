# Use an official lightweight Python image
FROM python:3.12-slim
# Set the working directory inside the container
WORKDIR /app
# Copy the rest of your application code
COPY . /app
# Install system dependencies (especially important for network security packages like Scapy)
RUN apt update -y && apt install awscli -y
RUN apt-get update && pip install -r requirements.txt
# Command to run your application (update main.py or command as necessary)
CMD ["python", "app.py"]