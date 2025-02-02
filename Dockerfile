FROM python:3.11 as builder

RUN pip install --upgrade pip
RUN pip install requests \
        python-dotenv \
        pyinstaller

WORKDIR /app
COPY src/ .

RUN pyinstaller --onefile --noconsole main.py

FROM debian:bookworm-slim
# Install required runtime libraries
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy executable and config files from builder stage
COPY --from=builder /app/dist/main .
COPY .env .
COPY config.json .

RUN chmod +x main

# Define the entry point
ENTRYPOINT ["./main"]
