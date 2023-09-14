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
        PrecedeCharacter TEXT NOT NULL,
        Format TEXT NOT NULL,
        LinkTo TEXT NOT NULL)''')
        conn.commit()
        conn.close()

    def insert_data(self, section, field_name, necessity, precede_character, format, LinkTo):
        conn = self.create_connection()
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO GrammarDB (Section, FieldName, Necessity, PrecedeCharacter, Format, LinkTo)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (section, field_name, necessity, precede_character, format, LinkTo))

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
        columns = ["Section", "FieldName", "Necessity", "PrecedeCharacter", "Format", "LinkTo"]

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
# grammar_db.create_table()

# grammar_db.clear_table()

# Insert Header

# grammar_db.insert_data("Header", "CPM",	"M"	,"None"	,"None",	"None")


# Insert Carrier

# fields = [
#     ("AirlineDesignator", "M", "None", "mm(a)", "None"),
#     ("FlightNumber", "M", "None", "fff(f)(a)", "None"),
#     ("DepartureDate", "O", "/", "ff", "None"),
#     ("RegistrationNumber", "M", ".", "mm(m)(m)(m)(m)(m)(m)(m)(m)", "None"),
#     ("DepartureStation", "M", ".", "aaa", "None"),
#     ("ULD_configuration", "O", ".", "m{1,12}", "None")
# ]

# # Insert each field into the database
# for field in fields:
#     field_name, necessity, precede_character, format, link_to = field
#     grammar_db.insert_data("Carrier", field_name, necessity, precede_character, format, link_to)
# # This code will insert each field into the "Carriers" section of your SQLite database using the grammar_db.insert_data method. Adjust the fields list as needed to match your data.


# Insert ULD


# uld_fields = [
#     ("ULDBayDesignation", "M", "-", "m(m)(m)", "LoadCategory"),
#     ("ULDTypeCode", "O", "/", "amm((fffff)mm(a))", "None"),
#     ("UnloadingStation", "M", "/", "aam", "None"),
#     ("Weight", "O", "/", "f(f)(f)(f)(f)", "None"),
#     ("LoadCategory", "M", "/", "a(a)(f)", "Weight, LoadCategory"),
#     ("VolumeCode", "O", "/", "f", "None"),
#     ("ContourCode", "O", ".", "aaa/mm", "None"),
#     ("IMP", "O", ".", "aaa(/f(f)(f))", "IMP"),
#     ("AVI", "O", ".", "VRf", "None")
# ]

# # Insert each field into the database
# for field in uld_fields:
#     field_name, necessity, precede_character, format, link_to = field
#     grammar_db.insert_data("ULDs", field_name, necessity, precede_character, format, link_to)


# Insert BLK data

# Sample data structure for BLK section
# blk_fields = [
#     ("Compartment", "M", "-", "f(f)", "LoadCategory"),
#     ("Destination", "M", "/", "aam", "None"),
#     ("Weight", "O", "/", "f(f)(f)(f)", "None"),
#     ("LoadCategory", "M", "/", "a(a)(f)", "Weight, LoadCategory"),
#     ("IMP", "O", ".", "aaa(/f(f)(f))", "IMP"),
#     ("NumPeices", "O", ".", "PCSn(n)(n)(n)", "None"),
#     ("AVI", "O", ".", "VRf", "None")
# ]

# # Insert each field into the database
# for field in blk_fields:
#     field_name, necessity, precede_character, format, link_to = field
#     grammar_db.insert_data("BLK", field_name, necessity, precede_character, format, link_to)

# print(grammar_db.get_all_rules(), "In grammar DB")

