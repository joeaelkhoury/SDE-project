# # Use an official Python runtime as a parent image
# FROM python:3.11.6

# # Set the working directory in the container
# WORKDIR /usr/src/app

# # Install Node.js
# RUN curl -sL https://deb.nodesource.com/setup_20.x | bash - && \
#     apt-get update && apt-get install -y nodejs

# # Install system dependencies for Puppeteer and Playwright
# RUN apt-get install -y \
#     libnss3 \
#     libnspr4 \
#     libdbus-1-3 \
#     libatk1.0-0 \
#     libatk-bridge2.0-0 \
#     libcups2 \
#     libdrm2 \
#     libxkbcommon0 \
#     libatspi2.0-0 \
#     libxcomposite1 \
#     libxdamage1 \
#     libxfixes3 \
#     libxrandr2 \
#     libgbm1 \
#     libasound2

# # Create package.json and install Node dependencies (Puppeteer)
# RUN npm init -y && \
#     npm install puppeteer

# # Install Playwright and necessary browsers
# RUN pip install playwright && \
#     playwright install

# # Copy the current directory contents into the container at /usr/src/app
# COPY . .

# # Install Python dependencies
# COPY requirements.txt ./
# RUN pip install --no-cache-dir -r requirements.txt

# # Make port 7860 available to the world outside this container
# EXPOSE 7860

# # Define environment variable for OpenAI API Key
# ENV OPENAI_API_KEY "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"

# # Run the Python script when the container launches
# CMD ["python", "./sde.py"]


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

# # Define environment variable for OpenAI API Key and Auth0 details
# # ENV OPENAI_API_KEY="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"
# # ENV AUTH0_DOMAIN="https://dev-52g2mrlpglpuz2lf.eu.auth0.com"
# # ENV AUTH0_CLIENT_ID="PxaSgxxgVo3Jbh3wICgXCZr67h2JZdeK"
# # ENV AUTH0_CLIENT_SECRET="6GwQdYHETa1lU0F_tLBOOtjAAe4AU0F4fcr-4N0A3r47Navd16N67z6QhN-WJocq"

# Copy the supervisor configuration file
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Start applications using supervisord
CMD ["/usr/local/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
