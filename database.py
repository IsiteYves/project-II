import sqlite3
from utils import RWANDA_DISTRICTS

def init_db():
    conn = sqlite3.connect("kura.db")
    cursor = conn.cursor()

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        name TEXT NOT NULL,
        district TEXT NOT NULL,
        skills TEXT NOT NULL,
        experience TEXT NOT NULL,
        languages TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS opportunities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        type TEXT NOT NULL,
        district TEXT NOT NULL,
        description TEXT NOT NULL,
        contact TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS mental_health (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        district TEXT NOT NULL,
        type TEXT NOT NULL,
        contact TEXT NOT NULL,
        hours TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS admin_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        district TEXT NOT NULL,
        visit_date TEXT NOT NULL,
        officials TEXT NOT NULL,
        activities TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    )

    conn.commit()
    conn.close()

def seed_data():
    datasets = {
        "opportunities": (
            "INSERT INTO opportunities (title, type, district, description, contact, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            [
                ("Tour Guide at Volcanoes National Park", "Tourism", "Musanze", "Lead tourists through gorilla habitats", "+250788123456", "2025-03-01"),
                ("Farm Assistant - Modern Greenhouse", "Agriculture", "Kigali", "Help with hydroponic farming", "+250787654321", "2025-03-02"),
                ("Hotel Receptionist - Kigali Marriott", "Tourism", "Kigali", "Guest services and check-in", "+250786543210", "2025-03-03"),
                ("Coffee Harvesting Specialist", "Agriculture", "Rubavu", "Modern coffee processing techniques", "+250785432109", "2025-03-04"),
                ("Wildlife Photography Assistant", "Tourism", "Akagera", "Document wildlife for conservation", "+250784321098", "2025-03-05"),
                ("Agricultural Extension Officer", "Agriculture", "Gatsibo", "Provide farming support to local communities", "+250783210987", "2025-03-06"),
                ("Eco-Tourism Guide", "Tourism", "Nyungwe", "Lead nature walks and bird watching tours", "+250782109876", "2025-03-07"),
                ("Horticulture Specialist", "Agriculture", "Ruhango", "Modern vegetable farming techniques", "+250781098765", "2025-03-08"),
            ]
        ),
        "mental_health": (
            "INSERT INTO mental_health (name, district, type, contact, hours, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            [
                ("Rwanda Mental Health Support Center", "Kigali", "Support Group", "+250788112233", "Mon-Fri 8AM-5PM", "2025-03-01"),
                ("Youth Wellness Hub", "Musanze", "Counseling", "+250787223344", "Daily 9AM-6PM", "2025-03-02"),
                ("Community One-Stop Center", "Rubavu", "Clinic", "+250786334455", "Mon-Sat 8AM-4PM", "2025-03-03"),
                ("Teen Support Network", "Kigali", "Support Group", "+250785445566", "Tue-Thu 3PM-7PM", "2025-03-04"),
                ("Rural Mental Health Initiative", "Huye", "Clinic", "+250784556677", "Mon-Fri 9AM-5PM", "2025-03-05"),
                ("Northern Province Counseling Center", "Burera", "Counseling", "+250783667788", "Mon-Fri 8AM-4PM", "2025-03-06"),
                ("Eastern Province Wellness Clinic", "Bugesera", "Clinic", "+250782778899", "Daily 8AM-6PM", "2025-03-07"),
                ("Western Province Support Group", "Karongi", "Support Group", "+250781889900", "Wed-Fri 2PM-6PM", "2025-03-08"),
            ]
        )
    }

    with sqlite3.connect("kura.db") as conn:
        cursor = conn.cursor()
        for table, (query, data) in datasets.items():
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            if cursor.fetchone()[0] == 0:
                cursor.executemany(query, data)
        conn.commit()

def add_opportunity(title, type_, district, description, contact):
    with sqlite3.connect("kura.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO opportunities (title, type, district, description, contact, created_at)
            VALUES (?, ?, ?, ?, ?, date('now'))
            """,
            (title, type_, district, description, contact)
        )
        conn.commit()

def add_mental_health_resource(name, district, type_, contact, hours):
    with sqlite3.connect("kura.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO mental_health (name, district, type, contact, hours, created_at)
            VALUES (?, ?, ?, ?, ?, date('now'))
            """,
            (name, district, type_, contact, hours)
        )
        conn.commit()

def get_all_users():
    with sqlite3.connect("kura.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, district, skills, experience, languages, created_at FROM users ORDER BY created_at DESC")
        return cursor.fetchall()

def authenticate_user(email, password):
    from utils import hash_password
    with sqlite3.connect("kura.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, district, skills, experience, languages FROM users WHERE email = ? AND password = ?", 
                      (email, hash_password(password)))
        return cursor.fetchone()

def get_user_by_email(email):
    with sqlite3.connect("kura.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, district, skills, experience, languages, created_at FROM users WHERE email = ?", (email,))
        return cursor.fetchone()

def update_user_profile(user_id, name, district, skills, experience, languages):
    with sqlite3.connect("kura.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE users 
            SET name = ?, district = ?, skills = ?, experience = ?, languages = ?
            WHERE id = ?
            """,
            (name, district, skills, experience, languages, user_id)
        )
        conn.commit()
        return cursor.rowcount > 0

def delete_user_portfolio(user_id):
    with sqlite3.connect("kura.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        return cursor.rowcount > 0

def get_all_admin_logs():
    with sqlite3.connect("kura.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT district, visit_date, officials, activities, created_at FROM admin_logs ORDER BY created_at DESC")
        return cursor.fetchall()
