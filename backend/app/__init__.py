import os
import sqlite3
from pathlib import Path

from flask import Flask, g, jsonify
from flask_cors import CORS

BASE_DIR = Path(__file__).resolve().parent.parent
SCHEMA_PATH = BASE_DIR.parent / "docs" / "schema.sql"


def _db_path() -> Path:
    return Path(os.environ.get("SLANGBASE_DB", BASE_DIR / "slangbase.db"))


def get_db() -> sqlite3.Connection:
    if "db" not in g:
        conn = sqlite3.connect(_db_path())
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        g.db = conn
    return g.db


def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app)

    # 建表（IF NOT EXISTS，幂等）
    sql = SCHEMA_PATH.read_text(encoding="utf-8")
    path = _db_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    try:
        conn.executescript(sql)
        conn.commit()
    finally:
        conn.close()

    @app.teardown_appcontext
    def _close_db(_exc):
        db = g.pop("db", None)
        if db is not None:
            db.close()

    from app.api.tag_types import tag_types_bp

    app.register_blueprint(tag_types_bp, url_prefix="/api")

    @app.get("/api/health")
    def health():
        return jsonify({"status": "ok"})

    return app
