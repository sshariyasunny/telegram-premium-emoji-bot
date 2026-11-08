import sqlite3
import json
import os
from typing import Optional, Dict, Any, List

DB_PATH = os.path.join(os.path.dirname(__file__), "bot_data.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # User settings table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_settings (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        first_name TEXT,
        style TEXT DEFAULT 'smart',
        density TEXT DEFAULT 'medium',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Custom emoji packs added by users
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_custom_packs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        pack_name TEXT,
        pack_title TEXT,
        emojis_json TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(user_id, pack_name)
    )
    """)

    # User saved individual custom emojis
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_custom_emojis (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        emoji_char TEXT,
        custom_emoji_id TEXT,
        tag TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(user_id, emoji_char, custom_emoji_id)
    )
    """)
    
    # History / Stats
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS format_stats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        original_length INTEGER,
        style_used TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    conn.commit()
    conn.close()

def get_user_settings(user_id: int, username: str = "", first_name: str = "") -> Dict[str, Any]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT style, density FROM user_settings WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    if row:
        settings = {"style": row[0], "density": row[1]}
    else:
        cursor.execute(
            "INSERT INTO user_settings (user_id, username, first_name, style, density) VALUES (?, ?, ?, 'smart', 'medium')",
            (user_id, username, first_name)
        )
        conn.commit()
        settings = {"style": "smart", "density": "medium"}
    conn.close()
    return settings

def update_user_style(user_id: int, style: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE user_settings SET style = ?, updated_at = CURRENT_TIMESTAMP WHERE user_id = ?", (style, user_id))
    conn.commit()
    conn.close()

def update_user_density(user_id: int, density: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE user_settings SET density = ?, updated_at = CURRENT_TIMESTAMP WHERE user_id = ?", (density, user_id))
    conn.commit()
    conn.close()

def add_custom_pack(user_id: int, pack_name: str, pack_title: str, emojis_data: List[Dict[str, str]]):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    emojis_json = json.dumps(emojis_data, ensure_ascii=False)
    cursor.execute("""
    INSERT INTO user_custom_packs (user_id, pack_name, pack_title, emojis_json)
    VALUES (?, ?, ?, ?)
    ON CONFLICT(user_id, pack_name) DO UPDATE SET
        pack_title = excluded.pack_title,
        emojis_json = excluded.emojis_json,
        created_at = CURRENT_TIMESTAMP
    """, (user_id, pack_name, pack_title, emojis_json))
    conn.commit()
    conn.close()

def get_user_custom_packs(user_id: int) -> List[Dict[str, Any]]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT pack_name, pack_title, emojis_json FROM user_custom_packs WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    result = []
    for row in rows:
        result.append({
            "pack_name": row[0],
            "pack_title": row[1],
            "emojis": json.loads(row[2])
        })
    return result

def add_custom_emoji(user_id: int, emoji_char: str, custom_emoji_id: str, tag: str = ""):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    INSERT OR REPLACE INTO user_custom_emojis (user_id, emoji_char, custom_emoji_id, tag)
    VALUES (?, ?, ?, ?)
    """, (user_id, emoji_char, custom_emoji_id, tag))
    conn.commit()
    conn.close()

def log_format_stat(user_id: int, original_length: int, style_used: str):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO format_stats (user_id, original_length, style_used) VALUES (?, ?, ?)",
                       (user_id, original_length, style_used))
        conn.commit()
        conn.close()
    except Exception:
        pass

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully!")

