import sqlite3

class GrammarDB:
    def __init__(self, database_name="grammar.db"):
        self.database_name = database_name

    def create_table(self):
        conn = self.create_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS GrammarDB (
                Section TEXT NOT NULL,
                FieldName TEXT NOT NULL,
                Necessity TEXT NOT NULL,
                PreceedCharacter TEXT NOT NULL,
                Format TEXT NOT NULL,
                Terminated BOOLEAN NOT NULL,
                Repeated BOOLEAN NOT NULL,
                DependsUpon TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def insert_data(self, section, field_name, necessity, preceed_character, format, terminated, repeated, depends_upon):
        conn = self.create_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO GrammarDB (Section, FieldName, Necessity, PreceedCharacter, Format, Terminated, Repeated, DependsUpon)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (section, field_name, necessity, preceed_character, format, terminated, repeated, depends_upon))
        conn.commit()
        conn.close()

    def create_connection(self):
        conn = None
        try:
            conn = sqlite3.connect(self.database_name)
            return conn
        except sqlite3.Error as e:
            print(e)
            return None
        
    def show_rules(self):
        conn = self.create_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM GrammarDB
        ''')
        rows = cursor.fetchall()
        conn.close()
        return rows
    
    def clear_table(self):
        conn = self.create_connection()
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM GrammarDB
        ''')
        conn.commit()
        conn.close()

if __name__ == "__main__":
    db = GrammarDB()
    db.create_table()
    # db.clear_table()

    # Adding the provided data
    db.insert_data("Header", "Header", "M", "", "CPM", 1, 0, "None")
    db.insert_data("Carrier", "Carrier", "M", "", "mm(a)", 0, 0, "None")
    db.insert_data("Carrier", "Flight Number", "M", "", "fff(f)(a)", 0, 0, "Airline Designator")
    db.insert_data("Carrier", "Departure Date", "O", "/", "ff", 0, 0, "Flight Number")
    db.insert_data("Carrier", "Registration Number", "M", ".", "mm(m)(m)(m)(m)(m)(m)(m)(m)", 1, 0, "Departure Date, Flight Number")
    db.insert_data("ULDs", "ULD Bay Designation", "M", "-", "m(m)(m)", 0, 0, "Load Category, Volume Code")
    db.insert_data("ULDs", "ULD Type Code", "O", "/", "amm((fffff)mm(a))", 0, 0, "ULD Bay Designation")

    # get all the rules and print them
    rules = db.show_rules()
    for rule in rules:
        print(rule)
