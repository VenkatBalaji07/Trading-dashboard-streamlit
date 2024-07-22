# Use the official Python base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy specific files into the container
COPY app.py app.py
COPY requirements.txt requirements.txt
COPY Commission1.csv Commission1.csv

# Upgrade pip to the latest version
RUN pip install --no-cache-dir --upgrade pip

# Install dependencies from requirements.txt
RUN pip3 install --no-cache-dir --no-dependencies -r requirements.txt

# Expose port 8501 for Streamlit
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]