# Use official Python image
FROM python:3.11-slim

# Set working directory within the container
WORKDIR /app

# Copy dependencies file first (for build speed)
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything else
COPY . .

# Expose port 5000 for Flask
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]
