# Use the official Python image as a base
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Update the package list and install curl
RUN apt-get update && apt-get install -y curl

# Copy the local Python requirements file to the container
COPY requirements.txt /app/

# Install the required dependencies
RUN pip install -r requirements.txt

# Copy the current directory contents into the container
COPY . /app/

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application
CMD ["python", "ping.py"]