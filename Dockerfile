# Use an official Python runtime as a parent image
FROM python:3.8

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Render assigns a port dynamically, ensure your application uses this port.
ENV LISTEN_PORT=8000
EXPOSE $LISTEN_PORT

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install any needed packages specified in requirements.txt
RUN python -m pip install -r requirements.txt

# Command to run the application, adjust the command to use the PORT environment variable provided by Render
CMD gunicorn SoftwareEngineeringAndAgileAssignment.wsgi:application --bind 0.0.0.0:$LISTEN_PORT
