FROM python:3.10-slim

# Install system dependencies for Playwright
RUN apt-get update && apt-get install -y \
    wget curl gnupg unzip xvfb libnss3 libatk-bridge2.0-0 libxss1 \
    libasound2 libgbm1 libgtk-3-0 libxcomposite1 libxrandr2 libxdamage1 \
    libgdk-pixbuf2.0-0 libnspr4 libx11-xcb1 libdrm2 libxfixes3 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy all files
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Install Playwright and Chromium
RUN python -m playwright install --with-deps

# Expose FastAPI port
EXPOSE 8000

# Start FastAPI app using uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

