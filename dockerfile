# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpoppler-cpp-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that Streamlit runs on
EXPOSE 8501

# Set environment variables for Google Service Account and Streamlit configuration
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/authentication.json
ENV STREAMLIT_SERVER_PORT=8501

# Command to run Streamlit app
CMD ["streamlit", "run", "app.py"]
