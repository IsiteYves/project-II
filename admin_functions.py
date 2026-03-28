import sqlite3
from datetime import datetime
from utils import get_valid_input, validate_district, validate_date, validate_officials, validate_activities
from database import add_opportunity, add_mental_health_resource, get_all_users, get_all_admin_logs

def admin_log():
    print("\n=== Admin: Log District Outreach ===")

    try:
        if input("Enter admin password: ") != "admin123":
            print("Invalid password!")
            return
    except KeyboardInterrupt:
        print("\nLogin cancelled. Returning to main menu.")
        return
    except EOFError:
        print("\nNo input detected. Login cancelled.")
        return

    print("\n--- Log District Visit ---")
    district = get_valid_input("District visited: ", validate_district, "")
    if not district:
        return
    
    visit_date = get_valid_input("Visit date (YYYY-MM-DD) [Leave blank for today]: ", validate_date, "")
    if visit_date is None:
        return
    if not visit_date:
        visit_date = datetime.now().strftime('%Y-%m-%d')
    
    officials = get_valid_input("Officials present (comma separated): ", validate_officials, "")
    if not officials:
        return
    
    activities = get_valid_input("Activities conducted: ", validate_activities, "")
    if not activities:
        return

    try:
        with sqlite3.connect("kura.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO admin_logs (district, visit_date, officials, activities)
                VALUES (?, ?, ?, ?)
                """,
                (district, visit_date, officials, activities),
            )
            conn.commit()
        print("✓ District outreach logged successfully!")
    except Exception as e:
        print(f"Error: {e}")

def admin_add_opportunity():
    print("\n=== Add New Opportunity ===")
    
    title = get_valid_input("Opportunity Title: ", lambda x: (len(x.strip()) >= 5, "Title must be at least 5 characters"), "")
    if not title:
        return
    
    print("Type (Tourism/Agriculture):")
    type_ = get_valid_input("Enter type: ", lambda x: (x.lower() in ['tourism', 'agriculture'], "Type must be 'Tourism' or 'Agriculture'"), "")
    if not type_:
        return
    type_ = type_.capitalize()
    
    district = get_valid_input("District: ", validate_district, "")
    if not district:
        return
    
    description = get_valid_input("Description: ", lambda x: (len(x.strip()) >= 10, "Description must be at least 10 characters"), "")
    if not description:
        return
    
    contact = get_valid_input("Contact: ", lambda x: (len(x.strip()) >= 5, "Contact must be at least 5 characters"), "")
    if not contact:
        return

    try:
        add_opportunity(title, type_, district, description, contact)
        print("✓ Opportunity added successfully!")
    except Exception as e:
        print(f"Error: {e}")

def admin_add_mental_health():
    print("\n=== Add Mental Health Resource ===")
    
    name = get_valid_input("Resource Name: ", lambda x: (len(x.strip()) >= 3, "Name must be at least 3 characters"), "")
    if not name:
        return
    
    district = get_valid_input("District: ", validate_district, "")
    if not district:
        return
    
    print("Type (Support Group/Counseling/Clinic):")
    type_ = get_valid_input("Enter type: ", lambda x: (x.lower() in ['support group', 'counseling', 'clinic'], "Type must be 'Support Group', 'Counseling', or 'Clinic'"), "")
    if not type_:
        return
    type_ = type_.title()
    
    contact = get_valid_input("Contact: ", lambda x: (len(x.strip()) >= 5, "Contact must be at least 5 characters"), "")
    if not contact:
        return
    
    hours = get_valid_input("Operating Hours: ", lambda x: (len(x.strip()) >= 3, "Hours must be at least 3 characters"), "")
    if not hours:
        return

    try:
        add_mental_health_resource(name, district, type_, contact, hours)
        print("✓ Mental health resource added successfully!")
    except Exception as e:
        print(f"Error: {e}")

def admin_view_users():
    print("\n=== Registered Users ===")
    
    try:
        users = get_all_users()
        if users:
            print(f"\n--- Total Registered Users: {len(users)} ---")
            for i, (user_id, name, district, skills, experience, languages, created_at) in enumerate(users, 1):
                print(f"\n{i}. ID: {user_id}")
                print(f"   Name: {name}")
                print(f"   District: {district}")
                print(f"   Skills: {skills}")
                print(f"   Registered: {created_at}")
        else:
            print("No users registered yet.")
    except Exception as e:
        print(f"Error: {e}")

def admin_view_logs():
    print("\n=== District Outreach Logs ===")
    
    try:
        logs = get_all_admin_logs()
        if logs:
            print(f"\n--- Total Outreach Logs: {len(logs)} ---")
            for i, (district, visit_date, officials, activities, created_at) in enumerate(logs, 1):
                print(f"\n{i}. District: {district}")
                print(f"   Visit Date: {visit_date}")
                print(f"   Officials: {officials}")
                print(f"   Activities: {activities}")
                print(f"   Logged: {created_at}")
        else:
            print("No outreach logs found.")
    except Exception as e:
        print(f"Error: {e}")

def admin_menu():
    while True:
        print("\n=== Admin Menu ===")
        print("1. Log District Outreach")
        print("2. Add New Opportunity")
        print("3. Add Mental Health Resource")
        print("4. View Registered Users")
        print("5. View Outreach Logs")
        print("6. Back to Main Menu")
        
        try:
            choice = input("Enter your choice (1-6): ")
            if choice == "1":
                admin_log()
            elif choice == "2":
                admin_add_opportunity()
            elif choice == "3":
                admin_add_mental_health()
            elif choice == "4":
                admin_view_users()
            elif choice == "5":
                admin_view_logs()
            elif choice == "6":
                break
            else:
                print("Invalid choice! Please enter 1-6.")
            
            if choice != "6":
                input("\nPress Enter to continue...")
        except KeyboardInterrupt:
            print("\nReturning to main menu...")
            break
        except EOFError:
            print("\nReturning to main menu...")
            break
