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
    networks:
      - backend
    depends_on:
      db:
        condition: service_healthy
      cache:
        condition: service_started
    labels:
      app: "myapp"
      environment: "development"

  db:
    image: mysql:8.0
    restart: on-failure
    container_name: mysql
    networks:
      - backend
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
    labels:
      app: "myapp"
      environment: "development"

  cache:
    image: redis:alpine
    networks:
      - backend
    labels:
      app: "myapp"
      environment: "development"

volumes:
  mysql_data:

networks:
  backend:
```

---

## Task 2: Healthchecks & depends_on

The `db` service has a healthcheck using `mysqladmin ping`. The `web` service uses `condition: service_healthy` so it only starts after MySQL is confirmed healthy — not just started.

| Condition | Meaning |
|-----------|---------|
| `service_healthy` | Wait for healthcheck to pass |
| `service_started` | Wait for container to just start |

To verify healthcheck status:
```bash
docker-compose ps                        # Shows (healthy) next to db
docker inspect mysql | grep -A 10 Health
```

---

## Task 3: Restart Policies

| Policy | When to use |
|--------|-------------|
| `no` | Development — don't auto restart while debugging |
| `always` | Critical production services that must run 24/7 |
| `on-failure` | Apps that should restart on error but not on manual stop |
| `unless-stopped` | Like always — but respects manual stops |

---

## Task 5: Named Networks, Volumes & Labels

### Networks
Explicit networks give you control over which services can talk to each other. Defined at the bottom of compose file and attached to each service:
```yaml
networks:
  - backend
```

### Named Volumes
Persist data even after containers are removed:
```yaml
volumes:
  - mysql_data:/var/lib/mysql
```

### Labels
Metadata tags for better organization — don't affect container behavior:
```yaml
labels:
  app: "myapp"
  environment: "development"
```

---

## Task 6: Scaling

Scale web app to 3 replicas:
```bash
docker-compose up --scale web=3 -d
```

### What breaks with port mapping?
If 3 containers all try to bind to port `8080` on your machine — only one can use it. It causes a conflict.

To scale properly you need to:
- Remove `container_name` from the service
- Remove `ports` from the service
- Add a **Load Balancer** (like Nginx) in front to distribute traffic

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

### Scale web service
```bash
docker-compose up --scale web=3 -d
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
- **Restart policies** for container recovery
- **Explicit networks** for service isolation
- **Labels** for better organization
- **Scaling** and why port mapping breaks it
- **Redis** as a caching layer

---

*Built as part of a DevOps learning journey* 🚀
