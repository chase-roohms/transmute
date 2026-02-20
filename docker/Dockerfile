# Stage 1: Build frontend
FROM node:25-alpine AS frontend-builder

WORKDIR /app/frontend
COPY frontend/ .
RUN npm install && npm run build

# Stage 2: Runtime
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Install additional system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    libmagic1 \
    libjxl-tools \
    wget \
    xvfb \
    && apt-get install --only-upgrade -y tar \
    && rm -rf /var/lib/apt/lists/*

# Install Draw.io
RUN ARCH=$(dpkg --print-architecture) && \
    if [ "$ARCH" = "amd64" ]; then \
      DRAWIO_URL="https://github.com/jgraph/drawio-desktop/releases/download/v29.3.6/drawio-amd64-29.3.6.deb"; \
    else \
      DRAWIO_URL="https://github.com/jgraph/drawio-desktop/releases/download/v29.3.6/drawio-arm64-29.3.6.deb"; \
    fi && \
    wget -q "$DRAWIO_URL" -O /tmp/drawio.deb && \
    apt-get update && apt-get install -y /tmp/drawio.deb && \
    rm /tmp/drawio.deb && \
    rm -rf /var/lib/apt/lists/*

# Copy backend code
COPY backend/ ./backend/

# Copy built frontend from builder stage
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# Copy entrypoint script
COPY docker/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Expose port
EXPOSE 3313

# Start the application
ENTRYPOINT ["/app/entrypoint.sh"]