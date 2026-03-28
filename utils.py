import re
import hashlib
from datetime import datetime

RWANDA_DISTRICTS = [
    "Gasabo", "Kicukiro", "Nyarugenge",
    "Gisagara", "Huye", "Kamonyi", "Muhanga", "Nyamagabe", "Nyanza", "Nyaruguru", "Ruhango",
    "Karongi", "Ngororero", "Nyabihu", "Nyamasheke", "Rubavu", "Rusizi", "Rutsiro",
    "Burera", "Gakenke", "Gicumbi", "Musanze", "Rulindo",
    "Bugesera", "Gatsibo", "Kayonza", "Kirehe", "Ngoma", "Nyagatare", "Rwamagana"
]

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def validate_email(text):
    if not text:
        return False, "Email is required"
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, text):
        return False, "Invalid email format"
    return True, ""

def validate_password(text):
    if not text or len(text) < 6:
        return False, "Password must be at least 6 characters"
    return True, ""

def validate_name(text):
    if not text or len(text.strip()) < 2:
        return False, "Name must be at least 2 characters long"
    if not re.match(r'^[a-zA-Z\s\-\'\.]+$', text):
        return False, "Name can only contain letters, spaces, hyphens, apostrophes, and dots"
    return True, ""

def validate_district(text):
    if not text:
        return False, "District is required"
    
    # Case-insensitive matching
    text_lower = text.lower()
    for district in RWANDA_DISTRICTS:
        if district.lower() == text_lower:
            return True, district  # Return the correctly cased district
    
    return False, f"District must be one of the 30 official Rwandan districts"

def validate_skills(text):
    if not text or len(text.strip()) < 3:
        return False, "Skills must be at least 3 characters long"
    if not re.match(r'^[a-zA-Z\s,\-]+$', text):
        return False, "Skills can only contain letters, spaces, commas, and hyphens"
    return True, ""

def validate_experience(text):
    if not text or len(text.strip()) < 5:
        return False, "Experience must be at least 5 characters long"
    if not re.match(r'^[a-zA-Z0-9\s,\.\-]+$', text):
        return False, "Experience can only contain letters, numbers, spaces, commas, dots, and hyphens"
    return True, ""

def validate_languages(text):
    if not text or len(text.strip()) < 3:
        return False, "Languages must be at least 3 characters long"
    if not re.match(r'^[a-zA-Z\s,\-]+$', text):
        return False, "Languages can only contain letters, spaces, commas, and hyphens"
    return True, ""

def validate_date(text):
    if not text:
        return True, ""
    try:
        parsed_date = datetime.strptime(text, '%Y-%m-%d')
        today = datetime.now()
        if parsed_date > today:
            return False, "Date cannot be in the future"
        return True, ""
    except ValueError:
        return False, "Date must be in YYYY-MM-DD format"

def validate_officials(text):
    if not text or len(text.strip()) < 3:
        return False, "Officials list must be at least 3 characters long"
    if not re.match(r'^[a-zA-Z\s,\.\-]+$', text):
        return False, "Officials can only contain letters, spaces, commas, dots, and hyphens"
    return True, ""

def validate_activities(text):
    if not text or len(text.strip()) < 5:
        return False, "Activities must be at least 5 characters long"
    if not re.match(r'^[a-zA-Z0-9\s,\.\-]+$', text):
        return False, "Activities can only contain letters, numbers, spaces, commas, dots, and hyphens"
    return True, ""

def get_valid_input(prompt, validator, error_msg):
    while True:
        try:
            value = input(prompt).strip()
            if validator == validate_district:
                print("\nAvailable districts:")
                for i, district in enumerate(RWANDA_DISTRICTS, 1):
                    print(f"{i:2d}. {district}")
                print()
            if not value and validator != validate_date:
                print("This field is required.")
                continue
            is_valid, result = validator(value)
            if is_valid:
                # For district validation, return the correctly cased district
                return result if validator == validate_district else value
            print(f"Invalid input: {result}")
        except KeyboardInterrupt:
            print("\nInput cancelled.")
            return None
        except EOFError:
            print("\nNo input detected.")
            return None
