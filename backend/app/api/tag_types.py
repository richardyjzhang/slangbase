"""标签类型 /api/tag-types"""

import re
import sqlite3
import uuid

from flask import Blueprint, jsonify, request

from app import get_db

tag_types_bp = Blueprint("tag_types", __name__)

_COLOR_RE = re.compile(r"^#[0-9a-fA-F]{6}$")
_NOW = "strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime')"


def _validate(data, *, require_all):
    """返回 (name, color, error)。"""
    if not isinstance(data, dict):
        return None, None, "请求体必须是 JSON 对象"

    raw_name = data.get("name")
    raw_color = data.get("color")

    name = None
    if require_all or raw_name is not None:
        if not isinstance(raw_name, str) or not raw_name.strip():
            return None, None, "name 不能为空"
        name = raw_name.strip()
        if len(name) > 64:
            return None, None, "name 长度不能超过 64"

    color = None
    if require_all or raw_color is not None:
        if not isinstance(raw_color, str) or not _COLOR_RE.match(raw_color):
            return None, None, "color 必须是 #RRGGBB 形式"
        color = raw_color.lower()

    return name, color, None


def _row(db, tid):
    r = db.execute(
        "SELECT id, name, color, created_at FROM tag_types WHERE id = ?", (tid,)
    ).fetchone()
    return dict(r) if r else None


@tag_types_bp.get("/tag-types")
def list_all():
    rows = get_db().execute(
        "SELECT id, name, color, created_at FROM tag_types ORDER BY created_at"
    ).fetchall()
    return jsonify({"items": [dict(r) for r in rows]})


@tag_types_bp.post("/tag-types")
def create():
    name, color, err = _validate(request.get_json(silent=True) or {}, require_all=True)
    if err:
        return jsonify({"message": err}), 400

    db = get_db()
    new_id = uuid.uuid4().hex
    try:
        db.execute(
            f"INSERT INTO tag_types (id, name, color, created_at) VALUES (?, ?, ?, {_NOW})",
            (new_id, name, color),
        )
        db.commit()
    except sqlite3.IntegrityError:
        return jsonify({"message": f"标签类型 '{name}' 已存在"}), 409

    return jsonify(_row(db, new_id)), 201


@tag_types_bp.put("/tag-types/<tid>")
def update(tid):
    name, color, err = _validate(request.get_json(silent=True) or {}, require_all=False)
    if err:
        return jsonify({"message": err}), 400
    if name is None and color is None:
        return jsonify({"message": "至少要更新一个字段"}), 400

    db = get_db()
    if _row(db, tid) is None:
        return jsonify({"message": "标签类型不存在"}), 404

    sets, vals = [], []
    if name is not None:
        sets.append("name = ?"); vals.append(name)
    if color is not None:
        sets.append("color = ?"); vals.append(color)
    vals.append(tid)

    try:
        db.execute(f"UPDATE tag_types SET {', '.join(sets)} WHERE id = ?", vals)
        db.commit()
    except sqlite3.IntegrityError:
        return jsonify({"message": f"标签类型 '{name}' 已存在"}), 409

    return jsonify(_row(db, tid))


@tag_types_bp.delete("/tag-types/<tid>")
def delete(tid):
    db = get_db()
    cur = db.execute("DELETE FROM tag_types WHERE id = ?", (tid,))
    db.commit()
    if cur.rowcount == 0:
        return jsonify({"message": "标签类型不存在"}), 404
    return "", 204
