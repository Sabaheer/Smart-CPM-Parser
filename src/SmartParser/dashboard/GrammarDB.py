import sqlite3

class GrammarDB:
    def __init__(self, database_name="grammar.db"):
        self.database_name = database_name
        self.create_table()

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
        
    def get_all_rules(self):
        conn = self.create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM GrammarDB")
        rows = cursor.fetchall()
        conn.close()

        # Define the column names for the table
        columns = ["Section", "FieldName", "Necessity", "PreceedCharacter", "Format", "Terminated", "Repeated", "DependsUpon"]

        # Create a list of dictionaries where each dictionary represents a row
        rules_list = []
        for row in rows:
            rule_dict = {columns[i]: row[i] for i in range(len(columns))}
            rules_list.append(rule_dict)

        return rules_list

    
    def clear_table(self):
        conn = self.create_connection()
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM GrammarDB
        ''')
        conn.commit()
        conn.close()

grammar_db = GrammarDB()

# grammar_db.insert_data("Header", "Header", "M", "", "CPM", 1, 0, "None")
# grammar_db.insert_data("Carrier", "Carrier", "M", "", "mm(a)", 0, 0, "None")
# grammar_db.insert_data("Carrier", "Flight Number", "M", "", "fff(f)(a)", 0, 0, "Airline Designator")
# grammar_db.insert_data("Carrier", "Departure Date", "O", "/", "ff", 0, 0, "Flight Number")
# grammar_db.insert_data("Carrier", "Registration Number", "M", ".", "mm(m)(m)(m)(m)(m)(m)(m)(m)", 1, 0, "Departure Date, Flight Number")
# grammar_db.insert_data("ULDs", "ULD Bay Designation", "M", "-", "m(m)(m)", 0, 0, "Load Category, Volume Code")
# grammar_db.insert_data("ULDs", "ULD Type Code", "O", "/", "amm((fffff)mm(a))", 0, 0, "ULD Bay Designation")