FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y wget gnupg curl unzip xvfb libnss3 libatk-bridge2.0-0 libxss1 libasound2 libgbm1 libgtk-3-0

# Set working directory
WORKDIR /app

# Copy everything
COPY . .

# Install Python packages
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Install Playwright & browsers
RUN pip install playwright
RUN playwright install chromium

# Expose port for FastAPI
EXPOSE 8000

# Start app
CMD ["./start.sh"]
