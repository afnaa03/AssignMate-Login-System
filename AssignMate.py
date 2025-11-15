import sqlite3
import hashlib

#different functions
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_database():
    conn = sqlite3.connect("assignmate.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()



def create_account(): # For account creation when they dont have account
    print("\n--- Create an Account ---")
    username = input("Create a username or MyCollege ID: ")
    password = input("Create a password: ")

    conn = sqlite3.connect("assignmate.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        print("❌ Username already exists. Try another one.")
    else:
        hashed = hash_password(password)
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed))
        conn.commit()
        print("✅ Account created successfully!")

    conn.close()


def forgot_password(): # When they forgot their password
    print("\n--- Reset Password ---")
    username = input("Enter your username or EMPLID: ")

    conn = sqlite3.connect("assignmate.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        new_pass = input("Enter your new password: ")
        hashed = hash_password(new_pass)

        cursor.execute("UPDATE users SET password = ? WHERE username = ?", (hashed, username))
        conn.commit()
        print("✅ Password updated successfully!")
    else:
        print("❌ Username not found.")

    conn.close()





def select_role(): # Asking whether they are a teacher or student
    while True:
        print("Welcome to AssignMate!")
        print("\nAre you a ...?")
        print("1. Student")
        print("2. Teacher")
        choice = input("Choose an option: ")

        if choice == "1":
            return "Student"
        elif choice == "2":
            return "Teacher"
        else:
            print("Invalid choice. Try again.")




def login_screen(role): # This is the login screen, shows different login options 
    while True:
        print(f"\n===== AssignMate ({role} login) =====")
        print("1. Login")
        print("2. Don't Have an Account? Set up Here")
        print("3. Forgot Password?")
        print("4. Back")
        choice = input("Choose an option: ")

        
        if choice == "1": # Input Login information
            username = input("Username or EMPLID: ")
            password = input("Password: ")
            if authenticate(username, password):
                print(f"✅ Login successful! Welcome Back {username}!")
                return
            else:
                print("❌ Incorrect username or password.")

        # Create account
        elif choice == "2":
            create_account()

        # Forgot Password
        elif choice == "3":
            forgot_password()

        # Back
        elif choice == "4":
            break

        else:
            print("Invalid choice. Try again.")




def authenticate(username, password): # Checked Whether Login Authentication is Correct
    hashed = hash_password(password)

    conn = sqlite3.connect("assignmate.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed))
    user = cursor.fetchone()
    conn.close()
    return user is not None




def main():
    create_database()
    role = select_role()  
    login_screen(role)

main()