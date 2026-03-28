from utils import get_valid_input, validate_email, validate_password, validate_name, validate_district, validate_skills, validate_experience, validate_languages, hash_password
from database import authenticate_user, get_user_by_email, update_user_profile
import sqlite3

current_user = None

def login():
    global current_user
    print("\n=== Login ===")
    
    try:
        email = get_valid_input("Email: ", validate_email, "")
        if not email:
            return False
        
        password = input("Password: ")
        if not password:
            print("Password is required.")
            return False
        
        user = authenticate_user(email, password)
        if user:
            current_user = user
            user_id, name, district, skills, experience, languages = user
            print(f"\n✓ Welcome back, {name}!")
            return True
        else:
            print("Invalid email or password.")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def register():
    print("\n=== Register New Account ===")
    
    email = get_valid_input("Email: ", validate_email, "")
    if not email:
        return False
    
    password = get_valid_input("Password (min 6 chars): ", validate_password, "")
    if not password:
        return False
    
    name = get_valid_input("Full Name: ", validate_name, "")
    if not name:
        return False
    
    district = get_valid_input("District: ", validate_district, "")
    if not district:
        return False
    
    skills = get_valid_input("Skills (comma separated): ", validate_skills, "")
    if not skills:
        return False
    
    experience = get_valid_input("Experience: ", validate_experience, "")
    if not experience:
        return False
    
    languages = get_valid_input("Languages (comma separated): ", validate_languages, "")
    if not languages:
        return False
    
    try:
        conn = sqlite3.connect("kura.db")
        cursor = conn.cursor()
        
        cursor.execute(
            """
        INSERT INTO users (email, password, name, district, skills, experience, languages)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
            (email, hash_password(password), name, district, skills, experience, languages),
        )
        
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        print(f"\n✓ Account created successfully! Your ID: {user_id}")
        return True
    except sqlite3.IntegrityError:
        print("Email already exists. Please use a different email.")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def logout():
    global current_user
    current_user = None
    print("\n✓ Logged out successfully.")

def is_logged_in():
    return current_user is not None

def get_current_user():
    return current_user

def update_profile():
    global current_user
    if not current_user:
        print("Please login first.")
        return
    
    print("\n=== Update Profile ===")
    user_id, name, district, skills, experience, languages = current_user
    
    print("--- Current Profile ---")
    print(f"Name: {name}")
    print(f"District: {district}")
    print(f"Skills: {skills}")
    print(f"Experience: {experience}")
    print(f"Languages: {languages}")
    
    print("\n--- Enter New Details ---")
    new_name = get_valid_input("Full Name: ", validate_name, "")
    if not new_name:
        return
    
    new_district = get_valid_input("District: ", validate_district, "")
    if not new_district:
        return
    
    new_skills = get_valid_input("Skills (comma separated): ", validate_skills, "")
    if not new_skills:
        return
    
    new_experience = get_valid_input("Experience: ", validate_experience, "")
    if not new_experience:
        return
    
    new_languages = get_valid_input("Languages (comma separated): ", validate_languages, "")
    if not new_languages:
        return
    
    if update_user_profile(user_id, new_name, new_district, new_skills, new_experience, new_languages):
        current_user = (user_id, new_name, new_district, new_skills, new_experience, new_languages)
        print("✓ Profile updated successfully!")
    else:
        print("Failed to update profile.")

def view_profile():
    global current_user
    if not current_user:
        print("Please login first.")
        return
    
    user_id, name, district, skills, experience, languages = current_user
    print("\n--- Your Profile ---")
    print(f"ID: {user_id}")
    print(f"Name: {name}")
    print(f"District: {district}")
    print(f"Skills: {skills}")
    print(f"Experience: {experience}")
    print(f"Languages: {languages}")
