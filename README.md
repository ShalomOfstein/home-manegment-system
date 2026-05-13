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