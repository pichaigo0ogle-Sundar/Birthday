FROM python:3.10-slim

# Force python to not buffer logs (makes logs appear instantly and prevents hangs)
ENV PYTHONUNBUFFERED=1
# Force Streamlit to hide update checks and run strictly in headless production
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_CHECK_UPDATE=false

WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 7860

# Run Streamlit with strict headless and cross-origin flags
CMD ["streamlit", "run", "streamlit_app.py", "--server.port", "7860", "--server.address", "0.0.0.0"]
