from db import db

def create_tables():

    db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            phone_number TEXT UNIQUE NOT NULL
        )
    """)

    db.execute("""
        CREATE TABLE IF NOT EXISTS Tshirts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            sizes INTEGER,
            collabration_with TEXT,
            max_number INTEGER NOT NULL,
            image_path TEXT NOT NULL
        )
    """)

    db.execute("""
CREATE TABLE IF NOT EXISTS admins (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,  
    phone_number TEXT NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE)
""")
    

    db.execute("""CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    owner_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    tshirt_id INTEGER NOT NULL REFERENCES Tshirts(id) ON DELETE CASCADE,
    tshirt_size INTEGER NOT NULL,
    Tshirt_number INTEGER NOT NULL,
    order_date DATE NOT NULL DEFAULT CURRENT_DATE
)""")
    

    db.execute("""CREATE TABLE if not exists VerificationCodes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    phone_number TEXT NOT NULL,
    code TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP
)""")



    user_exists = db.execute("SELECT * FROM users WHERE phone_number = '09192232099'")
    if not user_exists:
        db.execute("insert into users (name,last_name,phone_number) VALUES ('')")
        db.execute("insert into admins (user_id,phone_number) VALUES ()")



