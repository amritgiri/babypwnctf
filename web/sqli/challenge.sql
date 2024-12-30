CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS secrets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            secret_flag TEXT NOT NULL
        );
        INSERT OR IGNORE INTO users (username, password) VALUES ('admin', '9lM7O6GvHGD8pYansHvFyQnlGTuLtI'), ('user', 'user123');
        INSERT OR IGNORE INTO secrets (id, secret_flag) VALUES (1, 'i-CES{4dmIn_4cC3s5_9r4n73D}');