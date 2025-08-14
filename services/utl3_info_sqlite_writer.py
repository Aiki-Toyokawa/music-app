# utl3_info_sqlite_writer.py
import os
import json
import sqlite3
from datetime import datetime, timedelta
from typing import Any, Dict, Tuple

# DBパスは中央集約（dl直下）にしています。必要なら呼び出し側で上書き可。
DEFAULT_DB_PATH = os.path.join("dl", "metadata.sqlite3")

def _ensure_schema(conn: sqlite3.Connection) -> None:
    conn.execute("""
    CREATE TABLE IF NOT EXISTS videos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        -- user_data 相当
        user_edited_title   TEXT,
        user_download_date_time TEXT,
        user_notes          TEXT,
        user_tags_json      TEXT,

        -- raw_data 相当
        title               TEXT,
        target_url          TEXT,
        thumbnail_url       TEXT,
        uploader            TEXT,
        uploader_id         TEXT,
        uploader_url        TEXT,
        channel             TEXT,
        channel_id          TEXT,
        channel_url         TEXT,
        duration            TEXT,
        serial_duration     INTEGER,
        upload_date         TEXT,
        release_date        TEXT,
        video_id            TEXT NOT NULL UNIQUE,
        site_name           TEXT,

        highest_video_quality TEXT,
        highest_audio_quality TEXT,
        actual_video_quality  TEXT,
        actual_audio_quality  TEXT,

        video_width         INTEGER,
        video_height        INTEGER,
        age_limit           INTEGER,
        view_count          INTEGER,
        like_count          INTEGER,
        dislike_count       INTEGER,

        categories_json     TEXT,
        video_tags_json     TEXT,
        description_json    TEXT,

        created_at          TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S','now')),
        updated_at          TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S','now'))
    );
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_videos_video_id ON videos(video_id);")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_videos_channel_id ON videos(channel_id);")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_videos_uploader_id ON videos(uploader_id);")

def _extract_quality(info_dict: Dict[str, Any]) -> Tuple[str, str, Any, Any]:
    # (A) 実際にDLされた枝（requested_formats）から実質画質/音質を求める
    requested = info_dict.get("requested_formats", []) or []
    dl_v = next((f for f in requested if f.get("vcodec") != "none"), None)
    dl_a = next((f for f in requested if f.get("acodec") != "none"), None)

    actual_video_quality = f"{dl_v['height']}p" if dl_v and dl_v.get("height") else "不明"
    actual_audio_quality = f"{dl_a['abr']}kbps" if dl_a and dl_a.get("abr") else "不明"

    # (B) 全フォーマット一覧から最高値
    formats = info_dict.get("formats", []) or []
    videos  = [f for f in formats if f.get("vcodec") != "none" and f.get("height")]
    audios  = [f for f in formats if f.get("acodec") != "none" and f.get("abr")]

    highest_video_quality = f"{max(videos, key=lambda f: f.get('height', 0)).get('height')}p" if videos else "不明"
    highest_audio_quality = f"{max(audios, key=lambda f: f.get('abr', 0)).get('abr')}kbps" if audios else "不明"

    return highest_video_quality, highest_audio_quality, dl_v, dl_a

def upsert_info_sqlite(
    info_dict: Dict[str, Any],
    db_path: str = DEFAULT_DB_PATH
) -> Tuple[str, int]:
    """
    info_dict を SQLite に UPSERT する。
    Returns: (video_id, rowcount_changed)
    """
    if not info_dict:
        raise ValueError("info_dict is empty")

    # description を行配列で整形（base.json準拠）
    description_text = info_dict.get("description", "不明")
    description_list = description_text.splitlines() if description_text != "不明" else ["不明"]

    # 品質/寸法の算出は既存の JSON 生成ロジックと同等
    highest_v, highest_a, dl_v, dl_a = _extract_quality(info_dict)

    data = {
        # user_data（base.jsonに合わせる）
        "user_edited_title": info_dict.get("title", "不明"),
        "user_download_date_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user_notes": "",
        "user_tags_json": json.dumps([], ensure_ascii=False),

        # raw_data
        "title": info_dict.get("title", "不明"),
        "target_url": info_dict.get("webpage_url", "不明"),
        "thumbnail_url": info_dict.get("thumbnail", "不明"),
        "uploader": info_dict.get("uploader", "不明"),
        "uploader_id": info_dict.get("uploader_id", "不明"),
        "uploader_url": info_dict.get("uploader_url", "不明"),
        "channel": info_dict.get("channel", "不明"),
        "channel_id": info_dict.get("channel_id", "不明"),
        "channel_url": info_dict.get("channel_url", "不明"),
        "duration": str(timedelta(seconds=info_dict.get("duration", 0))),
        "serial_duration": info_dict.get("duration", 0),
        "upload_date": info_dict.get("upload_date", "不明"),
        "release_date": info_dict.get("release_date", "不明"),
        "video_id": info_dict.get("id", "不明"),
        "site_name": info_dict.get("extractor", "不明"),

        "highest_video_quality": highest_v,
        "highest_audio_quality": highest_a,
        "actual_video_quality": f"{dl_v.get('height')}p" if dl_v and dl_v.get("height") else "不明",
        "actual_audio_quality": f"{dl_a.get('abr')}kbps" if dl_a and dl_a.get("abr") else "不明",

        "video_width": (dl_v.get("width") if dl_v else None) or 0,
        "video_height": (dl_v.get("height") if dl_v else None) or 0,
        "age_limit": info_dict.get("age_limit", 0),
        "view_count": info_dict.get("view_count", 0),
        "like_count": info_dict.get("like_count", 0),
        "dislike_count": info_dict.get("dislike_count", 0),

        "categories_json": json.dumps(info_dict.get("categories", []) or [], ensure_ascii=False),
        "video_tags_json": json.dumps(info_dict.get("tags", []) or [], ensure_ascii=False),
        "description_json": json.dumps(description_list, ensure_ascii=False),
    }

    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    try:
        # 速度/堅牢性チューニング（必要に応じて）
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA synchronous=NORMAL;")
        _ensure_schema(conn)

        placeholders = ", ".join([f":{k}" for k in data.keys()])
        columns     = ", ".join(data.keys())
        updates     = ", ".join([f"{k}=excluded.{k}" for k in data.keys() if k != "video_id"])

        sql = f"""
        INSERT INTO videos ({columns})
        VALUES ({placeholders})
        ON CONFLICT(video_id) DO UPDATE SET
            {updates},
            updated_at=strftime('%Y-%m-%d %H:%M:%S','now');
        """

        cur = conn.execute(sql, data)
        conn.commit()
        return data["video_id"], cur.rowcount
    finally:
        conn.close()
