import os
import time
import random
import threading
from datetime import datetime, timedelta

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required

import psycopg2
import psycopg2.extras
from psycopg2.errors import UniqueViolation
import bcrypt

# =========================
# APP
# =========================
app = Flask(__name__)
CORS(app)

app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET", "dev_secret")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=12)

jwt = JWTManager(app)

# =========================
# DB CONFIG
# =========================
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise Exception("❌ DATABASE_URL não definida no ambiente")

# =========================
# DB CONNECTION
# =========================
def get_conn():
    for i in range(10):
        try:
            return psycopg2.connect(DATABASE_URL)
        except Exception:
            print(f"⏳ Tentando conectar ao banco... ({i+1}/10)")
            time.sleep(2)

    raise Exception("❌ Não conseguiu conectar no banco")

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

    print("✅ Banco inicializado")

# =========================
# AUTO LOG
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

        time.sleep(5)

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

    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("SELECT * FROM users WHERE username=%s", (data.get("username"),))
    user = cur.fetchone()

    cur.close()
    conn.close()

    if not user:
        return {"msg": "user not found"}, 404

    if not bcrypt.checkpw(data.get("password").encode(), user["password"].encode()):
        return {"msg": "invalid password"}, 401

    token = create_access_token(identity=user["username"])
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

# =========================
# STARTUP CONTROLADO
# =========================
def start_background_tasks():
    init_db()
    threading.Thread(target=generate_logs, daemon=True).start()

# roda apenas uma vez por processo
start_background_tasks()