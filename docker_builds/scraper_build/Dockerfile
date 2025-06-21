FROM python:3.10-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    firefox-esr \
    wget \
    curl \
    unzip \
    gnupg \
    libgtk-3-0 \
    libdbus-glib-1-2 \
    libasound2 \
    libx11-xcb1 \
    libnss3 \
    libxss1 \
    libappindicator3-1 \
    fonts-liberation \
    libatk-bridge2.0-0 \
    libxrandr2 \
    libu2f-udev \
    && apt-get clean

# Install geckodriver
ENV GECKODRIVER_VERSION v0.34.0
RUN wget -q "https://github.com/mozilla/geckodriver/releases/download/$GECKODRIVER_VERSION/geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz" \
    && tar -xvzf "geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz" \
    && mv geckodriver /usr/local/bin/ \
    && rm "geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz"

# Install Selenium
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy your script
COPY . .

CMD ["python", "raw_layer.py"]
