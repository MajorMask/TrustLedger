# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-hun \
    libtesseract-dev \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    libtiff-dev \
    libglib2.0-0 \
    wget \
    git \
    && apt-get clean

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
        transformers \
        torch \
        Pillow \
        pytesseract \
        sentencepiece \
        flask \
        sacremoses

# Verify Tesseract installation
RUN tesseract --version

# Expose the port the app runs on
EXPOSE 5000

# Define environment variables
ENV LC_ALL=C
ENV LANG=C
ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/4.00/tessdata

# Run the application
CMD ["python", "app.py"]