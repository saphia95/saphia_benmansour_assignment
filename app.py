import sqlite3
from flask import Flask, request
from flask_expects_json import expects_json

from werkzeug import Response

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    conn.execute(f"PRAGMA foreign_keys = ON;")
    return conn


page_schema = {
  "type": "object",
  "properties": {
    "name": {"type": "string"},
  },
  "required": ["name"]
}


@app.route('/page/', methods=('POST',))
@expects_json(page_schema)
def page():
    name = request.json['name']

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(f"INSERT INTO pages (name) VALUES ('{name}')")
    cursor.execute(f"SELECT * from pages where id = {cursor.lastrowid}")
    record = cursor.fetchone()

    conn.commit()
    conn.close()

    return {"id": record['id'],
            "created_at": record['created_at'],
            "name": record['name']}


video_schema = {
  "type": "object",
  "properties": {
    "title": {"type": "string"},
    "page_id": {"type": "integer"},
  },
  "required": ["title", "page_id"]
}


@app.route('/video/', methods=('POST',))
@expects_json(video_schema)
def video():
    if request.method == 'POST':
        title = request.json['title']
        page_id = request.json['page_id']

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(f"INSERT INTO videos (title, page_id) VALUES ('{title}', '{page_id}')")
        except:
            return Response(f"Page id {page_id} do not exist", status=404, mimetype='application/json')

        cursor.execute(f"SELECT * from videos where id = {cursor.lastrowid}")
        record = cursor.fetchone()

        conn.commit()
        conn.close()

    return {"id": record['id'],
            "created_at": record['created_at'],
            "title": record['title'],
            "page_id": record['page_id'],
            }


@app.route("/video/<string:video_id>", methods=["DELETE"])
def video_delete(video_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(f"DELETE FROM videos where id={video_id}")
        conn.commit()
        conn.close()
    except:
        return Response(f"Video id {video_id} do not exist", status=404, mimetype='application/json')
    return f"SUCCESS : Video id {video_id} has been deleted"


video_insight_schema = {
  "type": "object",
  "properties": {
    "videos_insights": {
        "type": "array",
        "properties": {
            "video_id": {"type": "integer"},
            "likes": {"type": "integer"},
            "views": {"type": "integer"},
        }
    },
  }
}


@app.route('/videos_insights/', methods=('POST',))
@expects_json(video_insight_schema)
def video_insight():
    if request.method == 'POST':
        videos_insights = request.json['videos_insights']
        videos_insights = [tuple(video_insight.values()) for video_insight in videos_insights]
        videos_insights_str = str(videos_insights)[1:-1]

        conn = get_db_connection()
        cursor = conn.cursor()

        query = f"INSERT INTO video_insight (video_id, likes, views) VALUES {videos_insights_str}"

        try:
            cursor.execute(query)
        except:
            return Response(f"One or multiple video_id are not available", status=404, mimetype='application/json')

        cursor.execute(f"SELECT * from video_insight;")
        records = cursor.fetchall()

        conn.commit()
        conn.close()

        results = []
        for record in records:
            result = {
                "id": record['id'],
                "created_at": record['created_at'],
                "video_id": record['video_id'],
                "likes": record['likes'],
                "views": record['views']
            }
            results.append(result)

    return {"videos_insights": results}
