FROM python:3.11-slim
RUN apt-get update && apt-get install -y --no-install-recommends aria2 p7zip-full ffmpeg libmagic1 curl procps rclone && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8080
CMD ["bash", "-c", "python3 health.py & exec python3 -m bot"]
