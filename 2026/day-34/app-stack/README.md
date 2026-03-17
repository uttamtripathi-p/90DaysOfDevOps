# 🐳 Docker Compose App Stack

A 3-service application stack built with Docker Compose as part of a DevOps learning journey.

## Stack

| Service | Technology | Purpose |
|--------|------------|---------|
| `web` | Python Flask | Web application |
| `db` | MySQL 8.0 | Database |
| `cache` | Redis (Alpine) | Caching layer |

---

## Project Structure

```
.
├── app.py                  # Flask application
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker image for Flask app
├── docker-compose.yml      # Multi-container setup
└── .env                    # Environment variables (not committed)
```

---

## Files

### app.py
Simple Flask web app that runs on port 5000.

### Dockerfile
```dockerfile
# Base image
FROM python:3.9

# Working directory
WORKDIR /app

# Copy all files
COPY . .

# Install requirements
RUN pip install -r requirements.txt

# Run the app
CMD ["python", "app.py"]
```

### .env
Create a `.env` file in the root directory with these variables:
```
MYSQL_ROOT_PASSWORD=your_root_password
MYSQL_USER=your_user
MYSQL_PASSWORD=your_password
```

---

## docker-compose.yml

```yaml
services:
  web:
    build: .
    ports:
      - "8080:5000"
    container_name: python
    depends_on:
      db:
        condition: service_healthy
      cache:
        condition: service_started

  db:
    image: mysql:8.0
    container_name: mysql
    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
      MYSQL_USER: ${MYSQL_USER}
      MYSQL_PASSWORD: ${MYSQL_PASSWORD}
      MYSQL_DATABASE: mysqldb
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost", "-u", "root", "--password=password"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 10s
    volumes:
      - mysql_data:/var/lib/mysql

  cache:
    image: redis:alpine

volumes:
  mysql_data:
```

---

## Healthcheck

The `db` service has a healthcheck using `mysqladmin ping`. The `web` service uses `condition: service_healthy` so it only starts after MySQL is confirmed healthy — not just started.

To verify healthcheck status:
```bash
docker-compose ps              # Shows (healthy) next to db
docker inspect mysql | grep -A 10 Health
```

---

## Usage

### Start the stack
```bash
docker-compose up -d
```

### View running services
```bash
docker-compose ps
```

### View logs
```bash
docker-compose logs          # All services
docker-compose logs web      # Specific service
```

### Stop without removing
```bash
docker-compose stop
```

### Remove everything
```bash
docker-compose down
```

### Rebuild after code changes
```bash
docker-compose up --build
```

---

## Access

Once running, open your browser and visit:
```
http://localhost:8080
```

---

## Key Concepts Learned

- **Multi-container setup** with Docker Compose
- **Custom Dockerfile** for a Python Flask app
- **Named volumes** for data persistence
- **Environment variables** via `.env` file
- **depends_on** with healthcheck conditions
- **Redis** as a caching layer

---

*Built as part of a DevOps learning journey* 🚀
