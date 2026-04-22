
# Base image 
FROM python:3.9-slim AS builder

# Working directory

WORKDIR /app

# Copying data

COPY . .

# Adding non-root user
RUN useradd -m appuser

# running python command

RUN pip install -r requirements.txt

# Defining user
USER appuser

# Running command
CMD ["python","app.py"]

# Exposing port
EXPOSE 5000
