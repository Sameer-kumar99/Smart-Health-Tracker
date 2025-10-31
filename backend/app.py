import binascii
import hashlib
import json
import os
import secrets
import sqlite3
from datetime import datetime
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

DB_PATH = os.path.join(os.path.dirname(__file__), "health_tracker.db")
WEB_ROOT = os.path.join(os.path.dirname(__file__), "..", "web")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            token TEXT UNIQUE NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            recorded_for TEXT NOT NULL,
            steps INTEGER DEFAULT 0,
            calories INTEGER DEFAULT 0,
            heart_rate INTEGER DEFAULT 0,
            sleep_hours REAL DEFAULT 0,
            notes TEXT DEFAULT '',
            created_at TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        )
        """
    )
    conn.commit()
    conn.close()


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    hashed = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 200_000)
    return f"{binascii.hexlify(salt).decode()}${binascii.hexlify(hashed).decode()}"


def verify_password(stored: str, password: str) -> bool:
    try:
        salt_hex, hashed_hex = stored.split("$")
    except ValueError:
        return False
    salt = binascii.unhexlify(salt_hex)
    expected = binascii.unhexlify(hashed_hex)
    derived = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 200_000)
    return secrets.compare_digest(expected, derived)


def json_response(handler: BaseHTTPRequestHandler, status: HTTPStatus, payload: dict):
    data = json.dumps(payload).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Content-Length", str(len(data)))
    handler.send_header("Access-Control-Allow-Origin", "*")
    handler.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
    handler.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
    handler.end_headers()
    handler.wfile.write(data)


class SmartHealthTrackerHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(HTTPStatus.NO_CONTENT)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.end_headers()

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/auth/register":
            self.handle_register()
        elif parsed.path == "/api/auth/login":
            self.handle_login()
        elif parsed.path == "/api/metrics":
            self.handle_create_metric()
        else:
            self.send_error(HTTPStatus.NOT_FOUND, "Unknown endpoint")

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/metrics":
            self.handle_list_metrics(parsed)
        elif parsed.path == "/api/metrics/summary":
            self.handle_summary(parsed)
        elif parsed.path == "/api/user/profile":
            self.handle_profile()
        else:
            self.serve_static(parsed.path)

    def get_request_json(self):
        length = int(self.headers.get("Content-Length", "0"))
        if length == 0:
            return {}
        body = self.rfile.read(length)
        try:
            return json.loads(body.decode("utf-8"))
        except json.JSONDecodeError:
            return {}

    def authenticate(self):
        auth_header = self.headers.get("Authorization", "")
        if not auth_header.startswith("Token "):
            return None
        token = auth_header.split(" ", 1)[1]
        conn = sqlite3.connect(DB_PATH)
        try:
            row = conn.execute(
                "SELECT users.id, users.name, users.email FROM sessions JOIN users ON sessions.user_id = users.id WHERE sessions.token = ?",
                (token,),
            ).fetchone()
            if not row:
                return None
            return {"id": row[0], "name": row[1], "email": row[2]}
        finally:
            conn.close()

    def handle_register(self):
        payload = self.get_request_json()
        name = payload.get("name", "").strip()
        email = payload.get("email", "").strip().lower()
        password = payload.get("password", "")
        if not name or not email or not password:
            json_response(self, HTTPStatus.BAD_REQUEST, {"error": "Name, email, and password are required."})
            return
        conn = sqlite3.connect(DB_PATH)
        try:
            try:
                conn.execute(
                    "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                    (name, email, hash_password(password)),
                )
                conn.commit()
            except sqlite3.IntegrityError:
                json_response(self, HTTPStatus.CONFLICT, {"error": "An account with that email already exists."})
                return
        finally:
            conn.close()
        json_response(self, HTTPStatus.CREATED, {"message": "Registration successful."})

    def handle_login(self):
        payload = self.get_request_json()
        email = payload.get("email", "").strip().lower()
        password = payload.get("password", "")
        if not email or not password:
            json_response(self, HTTPStatus.BAD_REQUEST, {"error": "Email and password are required."})
            return
        conn = sqlite3.connect(DB_PATH)
        try:
            row = conn.execute(
                "SELECT id, password, name FROM users WHERE email = ?",
                (email,),
            ).fetchone()
            if not row or not verify_password(row[1], password):
                json_response(self, HTTPStatus.UNAUTHORIZED, {"error": "Invalid credentials."})
                return
            token = secrets.token_hex(16)
            conn.execute(
                "INSERT INTO sessions (user_id, token, created_at) VALUES (?, ?, ?)",
                (row[0], token, datetime.utcnow().isoformat()),
            )
            conn.commit()
            json_response(
                self,
                HTTPStatus.OK,
                {
                    "token": token,
                    "user": {"id": row[0], "name": row[2], "email": email},
                },
            )
        finally:
            conn.close()

    def handle_create_metric(self):
        user = self.authenticate()
        if not user:
            json_response(self, HTTPStatus.UNAUTHORIZED, {"error": "Authentication required."})
            return
        payload = self.get_request_json()
        try:
            recorded_for = payload.get("recorded_for") or datetime.utcnow().date().isoformat()
            datetime.strptime(recorded_for, "%Y-%m-%d")
        except ValueError:
            json_response(self, HTTPStatus.BAD_REQUEST, {"error": "recorded_for must be YYYY-MM-DD."})
            return
        steps = int(payload.get("steps", 0) or 0)
        calories = int(payload.get("calories", 0) or 0)
        heart_rate = int(payload.get("heart_rate", 0) or 0)
        sleep_hours = float(payload.get("sleep_hours", 0) or 0)
        notes = (payload.get("notes") or "").strip()
        conn = sqlite3.connect(DB_PATH)
        try:
            conn.execute(
                """
                INSERT INTO metrics (user_id, recorded_for, steps, calories, heart_rate, sleep_hours, notes, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    user["id"],
                    recorded_for,
                    steps,
                    calories,
                    heart_rate,
                    sleep_hours,
                    notes,
                    datetime.utcnow().isoformat(),
                ),
            )
            conn.commit()
        finally:
            conn.close()
        json_response(self, HTTPStatus.CREATED, {"message": "Metric saved."})

    def handle_list_metrics(self, parsed):
        user = self.authenticate()
        if not user:
            json_response(self, HTTPStatus.UNAUTHORIZED, {"error": "Authentication required."})
            return
        params = parse_qs(parsed.query)
        start = params.get("start", [None])[0]
        end = params.get("end", [None])[0]
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        try:
            query = "SELECT recorded_for, steps, calories, heart_rate, sleep_hours, notes FROM metrics WHERE user_id = ?"
            filters = [user["id"]]
            if start:
                query += " AND recorded_for >= ?"
                filters.append(start)
            if end:
                query += " AND recorded_for <= ?"
                filters.append(end)
            query += " ORDER BY recorded_for DESC"
            rows = conn.execute(query, filters).fetchall()
            metrics = [dict(row) for row in rows]
        finally:
            conn.close()
        json_response(self, HTTPStatus.OK, {"metrics": metrics})

    def handle_summary(self, parsed):
        user = self.authenticate()
        if not user:
            json_response(self, HTTPStatus.UNAUTHORIZED, {"error": "Authentication required."})
            return
        params = parse_qs(parsed.query)
        days = int(params.get("days", [30])[0])
        conn = sqlite3.connect(DB_PATH)
        try:
            row = conn.execute(
                """
                SELECT
                    COUNT(*) as entries,
                    AVG(steps) as avg_steps,
                    AVG(calories) as avg_calories,
                    AVG(heart_rate) as avg_heart_rate,
                    AVG(sleep_hours) as avg_sleep
                FROM metrics
                WHERE user_id = ?
                    AND recorded_for >= date('now', ?)
                """,
                (user["id"], f"-{days} day"),
            ).fetchone()
            summary = {
                "entries": row[0] or 0,
                "avg_steps": round(row[1], 2) if row[1] is not None else 0,
                "avg_calories": round(row[2], 2) if row[2] is not None else 0,
                "avg_heart_rate": round(row[3], 2) if row[3] is not None else 0,
                "avg_sleep": round(row[4], 2) if row[4] is not None else 0,
            }
        finally:
            conn.close()
        json_response(self, HTTPStatus.OK, {"summary": summary})

    def handle_profile(self):
        user = self.authenticate()
        if not user:
            json_response(self, HTTPStatus.UNAUTHORIZED, {"error": "Authentication required."})
            return
        conn = sqlite3.connect(DB_PATH)
        try:
            row = conn.execute(
                "SELECT COUNT(*) FROM metrics WHERE user_id = ?",
                (user["id"],),
            ).fetchone()
            entries = row[0] if row else 0
        finally:
            conn.close()
        json_response(self, HTTPStatus.OK, {"user": {**user, "entries": entries}})

    def serve_static(self, path: str):
        if path == "/":
            path = "/index.html"
        sanitized = os.path.normpath(path.lstrip("/"))
        file_path = os.path.join(WEB_ROOT, sanitized)
        if not os.path.abspath(file_path).startswith(os.path.abspath(WEB_ROOT)):
            self.send_error(HTTPStatus.FORBIDDEN, "Invalid path")
            return
        if not os.path.exists(file_path) or os.path.isdir(file_path):
            self.send_error(HTTPStatus.NOT_FOUND, "File not found")
            return
        with open(file_path, "rb") as fh:
            content = fh.read()
        if file_path.endswith(".html"):
            content_type = "text/html; charset=utf-8"
        elif file_path.endswith(".css"):
            content_type = "text/css; charset=utf-8"
        elif file_path.endswith(".js"):
            content_type = "application/javascript; charset=utf-8"
        else:
            content_type = "application/octet-stream"
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(content)


def run_server(host: str = "0.0.0.0", port: int = 8000):
    init_db()
    server_address = (host, port)
    httpd = HTTPServer(server_address, SmartHealthTrackerHandler)
    print(f"Smart Health Tracker backend running on http://{host}:{port}")
    httpd.serve_forever()


if __name__ == "__main__":
    host = os.environ.get("HOST", "0.0.0.0")
    try:
        port = int(os.environ.get("PORT", "8000"))
    except ValueError:
        raise SystemExit("PORT environment variable must be an integer")
    run_server(host, port)
