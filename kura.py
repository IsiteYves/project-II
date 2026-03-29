# KURA - Youth Growth & Opportunity Bridge
import sqlite3
import os
from datetime import datetime


def init_db():
    # Create the local SQLite database and required tables.
    conn = sqlite3.connect("kura.db")
    cursor = conn.cursor()

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
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
    # Insert starter records only when tables are empty.
    conn = sqlite3.connect("kura.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM opportunities")
    if cursor.fetchone()[0] == 0:
        opportunities = [
            (
                "Tour Guide at Volcanoes National Park",
                "Tourism",
                "Musanze",
                "Lead tourists through gorilla habitats",
                "+250788123456",
                "2025-03-01",
            ),
            (
                "Farm Assistant - Modern Greenhouse",
                "Agriculture",
                "Kigali",
                "Help with hydroponic farming",
                "+250787654321",
                "2025-03-02",
            ),
            (
                "Hotel Receptionist - Kigali Marriott",
                "Tourism",
                "Kigali",
                "Guest services and check-in",
                "+250786543210",
                "2025-03-03",
            ),
            (
                "Coffee Harvesting Specialist",
                "Agriculture",
                "Rubavu",
                "Modern coffee processing techniques",
                "+250785432109",
                "2025-03-04",
            ),
            (
                "Wildlife Photography Assistant",
                "Tourism",
                "Akagera",
                "Document wildlife for conservation",
                "+250784321098",
                "2025-03-05",
            ),
        ]

        cursor.executemany(
            """
        INSERT INTO opportunities (title, type, district, description, contact, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
            opportunities,
        )

    cursor.execute("SELECT COUNT(*) FROM mental_health")
    if cursor.fetchone()[0] == 0:
        mental_health = [
            (
                "Rwanda Mental Health Support Center",
                "Kigali",
                "Support Group",
                "+250788112233",
                "Mon-Fri 8AM-5PM",
                "2025-03-01",
            ),
            (
                "Youth Wellness Hub",
                "Musanze",
                "Counseling",
                "+250787223344",
                "Daily 9AM-6PM",
                "2025-03-02",
            ),
            (
                "Community One-Stop Center",
                "Rubavu",
                "Clinic",
                "+250786334455",
                "Mon-Sat 8AM-4PM",
                "2025-03-03",
            ),
            (
                "Teen Support Network",
                "Kigali",
                "Support Group",
                "+250785445566",
                "Tue-Thu 3PM-7PM",
                "2025-03-04",
            ),
            (
                "Rural Mental Health Initiative",
                "Huye",
                "Clinic",
                "+250784556677",
                "Mon-Fri 9AM-5PM",
                "2025-03-05",
            ),
        ]

        cursor.executemany(
            """
        INSERT INTO mental_health (name, district, type, contact, hours, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
            mental_health,
        )

    conn.commit()
    conn.close()


def main_menu():
    # Display the home menu and return the selected option.
    print("\n=== KURA - Youth Growth & Opportunity Bridge ===")
    print("1. Register Portfolio")
    print("2. Explore Opportunities")
    print("3. Mental health and wellbeing resources")
    print("4. Admin(MOYA/RDB): Log district outreach")
    print("5. Exit")
    return input("Enter your choice (1-5): ")


def register_portfolio():
    # Collect and store a youth profile for opportunities matching.
    print("\n=== Register Your Portfolio ===")

    name = input("Full Name: ")
    district = input("District: ")
    skills = input("Skills (comma separated): ")
    experience = input("Experience: ")
    languages = input("Languages (comma separated): ")

    try:
        conn = sqlite3.connect("kura.db")
        cursor = conn.cursor()

        cursor.execute(
            """
        INSERT INTO users (name, district, skills, experience, languages)
        VALUES (?, ?, ?, ?, ?)
        """,
            (name, district, skills, experience, languages),
        )

        user_id = cursor.lastrowid
        conn.commit()
        conn.close()

        print(f"\n✓ Portfolio registered successfully! Your ID: {user_id}")
        print("\n--- Portfolio Summary ---")
        print(f"Name: {name}")
        print(f"District: {district}")
        print(f"Skills: {skills}")
        print(f"Experience: {experience}")
        print(f"Languages: {languages}")

        # Optionally export a simple text resume after registration.
        export = input("\nExport as .txt file? (y/n): ").lower()
        if export == "y":
            export_resume(user_id, name, district, skills, experience, languages)

    except Exception as e:
        print(f"Error: {e}")


def export_resume(user_id, name, district, skills, experience, languages):
    # Build a readable .txt resume from captured profile details.
    filename = f"resume_{name.replace(' ', '_')}_{user_id}.txt"

    try:
        with open(filename, "w") as f:
            f.write(f"RESUME - {name}\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"ID: {user_id}\n")
            f.write(f"Name: {name}\n")
            f.write(f"District: {district}\n")
            f.write(f"Skills: {skills}\n")
            f.write(f"Experience: {experience}\n")
            f.write(f"Languages: {languages}\n")
            f.write(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"\nGenerated by KURA - Youth Growth & Opportunity Bridge\n")

        print(f"✓ Resume exported as {filename}")
    except Exception as e:
        print(f"Error exporting resume: {e}")


def explore_opportunities():
    # Show opportunities, filtered by district when provided.
    print("\n=== Explore Opportunities ===")
    district = input("Enter your district (or press Enter for all): ")

    try:
        conn = sqlite3.connect("kura.db")
        cursor = conn.cursor()

        # Run a district-specific query or return all records.
        if district:
            cursor.execute(
                """
            SELECT title, type, description, contact FROM opportunities 
            WHERE district LIKE ? ORDER BY created_at DESC
            """,
                (f"%{district}%",),
            )
        else:
            cursor.execute(
                """
            SELECT title, type, description, contact FROM opportunities 
            ORDER BY created_at DESC
            """
            )

        opportunities = cursor.fetchall()
        conn.close()

        if opportunities:
            print(f"\n--- Found {len(opportunities)} opportunities ---")
            for i, (title, type, description, contact) in enumerate(opportunities, 1):
                print(f"\n{i}. {title}")
                print(f"   Type: {type}")
                print(f"   Description: {description}")
                print(f"   Contact: {contact}")
        else:
            print("No opportunities found in your district.")

    except Exception as e:
        print(f"Error: {e}")


def mental_health_resources():
    # Show wellbeing services, filtered by district when provided.
    print("\n=== Mental Health & Wellbeing Resources ===")
    district = input("Enter your district (or press Enter for all): ")

    try:
        conn = sqlite3.connect("kura.db")
        cursor = conn.cursor()

        # Run a district-specific query or return all records.
        if district:
            cursor.execute(
                """
            SELECT name, type, contact, hours FROM mental_health 
            WHERE district LIKE ? ORDER BY name
            """,
                (f"%{district}%",),
            )
        else:
            cursor.execute(
                """
            SELECT name, type, contact, hours FROM mental_health 
            ORDER BY name
            """
            )

        resources = cursor.fetchall()
        conn.close()

        if resources:
            print(f"\n--- Found {len(resources)} resources ---")
            for i, (name, type, contact, hours) in enumerate(resources, 1):
                print(f"\n{i}. {name}")
                print(f"   Type: {type}")
                print(f"   Contact: {contact}")
                print(f"   Hours: {hours}")
        else:
            print("No mental health resources found in your district.")

    except Exception as e:
        print(f"Error: {e}")


def admin_log():
    # Capture district outreach details from authorized officials.
    print("\n=== Admin: Log District Outreach ===")

    # Keep this admin flow protected with a basic password check.
    password = input("Enter admin password: ")
    if password != "admin123":
        print("Invalid password!")
        return

    print("\n--- Log District Visit ---")
    district = input("District visited: ")
    visit_date = input("Visit date (YYYY-MM-DD): ")
    officials = input("Officials present (comma separated): ")
    activities = input("Activities conducted: ")

    try:
        conn = sqlite3.connect("kura.db")
        cursor = conn.cursor()

        cursor.execute(
            """
        INSERT INTO admin_logs (district, visit_date, officials, activities)
        VALUES (?, ?, ?, ?)
        """,
            (district, visit_date, officials, activities),
        )

        conn.commit()
        conn.close()

        print("✓ District outreach logged successfully!")

    except Exception as e:
        print(f"Error: {e}")


def main():
    # Initialize storage and preload starter data before the menu loop.
    init_db()
    seed_data()

    # Keep the app running until the user chooses to exit.
    while True:
        choice = main_menu()

        if choice == "1":
            register_portfolio()
        elif choice == "2":
            explore_opportunities()
        elif choice == "3":
            mental_health_resources()
        elif choice == "4":
            admin_log()
        elif choice == "5":
            print("\nThank you for using KURA!")
            break
        else:
            print("Invalid choice! Please enter 1-5.")

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
