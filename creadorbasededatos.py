import sqlite3

conn = sqlite3.connect('registros.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS Alumnos (
                nombre TEXT,
                telefono TEXT,
                cuenta TEXT,
                qr_code TEXT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS NumerosTelefonos (
                numero TEXT)''')