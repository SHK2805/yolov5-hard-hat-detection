# Use an official Python runtime as a parent image
FROM python:3.9.21-bookworm

# Set the working directory in the container
WORKDIR /app

# Install necessary system dependencies
RUN apt-get update -y && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxrender-dev \
    libxext6 \
    libgl1-mesa-glx \
    git

# Clone YOLOv5 repository from GitHub
RUN git clone https://github.com/ultralytics/yolov5.git

# Set working directory to YOLOv5
WORKDIR /app/yolov5

# Install YOLOv5 dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set working directory back to /app
WORKDIR /app

# Copy the rest of your application code into the container
COPY . /app

# Install any additional packages specified in your application's requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Run your application when the container launches
CMD ["python", "main.py"]
