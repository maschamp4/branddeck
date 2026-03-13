# Use the official Microsoft Playwright image based on Ubuntu Jammy
# This image contains Python 3 and all necessary system dependencies for Chromium
FROM mcr.microsoft.com/playwright/python:v1.40.0-jammy

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies (Playwright is included here)
RUN pip install --no-cache-dir -r requirements.txt

# Copy all the rest of your application code
COPY . .

# Expose the port Gunicorn will listen on
EXPOSE 5000

# Set the command to run your Flask application using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "300", "app:app"]
