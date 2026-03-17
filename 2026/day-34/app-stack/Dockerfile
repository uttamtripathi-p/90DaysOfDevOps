# Base image
FROM python:3.9

# Working directory
WORKDIR /app

# Copy all files
COPY . .

# To install requirements

RUN pip install -r requirements.txt

# Command to execute

CMD ["python", "app.py"]
