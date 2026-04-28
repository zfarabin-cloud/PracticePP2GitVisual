"""
db.py — PostgreSQL integration using psycopg2.

All public functions return sensible defaults if the database is
unavailable, so the game remains playable without a live DB.

Schema (run once):
    CREATE TABLE players (
        id       SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL
    );

    CREATE TABLE game_sessions (
        id            SERIAL PRIMARY KEY,
        player_id     INTEGER REFERENCES players(id),
        score         INTEGER   NOT NULL,
        level_reached INTEGER   NOT NULL,
        played_at     TIMESTAMP DEFAULT NOW()
    );
"""

import psycopg2
import psycopg2.extras
from config import DB_CONFIG

# ---------------------------------------------------------------------------
# Connection helper
# ---------------------------------------------------------------------------

def _connect():
    return psycopg2.connect(**DB_CONFIG)


def ensure_schema():
    """Create tables if they don't exist yet."""
    ddl = """
    CREATE TABLE IF NOT EXISTS players (
        id       SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL
    );
    CREATE TABLE IF NOT EXISTS game_sessions (
        id            SERIAL PRIMARY KEY,
        player_id     INTEGER REFERENCES players(id),
        score         INTEGER   NOT NULL,
        level_reached INTEGER   NOT NULL,
        played_at     TIMESTAMP DEFAULT NOW()
    );
    """
    try:
        with _connect() as conn:
            with conn.cursor() as cur:
                cur.execute(ddl)
    except Exception as e:
        print(f"[DB] Schema init skipped: {e}")


# ---------------------------------------------------------------------------
# Player helpers
# ---------------------------------------------------------------------------

def get_or_create_player(username: str) -> int | None:
    """Return player id, creating a row if needed."""
    sql_sel = "SELECT id FROM players WHERE username = %s"
    sql_ins = "INSERT INTO players (username) VALUES (%s) RETURNING id"
    try:
        with _connect() as conn:
            with conn.cursor() as cur:
                cur.execute(sql_sel, (username,))
                row = cur.fetchone()
                if row:
                    return row[0]
                cur.execute(sql_ins, (username,))
                return cur.fetchone()[0]
    except Exception as e:
        print(f"[DB] get_or_create_player: {e}")
        return None


# ---------------------------------------------------------------------------
# Session helpers
# ---------------------------------------------------------------------------

def save_session(player_id: int, score: int, level: int) -> bool:
    """Insert a game session row."""
    sql = """
        INSERT INTO game_sessions (player_id, score, level_reached)
        VALUES (%s, %s, %s)
    """
    try:
        with _connect() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (player_id, score, level))
        return True
    except Exception as e:
        print(f"[DB] save_session: {e}")
        return False


def get_personal_best(player_id: int) -> int:
    """Return the player's all-time highest score (0 if none)."""
    sql = """
        SELECT COALESCE(MAX(score), 0)
        FROM game_sessions
        WHERE player_id = %s
    """
    try:
        with _connect() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (player_id,))
                return cur.fetchone()[0]
    except Exception as e:
        print(f"[DB] get_personal_best: {e}")
        return 0


def get_leaderboard(limit: int = 10) -> list[dict]:
    """
    Return top `limit` sessions as a list of dicts:
        rank, username, score, level_reached, played_at
    """
    sql = """
        SELECT
            ROW_NUMBER() OVER (ORDER BY gs.score DESC) AS rank,
            p.username,
            gs.score,
            gs.level_reached,
            gs.played_at
        FROM game_sessions gs
        JOIN players p ON p.id = gs.player_id
        ORDER BY gs.score DESC
        LIMIT %s
    """
    try:
        with _connect() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute(sql, (limit,))
                return [dict(r) for r in cur.fetchall()]
    except Exception as e:
        print(f"[DB] get_leaderboard: {e}")
        return []
