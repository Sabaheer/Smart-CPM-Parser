import sqlite3

class AirportCodes:
    def __init__(self, database_name="airport.db"):
        self.database_name = database_name
        self.create_database()

    def create_database(self):
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()

        # Create the AirportCodes table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS AirportCodes (
                IATA_Code TEXT PRIMARY KEY
            )
        ''')

        conn.commit()
        conn.close()

    # def insert_code(self, iata_code):
    #     conn = sqlite3.connect(self.database_name)
    #     cursor = conn.cursor()

    #     # Insert the IATA code into the AirportCodes table
    #     cursor.execute('''
    #         INSERT INTO AirportCodes (IATA_Code)
    #         VALUES (?)
    #     ''', (iata_code,))

    #     conn.commit()
    #     conn.close()

    def insert_code(self, iata_code):
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()

        # Check if the IATA code already exists in the database
        cursor.execute('SELECT IATA_Code FROM AirportCodes WHERE IATA_Code = ?', (iata_code,))
        existing_code = cursor.fetchone()

        if existing_code is None:
            # Insert the IATA code into the AirportCodes table if it doesn't exist
            cursor.execute('''
                INSERT OR IGNORE INTO AirportCodes (IATA_Code)
                VALUES (?)
            ''', (iata_code,))
            conn.commit()
            conn.close()
            return "Code inserted successfully."
        else:
            conn.close()
            return "Code already exists."



    def create_connection(self):
        conn = None
        try:
            conn = sqlite3.connect(self.database_name)
            return conn
        except sqlite3.Error as e:
            print(e)
            return None

    def get_all_codes(self):
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM AirportCodes')
        rows = cursor.fetchall()

        codes = [row[0] for row in rows]

        conn.close()

        return codes
    
    def clear_table(self):
        conn = self.create_connection()
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM AirportCodes
        ''')
        conn.commit()
        conn.close()


    # Create an instance of the AirportCodes class
airport_db = AirportCodes()

    # Create the database and table if they don't exist


    # Insert at least 30 sample airport codes
