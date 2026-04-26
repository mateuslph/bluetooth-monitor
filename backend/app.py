from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import psycopg2
import os

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "supersecret"
jwt = JWTManager(app)

conn = psycopg2.connect(
    host=os.getenv("DB_HOST", "db"),
    database="bluetooth",
    user="postgres",
    password="123"
)

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    if data["user"] == "admin" and data["password"] == "123":
        token = create_access_token(identity="admin")
        return jsonify(token=token)
    return {"msg": "erro"}, 401

@app.route("/log", methods=["POST"])
def log():
    data = request.json
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO logs (datetime, level, message) VALUES (%s, %s, %s)",
        (data["datetime"], data["level"], data["message"])
    )
    conn.commit()
    return {"ok": True}

@app.route("/logs")
@jwt_required()
def logs():
    cur = conn.cursor()
    cur.execute("SELECT * FROM logs ORDER BY datetime DESC LIMIT 50")
    return jsonify(cur.fetchall())

@app.route("/stats")
@jwt_required()
def stats():
    cur = conn.cursor()
    cur.execute("SELECT level, COUNT(*) FROM logs GROUP BY level")
    return jsonify(dict(cur.fetchall()))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)