from database import init_db, seed_data
from user_functions import explore_opportunities, mental_health_resources
from admin_functions import admin_menu
from auth_functions import login, register, logout, is_logged_in, get_current_user, update_profile, view_profile

def main_menu():
    while True:
        try:
            print("\n=== KURA - Youth Growth & Opportunity Bridge ===")
            if is_logged_in():
                user = get_current_user()
                print(f"Logged in as: {user[1]}")
                print("1. View Profile")
                print("2. Update Profile")
                print("3. Explore Opportunities")
                print("4. Mental health and wellbeing resources")
                print("5. Logout")
                print("6. Admin(MOYA/RDB): Log district outreach")
                print("7. Exit")
                choice = input("Enter your choice (1-7): ")
            else:
                print("1. Login")
                print("2. Register")
                print("3. Explore Opportunities")
                print("4. Mental health and wellbeing resources")
                print("5. Admin(MOYA/RDB): Log district outreach")
                print("6. Exit")
                choice = input("Enter your choice (1-6): ")
            return choice
        except KeyboardInterrupt:
            print("\n\nExiting KURA. Goodbye!")
            return '7' if is_logged_in() else '6'
        except EOFError:
            print("\n\nNo input detected. Using default exit.")
            return '7' if is_logged_in() else '6'

def main():
    init_db()
    seed_data()

    while True:
        choice = main_menu()

        if is_logged_in():
            if choice == "1":
                view_profile()
            elif choice == "2":
                update_profile()
            elif choice == "3":
                explore_opportunities()
            elif choice == "4":
                mental_health_resources()
            elif choice == "5":
                logout()
            elif choice == "6":
                admin_menu()
            elif choice == "7":
                print("\nThank you for using KURA!")
                break
            else:
                print("Invalid choice! Please enter 1-7.")
        else:
            if choice == "1":
                login()
            elif choice == "2":
                register()
            elif choice == "3":
                explore_opportunities()
            elif choice == "4":
                mental_health_resources()
            elif choice == "5":
                admin_menu()
            elif choice == "6":
                print("\nThank you for using KURA!")
                break
            else:
                max_choice = "6" if not is_logged_in() else "7"
                print(f"Invalid choice! Please enter 1-{max_choice}.")

        try:
            input("\nPress Enter to continue...")
        except KeyboardInterrupt:
            print("\n\nReturning to main menu...")
        except EOFError:
            print("\n\nReturning to main menu...")

if __name__ == "__main__":
    main()
