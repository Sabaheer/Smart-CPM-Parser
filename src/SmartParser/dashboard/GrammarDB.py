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
        RuleNumber INTEGER NOT NULL,
        FieldName TEXT NOT NULL,
        Necessity TEXT NOT NULL,
        PrecedeCharacter TEXT NOT NULL,
        Format TEXT NOT NULL,
        LinkTo TEXT NOT NULL,
        PRIMARY KEY (Section, RuleNumber))''')
        conn.commit()
        conn.close()

    def insert_data(self, section, rule_number, field_name, necessity, precede_character, format1, LinkTo):
        conn = self.create_connection()
        cursor = conn.cursor()


        cursor.execute('SELECT * FROM GrammarDB WHERE Section = ?', (section,))
        sec = cursor.fetchall()
        next_row = len(sec)+1
        insert_num = rule_number
        print(sec,"sec")
        print(next_row,"next_row")

        
        # # print(section, rule_number, field_name, necessity, precede_characer, format1, LinkTo)
        if  rule_number in range(1,next_row):
            for row in range(rule_number, next_row):
                cursor.execute('UPDATE GrammarDB SET RuleNumber = ? WHERE Section = ? AND RuleNumber = ?', (row+1, section, row))
        else:
            insert_num = next_row
        # If the row does not exist, simply insert it
        
        cursor.execute('''
            INSERT INTO GrammarDB (Section, RuleNumber, FieldName, Necessity, PrecedeCharacter, Format, LinkTo)
            VALUES (?,?, ?, ?, ?, ?, ?)
            ''', (section, insert_num, field_name, necessity, precede_character, format1, LinkTo))
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
        sections = ['HEADER', 'CARRIER', 'ULD', 'BLK']
        columns = ["Section", "RuleNumber","FieldName", "Necessity", "PrecedeCharacter", "Format", "LinkTo"]
        rules_list = [[],[],[],[]]
        for j in range(len(sections)):
            cursor.execute('SELECT * FROM GrammarDB WHERE Section = ? ORDER BY RuleNumber ASC', (sections[j],))
            rows = cursor.fetchall()
            print(len(rows), 'number of rows in section', j)
            for row in rows:
                rule_dict = {columns[i]: row[i] for i in range(len(columns))}
                rules_list[j].append(rule_dict) 
        conn.close()
            
        return rules_list

    
    def clear_table(self):
        conn = self.create_connection()
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM GrammarDB
        ''')
        conn.commit()
        conn.close()

    def delete_data(self, section, rule_number, field_name, necessity, precede_character, format1, LinkTo):
        conn = self.create_connection()
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM GrammarDB
            WHERE Section = ? AND RuleNumber = ? AND FieldName = ? AND Necessity = ? AND PrecedeCharacter = ? AND Format = ? AND LinkTo = ?
        ''', (section, rule_number,field_name, necessity, precede_character, format1, LinkTo))
        conn.commit()
        conn.close()


grammar_db = GrammarDB()
# grammar_db.create_table()

# grammar_db.clear_table()

# grammar_db.insert_data("HEADER", 1, "CPM","Mandatory"	,"None"	,"CPM","None")
# carrier_fields = [
#     (1, "AirlineDesignator","Mandatory", "None", "mm(a)", "None"),
#     (2, "FlightNumber","Mandatory", "None", "fff(f)(a)", "None"),
#     (3, "DepartureDate","Optional", "/", "ff", "None"),
#     (4, "RegistrationNumber","Mandatory", ".", "mm(m)(m)(m)(m)(m)(m)(m)(m)", "None"),
#     (5, "DepartureStation","Mandatory", ".", "aaa", "None"),
#     (6, "ULD_configuration","Optional", ".", "m{1,12}", "None")
# ]
#
# for field in carrier_fields:
#     rule_number,field_name, necessity, precede_character, format1, link_to = field
#     grammar_db.insert_data("CARRIER",rule_number, field_name, necessity, precede_character, format1, link_to)

# uld_fields = [
# (1, "ULDBayDesignation", "Mandatory", "-", "m(m)(m)", "LoadCategory"),
#     (2, "ULDTypeCode", "Optional", "/", "amm((fffff)mm(a))", "None"),
#     (3, "UnloadingStation", "Mandatory", "/", "aam", "None"),
#     (4, "Weight", "Optional", "/", "f(f)(f)(f)(f)", "None"),
#     (5, "LoadCategory", "Mandatory", "/", "a(a)(f)", "Weight, LoadCategory"),
#     (6, "VolumeCode", "Optional", "/", "f", "None"),
#     (7, "ContourCode", "Optional", ".", "aaa/mm", "None"),
#     (8, "IMP", "Optional", ".", "aaa(/f(f)(f))", "IMP"),
#
# ]
# for field in uld_fields:
#     rule_number,field_name, necessity, precede_character, format1, link_to = field
#     grammar_db.insert_data("ULDs", rule_number, field_name, necessity, precede_character, format1, link_to)

# blk_fields = [
#     (1, "Compartment", "Mandatory", "-", "f(f)", "LoadCategory"),
#     (2, "Destination", "Mandatory", "/", "aam", "None"),
#     (3, "Weight", "Optional", "/", "f(f)(f)(f)", "None"),
#     (4, "LoadCategory", "Mandatory", "/", "a(a)(f)", "Weight, LoadCategory"),
#     (5, "IMP", "Optional", ".", "aaa(/f(f)(f))", "IMP"),
#     (6, "NumPieces", "Optional", ".", "PCSn(n)(n)(n)", "None"),
#     (7, "AVI", "Optional", ".", "VRf", "None")
# ]
# for field in blk_fields:
#     rule_number,field_name, necessity, precede_character, format1, link_to = field
#     grammar_db.insert_data("BLK", rule_number, field_name, necessity, precede_character, format1, link_to)

print(grammar_db.get_all_rules(), "In grammar DB")

