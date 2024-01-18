# Use an official Python runtime as a parent image
FROM python:3.11.6

# Set the working directory in the container
WORKDIR /usr/src/app

# Install Node.js
RUN curl -sL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get update && apt-get install -y nodejs

# Install system dependencies for Puppeteer and Playwright
RUN apt-get install -y \
    libnss3 \
    libnspr4 \
    libdbus-1-3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libatspi2.0-0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libasound2

# Create package.json and install Node dependencies (Puppeteer)
RUN npm init -y && \
    npm install puppeteer

# Install Playwright and necessary browsers
RUN pip install playwright && \
    playwright install

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Make port 7860 available to the world outside this container
EXPOSE 7860

# Define environment variable for OpenAI API Key
ENV OPENAI_API_KEY "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"

# Run the Python script when the container launches
CMD ["python", "./sde.py"]
