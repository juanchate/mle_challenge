# Use the official lightweight Python image.  
FROM python:3.9-slim

# Install make  
RUN apt-get update && apt-get install -y make  
  
# Allow statements and log messages to immediately appear in the Cloud Run logs  
ENV PYTHONUNBUFFERED True  
  
# Copy local code to the container image.  
WORKDIR /app  
COPY . ./  
  
# Install production and test dependencies.  
RUN pip install -r requirements.txt -r requirements-test.txt
  
# Run the web service on container startup.  
CMD uvicorn challenge.api:app --host 0.0.0.0 --port $PORT  
