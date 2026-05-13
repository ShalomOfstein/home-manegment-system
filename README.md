# Home Management System with Docker

## Project Overview

This project modernizes a small legacy home management system using Docker and Docker Compose.

The original system included:

- A Python recipe suggester
- A manually edited `inventory.txt` file
- A simple HTML dashboard

The goal of this project is to make the system portable so it can run on any computer with Docker installed, without depending on a specific local Python version or broken file paths.

The system is now split into two Docker services:

- `app` — a Python Flask recipe application
- `proxy` — an Nginx reverse proxy that serves the dashboard and routes API requests

---

## Project Structure

```txt
HomeManagementSystem/
│
├── containers/
│   └── app/
│       ├── app.py
│       ├── requirements.txt
│       ├── Dockerfile
│       └── .dockerignore
│
├── dashboard/
│   └── index.html
│
├── proxy/
│   └── reverse_proxy.conf
│
├── volume/
│   └── inventory.txt
│
├── .env
├── docker-compose.yml
└── README.md
```

---

## Services

### 1. Python App Service

The `app` service is the Python recipe suggester.

It is built using the Dockerfile located at:

```txt
containers/app/Dockerfile
```

The Dockerfile uses the required base image:

```dockerfile
FROM python:3.9-slim
```

This ensures that the application always runs with Python 3.9, even if the host computer has a different Python version installed.

The Python app reads:

- The owner name from the `.env` file
- The available ingredients from the mounted `inventory.txt` file

---

### 2. Flask API

The recipe suggester is implemented as a small Flask application.

Flask is used so the Python recipe logic can respond to HTTP requests. Instead of running once and exiting like a regular script, the Flask app stays running inside the container and exposes an API route:

```txt
/api
```

When a request is sent to `/api`, the Flask app:

1. Reads the owner name from the `USER_NAME` environment variable.
2. Reads the ingredients from `/data/inventory.txt`.
3. Compares the inventory with the available recipe options.
4. Returns the result as a JSON response.

Example API response:

```json
{
  "message": "Hello YourName!",
  "inventory": ["eggs", "cheese", "pasta"],
  "suggested_recipe": "Cheese omelette"
}
```

Flask runs inside the `app` container on port `5000`.

In the final setup, this port is not exposed directly to the user. Instead, Nginx forwards requests from:

```txt
http://localhost/api
```

to the Flask app internally at:

```txt
http://app:5000/api
```

---

### 3. Nginx Proxy Service

The `proxy` service runs an Nginx server.

It uses the official lightweight Nginx image:

```yaml
image: nginx:alpine
```

Nginx acts as a reverse proxy and handles two routes:

```txt
http://localhost      -> serves the static dashboard
http://localhost/api  -> forwards the request to the Python Flask app
```

The Nginx routing rules are defined in:

```txt
proxy/reverse_proxy.conf
```

The reverse proxy allows the user to interact with the whole system through one public address:

```txt
http://localhost
```

---

## Environment Variables

The owner name is stored in the `.env` file:

```env
USER_NAME=YourName
```

This value is passed into the Python container using Docker Compose.

The Python app reads this value from the environment instead of hardcoding the owner name in the source code.

This satisfies the requirement that the owner name should not be hardcoded in the script.

---

## Inventory File

The inventory file is stored on the host computer at:

```txt
volume/inventory.txt
```

It is mounted into the Python container at:

```txt
/data/inventory.txt
```

This means that when `inventory.txt` is edited on the host computer, the Python app inside the container can immediately read the updated content.

Example inventory file:

```txt
eggs
cheese
pasta
tomatoes
milk
```

The Docker Compose bind mount is what makes this possible.

---

## Docker Compose

The project uses Docker Compose to run the full system with one command.

Docker Compose starts two services:

```txt
app    -> Python Flask recipe app
proxy  -> Nginx reverse proxy
```

The `app` service is built from the local Dockerfile.

The `proxy` service uses the official Nginx image.

The services communicate through Docker’s internal network. This allows Nginx to forward API requests to the app using the service name:

```txt
app
```

For example, the Nginx config forwards requests to:

```txt
http://app:5000/api
```

---

## How to Run the Project

From the project root folder, run:

```bash
docker compose up --build
```

Then open the dashboard in a browser:

```txt
http://localhost
```

To view the raw API response, open:

```txt
http://localhost/api
```

To stop the containers, press:

```txt
CTRL + C
```

Then run:

```bash
docker compose down
```

---