# Use an official Python runtime as a parent image
FROM python:3.11.6

# Set the working directory in the container
WORKDIR /usr/src/app

# Install system dependencies for Chrome and Node.js
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    curl \
    lsb-release \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libcups2 \
    libxkbcommon0 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libatspi2.0-0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js (use the official Node.js Docker method)
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs

# Install Python and Node.js dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt \
    && npm install -g npm@latest \
    && npm install puppeteer

# Install Playwright and necessary browsers
RUN pip install playwright \
    && playwright install

# Make ports 5000 and 7860 available to the world outside this container
EXPOSE 5000 7860

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Copy the supervisor configuration file
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Start applications using supervisord
CMD ["/usr/local/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
