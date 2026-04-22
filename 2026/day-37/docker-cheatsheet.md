# 🐳 Docker Revision Notes

---

## 🔲 Container Commands

| Command | Description |
|--------|-------------|
| `docker run` | Starts a container from an image |
| `docker ps` | Lists all running containers |
| `docker stop <cont_id>` | Stops the specified container |
| `docker rm <cont_id>` | Removes the specified container |
| `docker exec` | Enter inside a running container |
| `docker logs <cont_id>` | Shows logs of the specified container |

---

## 🖼️ Image Commands

| Command | Description |
|--------|-------------|
| `docker build` | Builds an image from a Dockerfile |
| `docker pull` | Pulls an image from Docker Hub |
| `docker push` | Pushes a local image to Docker Hub |
| `docker tag` | Tags an image before pushing to Docker Hub |
| `docker image ls` | Shows all locally available images |
| `docker rmi <image_id>` | Removes the specified image |

---

## 💾 Volume Commands

| Command | Description |
|--------|-------------|
| `docker volume create` | Creates a new volume |
| `docker volume ls` | Lists all volumes |
| `docker volume inspect` | Shows volume info (created-on, mountpoint, etc.) |
| `docker volume rm` | Removes an existing volume |

---

## 🌐 Network Commands

| Command | Description |
|--------|-------------|
| `docker network create` | Creates a new network |
| `docker network ls` | Lists all available networks |
| `docker network inspect` | Shows network info (attached containers, config, etc.) |
| `docker network connect` | Connects a container to a specified network |

---

## 🧩 Compose Commands

| Command | Description |
|--------|-------------|
| `docker compose up` | Builds images and starts containers for all services in the compose file |
| `docker compose down` | Stops and removes all compose containers and networks |
| `docker compose ps` | Lists all running containers started from the compose file |
| `docker compose logs` | Shows logs for the compose file and its services |
| `docker compose build` | Only builds images for services — does NOT start containers |

---

## 🧹 Cleanup Commands

| Command | Description |
|--------|-------------|
| `docker image prune` | Removes all unused images |
| `docker container prune` | Removes all stopped containers |
| `docker network prune` | Removes all unused networks |
| `docker volume prune` | Removes all unused volumes |
| `docker system prune` | Removes ALL unused objects (images, containers, networks, volumes) in one command |
| `docker system df` | Shows disk space consumed by the Docker daemon |

---

## 📄 Dockerfile Instructions

| Instruction | Description |
|------------|-------------|
| `FROM` | Specifies the base image to use |
| `RUN` | Executes a command during the **image build** process |
| `COPY` | Copies files from your local system into the image |
| `WORKDIR` | Sets the working directory (opened by default when you enter a container) |
| `EXPOSE` | Documents which port the app listens on — does **not** actually publish the port (use `-p` in `docker run` for that) |
| `CMD` | Sets the **default command** when the container starts — can be **overridden** at runtime — written as a JSON array e.g. `["node", "app.js"]` |
| `ENTRYPOINT` | Defines the **main executable** — harder to override at runtime — better for fixed entrypoints |

### CMD vs ENTRYPOINT

| | `CMD` | `ENTRYPOINT` |
|--|-------|--------------|
| Purpose | Default command | Main executable |
| Overridable at runtime? | ✅ Yes, easily | ❌ Only with `--entrypoint` flag |
| Often used together? | ✅ Yes | ✅ Yes |

> **Tip:** Use `ENTRYPOINT` for the fixed command and `CMD` for default arguments that can be overridden.

---

*Happy Dockering! 🚀*
