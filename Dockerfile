# # Build Stage
# FROM python:latest AS builder

# WORKDIR /app

# COPY ./requirements.txt .

# # Install dependencies
# RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Production Stage
FROM python:3.12.3

WORKDIR /app

# Copy only the necessary files from the builder stage
COPY . /app

# Install Google Chrome and Chrome WebDriver
# RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
#     && apt-get update \
#     && apt-get install -y ./google-chrome-stable_current_amd64.deb \
#     && rm google-chrome-stable_current_amd64.deb \
#     && CHROME_DRIVER_VERSION=`curl -sS https://chromedriver.storage.googleapis.com/LATEST_RELEASE` \
#     && wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip \
#     && unzip /tmp/chromedriver.zip -d /usr/local/bin/ \
#     && rm /tmp/chromedriver.zip \
#     && chmod +x /usr/local/bin/chromedriver

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Expone el puerto 8000
EXPOSE 8000

# Comando para iniciar el servidor FastAPI
CMD ["/usr/local/bin/uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--root-path", "/api/v1", "--reload"]

