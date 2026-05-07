"""标签 /api/tags"""

import sqlite3
import uuid

from flask import Blueprint, jsonify, request

from app import get_db

tags_bp = Blueprint("tags", __name__)

_NOW = "strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime')"


def _validate(data, *, require_all):
    """返回 (tag_type_id, name, error)。"""
    if not isinstance(data, dict):
        return None, None, "请求体必须是 JSON 对象"

    raw_tid = data.get("tag_type_id")
    raw_name = data.get("name")

    tag_type_id = None
    if require_all or raw_tid is not None:
        if not isinstance(raw_tid, str) or not raw_tid.strip():
            return None, None, "tag_type_id 不能为空"
        tag_type_id = raw_tid.strip()

    name = None
    if require_all or raw_name is not None:
        if not isinstance(raw_name, str) or not raw_name.strip():
            return None, None, "name 不能为空"
        name = raw_name.strip()
        if len(name) > 64:
            return None, None, "name 长度不能超过 64"

    return tag_type_id, name, None


def _type_exists(db, tid: str) -> bool:
    r = db.execute("SELECT 1 FROM tag_types WHERE id = ?", (tid,)).fetchone()
    return r is not None


def _row(db, tag_id: str):
    r = db.execute(
        """
        SELECT t.id, t.tag_type_id, t.name, t.created_at,
               tt.name AS tag_type_name, tt.color AS tag_type_color
        FROM tags t
        JOIN tag_types tt ON tt.id = t.tag_type_id
        WHERE t.id = ?
        """,
        (tag_id,),
    ).fetchone()
    return dict(r) if r else None


@tags_bp.get("/tags")
def list_all():
    tag_type_id = request.args.get("tag_type_id", type=str)
    db = get_db()
    sql = """
        SELECT t.id, t.tag_type_id, t.name, t.created_at,
               tt.name AS tag_type_name, tt.color AS tag_type_color
        FROM tags t
        JOIN tag_types tt ON tt.id = t.tag_type_id
    """
    args = []
    if tag_type_id and tag_type_id.strip():
        sql += " WHERE t.tag_type_id = ?"
        args.append(tag_type_id.strip())
    sql += " ORDER BY t.created_at"
    rows = db.execute(sql, args).fetchall()
    return jsonify({"items": [dict(r) for r in rows]})


@tags_bp.post("/tags")
def create():
    tag_type_id, name, err = _validate(request.get_json(silent=True) or {}, require_all=True)
    if err:
        return jsonify({"message": err}), 400

    db = get_db()
    if not _type_exists(db, tag_type_id):
        return jsonify({"message": "标签类型不存在"}), 400

    new_id = uuid.uuid4().hex
    try:
        db.execute(
            f"INSERT INTO tags (id, tag_type_id, name, created_at) VALUES (?, ?, ?, {_NOW})",
            (new_id, tag_type_id, name),
        )
        db.commit()
    except sqlite3.IntegrityError:
        return jsonify({"message": f"该类型下已存在名为「{name}」的标签"}), 409

    return jsonify(_row(db, new_id)), 201


@tags_bp.put("/tags/<tid>")
def update(tid):
    tag_type_id, name, err = _validate(request.get_json(silent=True) or {}, require_all=False)
    if err:
        return jsonify({"message": err}), 400
    if tag_type_id is None and name is None:
        return jsonify({"message": "至少要更新一个字段"}), 400

    db = get_db()
    current = _row(db, tid)
    if current is None:
        return jsonify({"message": "标签不存在"}), 404

    next_tid = tag_type_id if tag_type_id is not None else current["tag_type_id"]
    if tag_type_id is not None and not _type_exists(db, next_tid):
        return jsonify({"message": "标签类型不存在"}), 400

    sets, vals = [], []
    if tag_type_id is not None:
        sets.append("tag_type_id = ?")
        vals.append(tag_type_id)
    if name is not None:
        sets.append("name = ?")
        vals.append(name)
    vals.append(tid)

    try:
        db.execute(f"UPDATE tags SET {', '.join(sets)} WHERE id = ?", vals)
        db.commit()
    except sqlite3.IntegrityError:
        dup_name = name if name is not None else current["name"]
        return jsonify({"message": f"该类型下已存在名为「{dup_name}」的标签"}), 409

    return jsonify(_row(db, tid))


@tags_bp.delete("/tags/<tid>")
def delete(tid):
    db = get_db()
    cur = db.execute("DELETE FROM tags WHERE id = ?", (tid,))
    db.commit()
    if cur.rowcount == 0:
        return jsonify({"message": "标签不存在"}), 404
    return "", 204
