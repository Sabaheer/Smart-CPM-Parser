import sqlite3


class EtihadDb:
    def __init__(self, database_name="db.db"):
        self.database_name = database_name
        pass

    def create_db(self):
        con = self.create_connection()
        con.execute("DROP TABLE IF EXISTS files")
        con.execute("DROP TABLE IF EXISTS errors")
        con.execute("CREATE TABLE files(source VARCHAR(200), filename VARCHAR(200), content TEXT) ")
        con.execute(
            "CREATE TABLE errors(source VARCHAR(200), filename VARCHAR(200), line VARCHAR(300), field VARCHAR(300), value VARCHAR(300), error_type VARCHAR(20), column1 INTEGER PRIMARY KEY AUTOINCREMENT) ")
        # con.execute("CREATE TABLE thenrule(ruleid int, rule_group)")
        con.commit()

    def add_error(self, source, filename, line, field, value, error_type):
        con = self.create_connection()
        print("adding error")
        sql = '''INSERT INTO errors(source, filename, line, field, value, error_type)
                               VALUES(?,?,?,?,?,?)'''

        con.execute(sql, (source, filename, line, field, value, error_type))
        con.commit()

    def get_all_sources(self):
        con = self.create_connection()

        cur = con.cursor()
        cur.execute(f"SELECT DISTINCT source FROM files")
        rows = cur.fetchall()
        return rows

    def delete_errors(self, source, filename):
        con = self.create_connection()
        cur = con.cursor()
        cur.execute(f"DELETE FROM errors WHERE source='{source}' AND filename='{filename}'")
        con.commit()

    def get_errors_by_source(self, source):
        con = self.create_connection()

        cur = con.cursor()
        cur.execute(f"SELECT * FROM errors WHERE source={source}")
        rows = cur.fetchall()
        return rows

    def get_errors(self):
        con = self.create_connection()

        cur = con.cursor()
        cur.execute(f"SELECT * FROM errors ORDER by column1 DESC")
        rows = cur.fetchall()
        return rows

    def add_file(self, source, filename, content):
        if self.get_file_content(source, filename):
            self.update(source, filename, content)
        else:
            con = self.create_connection()
            sql = ''' INSERT INTO files(source, filename, content)
                       VALUES(?,?,?) '''

            con.execute(sql, (source, filename, content))
            con.commit()

    def update(self, source, filename, content):
        con = self.create_connection()
        sql = '''UPDATE files SET content=? WHERE source=? AND filename=? '''

        con.execute(sql, (content, source, filename))
        con.commit()

    def get_file_list(self):
        con = self.create_connection()

        cur = con.cursor()
        cur.execute("SELECT * FROM files")
        rows = cur.fetchall()
        return rows

    def get_file_content(self, source, filename):
        con = self.create_connection()

        cur = con.cursor()
        cur.execute(
            f"SELECT * FROM files WHERE filename='{filename}' AND source='{source}' LIMIT 1")  # TODO: SQL injection!!!
        rows = cur.fetchall()
        if len(rows) == 1:
            return rows[0][2]
        return None

    def create_connection(self):
        conn = None
        try:
            conn = sqlite3.connect(self.database_name)
        except BaseException as error:
            print(error)

        return conn
