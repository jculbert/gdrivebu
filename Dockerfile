# Use Ubuntu 22.04 as the base image
FROM ubuntu:22.04

# Set environment variables for Python (optional, but good practice)
ENV PYTHONUNBUFFERED 1

# Update package lists and install Python 3 and pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib 

# Set the working directory inside the container
#WORKDIR /app

# Copy your application code into the container
#COPY . /app

# Install any Python dependencies
#RUN pip3 install --no-cache-dir -r requirements.txt

# Define the command to run your application
#CMD ["python3", "your_script.py"]
CMD tail -f /dev/null