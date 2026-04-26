# 🚀 Bluetooth Monitor Dashboard

![Build](https://img.shields.io/badge/build-passing-brightgreen)
![Docker](https://img.shields.io/badge/docker-ready-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-production--ready-success)

---

## 📸 Preview

![Dashboard Preview](./docs/demo.gif)

> 💡 *Real-time monitoring dashboard with authentication and live data visualization.*

---

## 🧠 Overview

Bluetooth Monitor Dashboard is a **full-stack monitoring system** designed to simulate and visualize real-time events such as latency and connectivity.

Built with a modern architecture using:

* **Frontend:** React + Vite + Recharts + Tailwind
* **Backend:** Flask + JWT + PostgreSQL
* **Infrastructure:** Docker + Docker Compose

---

## 🎯 Goals

* Provide real-time monitoring visualization
* Implement secure authentication (JWT + bcrypt)
* Demonstrate full-stack architecture
* Simulate real-world monitoring scenarios
* Build a production-ready Docker environment

---

## ⚙️ Features

### 🔐 Authentication

* User registration & login
* Password hashing with bcrypt
* JWT-based authentication
* Protected API routes

---

### 📊 Real-Time Dashboard

* Live updating chart (latency/events)
* Automatic refresh (polling)
* Dynamic metrics (average latency)
* Visual status indicator (OK / WARNING)

---

### 📜 Logging System

* Persistent logs stored in PostgreSQL
* Log levels (INFO, WARN)
* Real-time log updates in UI

---

### 🤖 Auto Data Simulation

* Background log generator
* Random latency simulation
* Continuous data flow for testing

---

### 🐳 Dockerized Architecture

* Full environment containerized
* Easy setup with Docker Compose
* Isolated services (frontend, backend, database)

---

## 🏗️ Project Structure

```bash id="9mh67v"
bluetooth-monitor/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── package.json
│
├── docker-compose.yml
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash id="8qz7wd"
git clone https://github.com/your-username/bluetooth-monitor.git
cd bluetooth-monitor
```

---

### 2. Run with Docker

```bash id="qqmtxw"
docker compose up --build
```

---

### 3. Access the application

* Frontend → http://localhost:3000
* Backend → http://localhost:5000/health

---

## 🧪 API Usage

### Register user

```bash id="b2g2yb"
curl -X POST http://localhost:5000/register \
-H "Content-Type: application/json" \
-d '{"username":"admin","password":"123"}'
```

---

### Login

```bash id="gnb39z"
curl -X POST http://localhost:5000/login \
-H "Content-Type: application/json" \
-d '{"username":"admin","password":"123"}'
```

---

## 📊 Tech Stack

| Layer    | Technology                      |
| -------- | ------------------------------- |
| Frontend | React, Vite, Recharts, Tailwind |
| Backend  | Flask, JWT, bcrypt              |
| Database | PostgreSQL                      |
| DevOps   | Docker, Docker Compose          |

---

## 📈 Future Improvements

* ⚡ WebSocket (true real-time updates)
* 🔔 Telegram alerts
* 📊 Advanced metrics & charts
* 🧭 Sidebar navigation (SaaS layout)
* ☁️ Cloud deployment (AWS / VPS)

---

## 🧠 What I Learned

* Building a full-stack application with authentication
* Handling real-time data in frontend
* Managing Dockerized environments
* Debugging dependency issues (Node + PostCSS + Docker)
* Structuring scalable applications

---

## 👨‍💻 About Me

Developed by **Mateus Lunkes Pereira**

* 💼 Freelance Software Engineer
* 🌐 Full-stack development (React, Python, Java)
* 🚀 Focused on building real-world systems

---

## 📄 License

MIT License
