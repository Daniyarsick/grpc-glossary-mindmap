# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the requirements file into the container at /usr/src/app
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code into the container
# We need glossary_service and proto definitions
COPY . .
COPY ../proto ./proto

# Make port 8080 available to the world outside this container (for Flask)
# And port 50051 for gRPC
EXPOSE 8080 50051

# Define environment variable
ENV NAME World

# Run server.py when the container launches
CMD ["python", "server.py"]
