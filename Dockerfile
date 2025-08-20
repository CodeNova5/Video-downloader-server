# Use official Python image
FROM python:3.9

# Install FFmpeg and other dependencies
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean

# Set working directory
WORKDIR /app

# Copy project files into the container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir flask flask-cors yt-dlp

# Expose port 8080
EXPOSE 8080

# Run the app
CMD ["python", "app.py"]
