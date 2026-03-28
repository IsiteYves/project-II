import sqlite3
from datetime import datetime
from utils import get_valid_input, validate_name, validate_district, validate_skills, validate_experience, validate_languages
from database import get_user_by_email, update_user_profile

def explore_opportunities():
    print("\n=== Explore Opportunities ===")

    try:
        district = input("Enter your district (or press Enter for all): ")
    except KeyboardInterrupt:
        print("\nSearch cancelled. Returning to main menu.")
        return
    except EOFError:
        print("\nNo input detected. Showing all opportunities.")
        district = ""

    try:
        conn = sqlite3.connect("kura.db")
        cursor = conn.cursor()

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
    print("\n=== Mental Health & Wellbeing Resources ===")

    try:
        district = input("Enter your district (or press Enter for all): ")
    except KeyboardInterrupt:
        print("\nSearch cancelled. Returning to main menu.")
        return
    except EOFError:
        print("\nNo input detected. Showing all resources.")
        district = ""

    try:
        conn = sqlite3.connect("kura.db")
        cursor = conn.cursor()

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
