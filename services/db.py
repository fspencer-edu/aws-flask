import psycopg2
from config import Config

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS journal_entries (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            image_url TEXT,
            created_at TIMESTAMP NOT NULL
        );
        """
    )

    conn.commit()
    cur.close()
    conn.close()

def get_db_connection():
    return psycopg2.connect(
        host=Config.DB_HOST,
        dbname=Config.DB_NAME,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        port=Config.DB_PORT,
    )


def get_all_entries():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT id, title, content, image_url, created_at
        FROM journal_entries
        ORDER BY created_at DESC
        """
    )

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows


def insert_entry(title, content, image_url, created_at):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO journal_entries (title, content, image_url, created_at)
        VALUES (%s, %s, %s, %s)
        """,
        (title, content, image_url, created_at),
    )

    conn.commit()
    cur.close()
    conn.close()