# VULNERABLE_TEST_FIXTURE_DO_NOT_USE
# Intentionally insecure. Exists ONLY to exercise IPDefender SAST detection.

import sqlite3


def lookup_user(conn, username):
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    cursor = conn.execute(query)
    return cursor.fetchall()


def delete_records(conn, table, where):
    query = "DELETE FROM " + table + " WHERE " + where
    conn.execute(query)
    conn.commit()


if __name__ == "__main__":
    conn = sqlite3.connect(":memory:")
    conn.execute(
        "CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, email TEXT)"
    )
    conn.execute("INSERT INTO users VALUES (1, 'alice', 'alice@example.com')")
    conn.execute("INSERT INTO users VALUES (2, 'bob', 'bob@example.com')")
    conn.commit()

    rows = lookup_user(conn, "alice")
    print("Found:", rows)

    delete_records(conn, "users", "username = 'bob'")
    print("Deleted bob")

    conn.close()
