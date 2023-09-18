import sqlite3

class AuthDB:
    def __init__(self, db_name='users.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_users_table()

    def create_users_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def close(self):
        self.conn.close()

    def insert_user(self, username, password):
        try:
            self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def find_user(self, username):
        self.cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        return self.cursor.fetchone()

    def verify_user(self, username, password):
        user = self.find_user(username)
        if user and user[2] == password:
            return True
        return False
    def get_all_users(self):
        self.cursor.execute("SELECT * FROM users")
        return self.cursor.fetchall()
    def clear_database(self):
        try:
            self.cursor.execute("DELETE FROM users")
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error clearing database: {e}")
            return False
authDB = AuthDB()




