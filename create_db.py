import sqlite3

def create_connection():
    # This will create the database file 'inventory_store.db' in the same folder as this script
    conn = sqlite3.connect('inventory_store.db')
    return conn

def create_tables(conn):
    cursor = conn.cursor()

    # Create product table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS product (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL
        )
    ''')

    # Create sales table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sale_date TEXT NOT NULL,
            name TEXT NOT NULL,
            sale_quantity INTEGER NOT NULL
        )
    ''')

    conn.commit()

def main():
    conn = create_connection()
    create_tables(conn)
    conn.close()
    print("Database and tables created successfully!")

if __name__ == "__main__":
    main()
