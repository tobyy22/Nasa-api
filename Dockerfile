FROM python:3.8

# Set the working directory
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY . .

# Expose the port that the server listens on
EXPOSE 8001

# Set environment variables
ENV PATH="/app:${PATH}"
ENV PYTHONPATH="/app"

# Start the server
CMD ["python3", "server.py"]