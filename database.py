import sqlite3
import hashlib
import os
import hmac
import hashlib

DB_PATH = "lab.db"


def hash_password(password: str) -> str:
    salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt,
        600_000
    )
    return f"{salt.hex()}:{digest.hex()}"


def verify_password(password: str, stored: str) -> bool:
    salt_hex, digest_hex = stored.split(":")
    salt = bytes.fromhex(salt_hex)
    expected = bytes.fromhex(digest_hex)

    actual = hashlib.pbkdf2_hmac(
        "sha256", password.encode(), salt, 600_000
    )
    return hmac.compare_digest(actual, expected)


def init_db():
    conn = sqlite3.connect(DB_PATH)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)

    users = [
        ("alice", hash_password("alice123"), "user"),
        ("bob", hash_password("bob123"), "admin")
    ]

    conn.executemany("""
        INSERT OR IGNORE INTO users
        (username, password_hash, role)
        VALUES (?, ?, ?)
    """, users)

    conn.commit()

    # Retrieve and display all database records
    cursor = conn.execute("""
        SELECT id, username, password_hash, role
        FROM users
    """)

    print("\nDatabase records:")
    print("=" * 60)

    for user in cursor.fetchall():
        print(f"ID:            {user[0]}")
        print(f"Username:      {user[1]}")
        print(f"Password Hash: {user[2]}")
        print(f"Role:          {user[3]}")
        print("-" * 60)

    conn.close()


if __name__ == "__main__":
    init_db()
    print("Database initialized")
