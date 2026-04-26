import os
import time
import random
import threading
from datetime import timedelta, datetime

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required
)

import psycopg2
import psycopg2.extras
from psycopg2.errors import UniqueViolation
import bcrypt

# =========================
# CONFIG
# =========================
app = Flask(__name__)
CORS(app)

app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET", "dev_secret")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=12)

jwt = JWTManager(app)

# =========================
# DB CONFIG
# =========================
DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("DB_NAME", "bluetooth")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "123456")

# =========================
# DB CONNECTION (RETRY)
# =========================
def get_conn():
    for _ in range(10):
        try:
            return psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
        except Exception:
            print("Aguardando banco...")
            time.sleep(2)
    raise Exception("Não conectou ao banco")

# =========================
# INIT DB
# =========================
def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id SERIAL PRIMARY KEY,
            datetime TIMESTAMP,
            level VARCHAR(10),
            message TEXT
        )
    """)

    conn.commit()
    cur.close()
    conn.close()

init_db()

# =========================
# AUTO LOG GENERATOR
# =========================
def generate_logs():
    while True:
        try:
            conn = get_conn()
            cur = conn.cursor()

            latency = random.randint(10, 200)
            level = "INFO" if latency < 120 else "WARN"

            cur.execute(
                "INSERT INTO logs (datetime, level, message) VALUES (%s, %s, %s)",
                (datetime.now(), level, f"Ping {latency} ms")
            )

            conn.commit()
            cur.close()
            conn.close()

        except Exception as e:
            print("Erro auto log:", e)

        time.sleep(3)

# inicia thread em background
threading.Thread(target=generate_logs, daemon=True).start()

# =========================
# ROUTES
# =========================

@app.route("/health")
def health():
    return {"status": "ok"}, 200

@app.route("/register", methods=["POST"])
def register():
    conn = None
    try:
        data = request.get_json()

        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return {"msg": "username and password required"}, 400

        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        conn = get_conn()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            (username, hashed.decode())
        )

        conn.commit()
        cur.close()
        conn.close()

        return {"msg": "user created"}, 201

    except UniqueViolation:
        if conn:
            conn.rollback()
        return {"msg": "user already exists"}, 409

    except Exception as e:
        if conn:
            conn.rollback()
        return {"error": str(e)}, 500

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("SELECT * FROM users WHERE username=%s", (username,))
    user = cur.fetchone()

    cur.close()
    conn.close()

    if not user:
        return {"msg": "user not found"}, 404

    if not bcrypt.checkpw(password.encode(), user["password"].encode()):
        return {"msg": "invalid password"}, 401

    token = create_access_token(identity=username)

    return {"token": token}

@app.route("/logs", methods=["GET"])
@jwt_required()
def logs():
    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("SELECT * FROM logs ORDER BY datetime DESC LIMIT 50")
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify(rows)

@app.route("/")
def root():
    return {"message": "API running"}

# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)