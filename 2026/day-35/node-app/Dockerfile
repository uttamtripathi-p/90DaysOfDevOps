# Base image
FROM node:20.11.0-bookworm-slim AS build

# Working directory
WORKDIR /app

# Copy files
COPY package*.json ./ 

# Installing dependencies

RUN npm install 

COPY . .

RUN useradd -m appuser

FROM gcr.io/distroless/nodejs20-debian12 AS deployer

COPY --from=build /app /app

WORKDIR /app

EXPOSE 3000

COPY --from=build /etc/passwd /etc/passwd
USER appuser


CMD ["app.js"]

