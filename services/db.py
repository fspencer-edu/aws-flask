import psycopg2
from config import Config


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