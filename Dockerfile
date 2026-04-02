# Stage 1: Build WebAssembly using pygbag
FROM python:3.11-slim AS builder

WORKDIR /app
COPY requirements.txt .
COPY snake.py .

# Install pygbag
RUN pip install --no-cache-dir pygbag

# Build the project to WebAssembly
# pygbag will output the build to /app/build/web
RUN python -m pygbag --build snake.py

# Stage 2: Serve the files using Nginx
FROM nginx:alpine

# Copy the custom nginx configuration for correct WASM MIME types
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy the Pygbag build output from Stage 1
COPY --from=builder /app/build/web /usr/share/nginx/html

# Expose port (Cloud Run defaults to 8080)
EXPOSE 8080

CMD ["nginx", "-g", "daemon off;"]
