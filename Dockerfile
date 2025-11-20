# Use official Python 3.11 image as base
FROM python:3.11-slim

# Set working directory in the container
WORKDIR /app

# Copy all files from current folder to /app in the container
COPY . /app

# Install required Python packages
RUN pip install --no-cache-dir pandas scikit-learn openpyxl

# Command to run the Python script when the container starts
CMD ["python", "springer-capital-son.py"]
