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
├── docker-compose.yml          ← Orchestrates the app and proxy services
├── .env                        ← Stores USER_NAME without hardcoding it in Python
├── README.md                   ← Explains the project, setup, and architecture
├── ANSWERS.md                  ← Answers to the theoretical questions
│
├── containers/
│   └── app/
│       ├── app.py              ← Python Flask app / Recipe Suggester API
│       ├── Dockerfile          ← Builds the Python app image using python:3.9-slim
│       ├── requirements.txt    ← Python dependencies, mainly Flask
│       └── .dockerignore       ← Keeps unnecessary files out of the app image
│
├── proxy/
│   └── nginx.conf              ← Nginx config: / → dashboard, /api → Python app
│
├── dashboard/
│   └── index.html              ← Static dashboard UI served by Nginx
│
└── volume/
    └── inventory.txt           ← Inventory file, editable with live update
```

---