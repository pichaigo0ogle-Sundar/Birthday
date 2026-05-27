FROM python:3.10-slim

WORKDIR /app

# Install only basic required tools (skipping software-properties-common)
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files and media assets
COPY . .

# Expose Hugging Face's default port
EXPOSE 7860

# Run Streamlit on port 7860
CMD ["streamlit", "run", "streamlit_app.py", "--server.port", "7860", "--server.address", "0.0.0.0", "--server.headless", "true", "--server.enableCORS", "false", "--server.enableXsrfProtection", "false"]
