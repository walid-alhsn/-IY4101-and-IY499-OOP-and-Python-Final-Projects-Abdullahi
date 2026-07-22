# AIRLINE / FLIGHT BOOKING MANAGEMENT SYSTEM

import hashlib
import hmac
import json
import secrets
import tkinter as tk
import uuid

from pathlib import Path
from tkinter import messagebox, ttk


# FILE PATHS

# The folder containing this Python file
BASE_DIR = Path(__file__).resolve().parent

# The folder where the JSON data files will be stored
DATA_DIR = BASE_DIR / "data"

# Individual JSON file locations
USERS_FILE = DATA_DIR / "users.json"
FLIGHTS_FILE = DATA_DIR / "flights.json"
BOOKINGS_FILE = DATA_DIR / "bookings.json"


# FILE-HANDLING FUNCTIONS

def create_data_files():
    """
    Create the data folder and JSON files if they do not
    already exist.
    """

    # Create the data folder
    DATA_DIR.mkdir(exist_ok=True)

    data_files = [
        USERS_FILE,
        FLIGHTS_FILE,
        BOOKINGS_FILE
    ]

    for file_path in data_files:
        if not file_path.exists():
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump([], file, indent=4)

            print(f"Created: {file_path.name}")


def load_json_file(file_path):
    """
    Load and return data from a JSON file.

    If the file is missing or contains invalid JSON,
    an empty list is returned instead of crashing.
    """

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    except FileNotFoundError:
        print(f"Error: {file_path.name} could not be found.")
        return []

    except json.JSONDecodeError:
        print(f"Error: {file_path.name} contains invalid JSON data.")
        return []


def save_json_file(file_path, data):
    """
    Save Python data to a JSON file.

    Returns True when the data is saved successfully.
    Returns False when an error occurs.
    """

    try:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        return True

    except OSError as error:
        print(f"Error saving {file_path.name}: {error}")
        return False

# VALIDATION FUNCTIONS

def validate_name(name):
    """
    Check that a full name is valid.

    Returns:
        (True, "") when the name is valid.
        (False, error_message) when it is invalid.
    """

    name = name.strip()

    if name == "":
        return False, "Full name cannot be empty."

    if len(name) < 2:
        return False, "Full name must contain at least two characters."

    for character in name:
        if not (
            character.isalpha()
            or character.isspace()
            or character in "-'"
        ):
            return False, (
                "Full name can only contain letters, spaces, "
                "hyphens and apostrophes."
            )

    return True, ""


def validate_email(email):
    """
    Check that an email address has a reasonable format.
    """

    email = email.strip()

    if email == "":
        return False, "Email address cannot be empty."

    if " " in email:
        return False, "Email address cannot contain spaces."

    if email.count("@") != 1:
        return False, "Email address must contain one @ symbol."

    local_part, domain_part = email.split("@")

    if local_part == "":
        return False, "Email address must contain text before the @ symbol."

    if domain_part == "":
        return False, "Email address must contain a domain after the @ symbol."

    if "." not in domain_part:
        return False, "Email domain must contain a full stop."

    if domain_part.startswith(".") or domain_part.endswith("."):
        return False, "Email domain cannot start or end with a full stop."

    return True, ""


def validate_phone(phone):
    """
    Check that a telephone number has a reasonable format.
    """

    phone = phone.strip()

    if phone == "":
        return False, "Telephone number cannot be empty."

    # Remove permitted formatting characters
    cleaned_phone = phone.replace(" ", "")
    cleaned_phone = cleaned_phone.replace("-", "")
    cleaned_phone = cleaned_phone.replace("(", "")
    cleaned_phone = cleaned_phone.replace(")", "")

    # Permit one + symbol only at the beginning
    if cleaned_phone.startswith("+"):
        digits = cleaned_phone[1:]
    else:
        digits = cleaned_phone
    # Check if the remaining characters are all digits
    if not digits.isdigit():
        return False, "Telephone number can only contain numbers."
    # Check the length of the digits
    if len(digits) < 7 or len(digits) > 15:
        return False, "Telephone number must contain between 7 and 15 digits."

    return True, ""


def validate_password(password):
    """
    Check whether a password satisfies the account requirements.
    """

    if password == "":
        return False, "Password cannot be empty."

    if len(password) < 8:
        return False, "Password must contain at least eight characters."

    has_uppercase = False
    has_lowercase = False
    has_digit = False

    # check for at least one uppercase letter, one lowercase letter, and one digit
    for character in password:
        if character.isupper():
            has_uppercase = True
        elif character.islower():
            has_lowercase = True
        elif character.isdigit():
            has_digit = True

    if not has_uppercase:
        return False, "Password must contain at least one uppercase letter."

    if not has_lowercase:
        return False, "Password must contain at least one lowercase letter."

    if not has_digit:
        return False, "Password must contain at least one number."

    return True, ""

# AUTHENTICATION FUNCTIONS

def normalise_email(email):
    """
    Remove unnecessary spaces and convert an email address
    to lowercase.
    """

    return email.strip().lower()


def email_exists(email, users):
    """
    Check whether an email address is already registered.
    """

    email = normalise_email(email)

    for user in users:
        if normalise_email(user["email"]) == email:
            return True

    return False


def generate_user_id():
    """
    Generate a unique user ID.
    """

    random_part = uuid.uuid4().hex[:8].upper()
    return f"USR-{random_part}"


def create_password_hash(password, salt):
    """
    Create a secure password hash using the supplied salt.
    """

    salt_bytes = bytes.fromhex(salt)
    password_bytes = password.encode("utf-8")

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password_bytes,
        salt_bytes,
        100000
    )

    return password_hash.hex()


def register_user(
    full_name,
    email,
    phone,
    password,
    confirm_password
):
    """
    Validate and register a new passenger account.

    Returns:
        True and a success message when registration succeeds.
        False and an error message when registration fails.
    """

    # Validate the passenger's name
    is_valid, message = validate_name(full_name)

    if not is_valid:
        return False, message

    # Validate the email address
    is_valid, message = validate_email(email)

    if not is_valid:
        return False, message

    # Validate the telephone number
    is_valid, message = validate_phone(phone)

    if not is_valid:
        return False, message

    # Validate the password
    is_valid, message = validate_password(password)

    if not is_valid:
        return False, message

    # Ensure both password fields match
    if password != confirm_password:
        return False, "Passwords do not match."

    users = load_json_file(USERS_FILE)

    # Ensure the loaded data is a list
    if not isinstance(users, list):
        return False, "The user data file has an invalid structure."

    cleaned_email = normalise_email(email)

    # Prevent duplicate accounts
    if email_exists(cleaned_email, users):
        return False, "An account already exists with this email address."

    # Generate a random salt and hash the password
    salt = secrets.token_hex(16)
    password_hash = create_password_hash(password, salt)

    new_user = {
        "user_id": generate_user_id(),
        "full_name": full_name.strip(),
        "email": cleaned_email,
        "phone": phone.strip(),
        "password_hash": password_hash,
        "salt": salt,
        "role": "passenger"
    }

    users.append(new_user)

    if save_json_file(USERS_FILE, users):
        return True, "Account created successfully."

    return False, "The account could not be saved."

def find_user_by_email(email, users):
    """
    Find and return a user with the supplied email address.

    Returns None if the email address is not registered.
    """

    cleaned_email = normalise_email(email)

    for user in users:
        saved_email = normalise_email(user.get("email", ""))

        if saved_email == cleaned_email:
            return user

    return None


def authenticate_user(email, password):
    """
    Authenticate a user using their email address and password.

    Returns:
        True, success message and user details when login succeeds.
        False, error message and None when login fails.
    """

    email = email.strip()

    if email == "" or password == "":
        return False, "Email and password are required.", None

    users = load_json_file(USERS_FILE)

    if not isinstance(users, list):
        return False, "The user data file has an invalid structure.", None

    user = find_user_by_email(email, users)

    if user is None:
        return False, "Invalid email address or password.", None

    stored_salt = user.get("salt", "")
    stored_hash = user.get("password_hash", "")

    if stored_salt == "" or stored_hash == "":
        return False, "The account data is incomplete.", None

    try:
        entered_hash = create_password_hash(
            password,
            stored_salt
        )

    except ValueError:
        return False, "The account data is invalid.", None

    if not hmac.compare_digest(entered_hash, stored_hash):
        return False, "Invalid email address or password.", None

    # Do not pass the password hash or salt to the GUI
    authenticated_user = {
        "user_id": user["user_id"],
        "full_name": user["full_name"],
        "email": user["email"],
        "phone": user["phone"],
        "role": user["role"]
    }

    return True, "Login successful.", authenticated_user

# ==========================================================
# GRAPHICAL USER INTERFACE
# ==========================================================

class AirlineBookingApp:
    """
    Main graphical user interface for the airline booking
    management system.
    """

    def __init__(self, root):
        """
        Set up the main application window.
        """

        self.root = root
        self.current_user = None

        self.root.title("Airline Booking Management System")
        self.root.geometry("750x550")
        self.root.minsize(700, 500)

        # Configure reusable widget styles
        self.style = ttk.Style()

        self.style.configure(
            "Title.TLabel",
            font=("Arial", 24, "bold")
        )

        self.style.configure(
            "Subtitle.TLabel",
            font=("Arial", 12)
        )

        self.style.configure(
            "Dashboard.TButton",
            font=("Arial", 12),
            padding=10
        )

        self.show_login_page()

    def clear_window(self):
        """
        Remove every widget currently displayed in the window.
        """

        for widget in self.root.winfo_children():
            widget.destroy()

    # ======================================================
    # LOGIN PAGE
    # ======================================================

    def show_login_page(self):
        """
        Display the login page.
        """

        self.clear_window()

        main_frame = ttk.Frame(
            self.root,
            padding=40
        )
        main_frame.pack(expand=True)

        title_label = ttk.Label(
            main_frame,
            text="Airline Booking System",
            style="Title.TLabel"
        )
        title_label.grid(
            row=0,
            column=0,
            columnspan=2,
            pady=(0, 10)
        )

        subtitle_label = ttk.Label(
            main_frame,
            text="Log in to search, book and manage your flights",
            style="Subtitle.TLabel"
        )
        subtitle_label.grid(
            row=1,
            column=0,
            columnspan=2,
            pady=(0, 30)
        )

        email_label = ttk.Label(
            main_frame,
            text="Email address:"
        )
        email_label.grid(
            row=2,
            column=0,
            sticky="w",
            padx=(0, 15),
            pady=10
        )

        self.login_email_entry = ttk.Entry(
            main_frame,
            width=35
        )
        self.login_email_entry.grid(
            row=2,
            column=1,
            pady=10
        )

        password_label = ttk.Label(
            main_frame,
            text="Password:"
        )
        password_label.grid(
            row=3,
            column=0,
            sticky="w",
            padx=(0, 15),
            pady=10
        )

        self.login_password_entry = ttk.Entry(
            main_frame,
            width=35,
            show="*"
        )
        self.login_password_entry.grid(
            row=3,
            column=1,
            pady=10
        )

        login_button = ttk.Button(
            main_frame,
            text="Log In",
            command=self.handle_login
        )
        login_button.grid(
            row=4,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=(20, 10)
        )

        signup_text = ttk.Label(
            main_frame,
            text="Do not have an account?"
        )
        signup_text.grid(
            row=5,
            column=0,
            columnspan=2,
            pady=(15, 5)
        )

        signup_button = ttk.Button(
            main_frame,
            text="Create an Account",
            command=self.show_signup_page
        )
        signup_button.grid(
            row=6,
            column=0,
            columnspan=2,
            sticky="ew"
        )

        self.login_email_entry.focus()

    def handle_login(self):
        """
        Read the login form and authenticate the user.
        """

        email = self.login_email_entry.get()
        password = self.login_password_entry.get()

        success, message, user = authenticate_user(
            email,
            password
        )

        if not success:
            messagebox.showerror(
                "Login Failed",
                message
            )
            return

        self.current_user = user

        messagebox.showinfo(
            "Login Successful",
            f"Welcome, {user['full_name']}!"
        )

        if user["role"] == "admin":
            self.show_admin_dashboard()
        else:
            self.show_passenger_dashboard()

    # ======================================================
    # SIGN-UP PAGE
    # ======================================================

    def show_signup_page(self):
        """
        Display the new-account registration page.
        """

        self.clear_window()

        main_frame = ttk.Frame(
            self.root,
            padding=35
        )
        main_frame.pack(expand=True)

        title_label = ttk.Label(
            main_frame,
            text="Create an Account",
            style="Title.TLabel"
        )
        title_label.grid(
            row=0,
            column=0,
            columnspan=2,
            pady=(0, 25)
        )

        full_name_label = ttk.Label(
            main_frame,
            text="Full name:"
        )
        full_name_label.grid(
            row=1,
            column=0,
            sticky="w",
            padx=(0, 15),
            pady=8
        )

        self.signup_name_entry = ttk.Entry(
            main_frame,
            width=35
        )
        self.signup_name_entry.grid(
            row=1,
            column=1,
            pady=8
        )

        email_label = ttk.Label(
            main_frame,
            text="Email address:"
        )
        email_label.grid(
            row=2,
            column=0,
            sticky="w",
            padx=(0, 15),
            pady=8
        )

        self.signup_email_entry = ttk.Entry(
            main_frame,
            width=35
        )
        self.signup_email_entry.grid(
            row=2,
            column=1,
            pady=8
        )

        phone_label = ttk.Label(
            main_frame,
            text="Telephone number:"
        )
        phone_label.grid(
            row=3,
            column=0,
            sticky="w",
            padx=(0, 15),
            pady=8
        )

        self.signup_phone_entry = ttk.Entry(
            main_frame,
            width=35
        )
        self.signup_phone_entry.grid(
            row=3,
            column=1,
            pady=8
        )

        password_label = ttk.Label(
            main_frame,
            text="Password:"
        )
        password_label.grid(
            row=4,
            column=0,
            sticky="w",
            padx=(0, 15),
            pady=8
        )

        self.signup_password_entry = ttk.Entry(
            main_frame,
            width=35,
            show="*"
        )
        self.signup_password_entry.grid(
            row=4,
            column=1,
            pady=8
        )

        confirm_password_label = ttk.Label(
            main_frame,
            text="Confirm password:"
        )
        confirm_password_label.grid(
            row=5,
            column=0,
            sticky="w",
            padx=(0, 15),
            pady=8
        )

        self.signup_confirm_entry = ttk.Entry(
            main_frame,
            width=35,
            show="*"
        )
        self.signup_confirm_entry.grid(
            row=5,
            column=1,
            pady=8
        )

        password_rule_label = ttk.Label(
            main_frame,
            text=(
                "Password must contain at least 8 characters, "
                "one uppercase letter,\none lowercase letter "
                "and one number."
            )
        )
        password_rule_label.grid(
            row=6,
            column=0,
            columnspan=2,
            pady=(10, 15)
        )

        create_account_button = ttk.Button(
            main_frame,
            text="Create Account",
            command=self.handle_signup
        )
        create_account_button.grid(
            row=7,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=(5, 10)
        )

        back_button = ttk.Button(
            main_frame,
            text="Back to Login",
            command=self.show_login_page
        )
        back_button.grid(
            row=8,
            column=0,
            columnspan=2,
            sticky="ew"
        )

        self.signup_name_entry.focus()

    def handle_signup(self):
        """
        Read the sign-up form and attempt to create an account.
        """

        full_name = self.signup_name_entry.get()
        email = self.signup_email_entry.get()
        phone = self.signup_phone_entry.get()
        password = self.signup_password_entry.get()
        confirm_password = self.signup_confirm_entry.get()

        success, message = register_user(
            full_name,
            email,
            phone,
            password,
            confirm_password
        )

        if not success:
            messagebox.showerror(
                "Registration Failed",
                message
            )
            return

        messagebox.showinfo(
            "Account Created",
            message
        )

        self.show_login_page()

        # Automatically insert the newly registered email
        self.login_email_entry.insert(
            0,
            normalise_email(email)
        )

        self.login_password_entry.focus()

    # ======================================================
    # PASSENGER DASHBOARD
    # ======================================================

    def show_passenger_dashboard(self):
        """
        Display the main dashboard for a passenger.
        """

        self.clear_window()

        main_frame = ttk.Frame(
            self.root,
            padding=40
        )
        main_frame.pack(
            fill="both",
            expand=True
        )

        welcome_label = ttk.Label(
            main_frame,
            text=f"Welcome, {self.current_user['full_name']}",
            style="Title.TLabel"
        )
        welcome_label.pack(pady=(20, 10))

        email_label = ttk.Label(
            main_frame,
            text=self.current_user["email"],
            style="Subtitle.TLabel"
        )
        email_label.pack(pady=(0, 30))

        search_button = ttk.Button(
            main_frame,
            text="Search and Book a Flight",
            style="Dashboard.TButton",
            command=lambda: self.show_feature_message(
                "Flight Search"
            )
        )
        search_button.pack(
            fill="x",
            padx=120,
            pady=8
        )

        bookings_button = ttk.Button(
            main_frame,
            text="My Bookings",
            style="Dashboard.TButton",
            command=lambda: self.show_feature_message(
                "My Bookings"
            )
        )
        bookings_button.pack(
            fill="x",
            padx=120,
            pady=8
        )

        check_in_button = ttk.Button(
            main_frame,
            text="Check In",
            style="Dashboard.TButton",
            command=lambda: self.show_feature_message(
                "Check In"
            )
        )
        check_in_button.pack(
            fill="x",
            padx=120,
            pady=8
        )

        logout_button = ttk.Button(
            main_frame,
            text="Log Out",
            style="Dashboard.TButton",
            command=self.logout
        )
        logout_button.pack(
            fill="x",
            padx=120,
            pady=(25, 8)
        )

    # ======================================================
    # ADMINISTRATOR DASHBOARD
    # ======================================================

    def show_admin_dashboard(self):
        """
        Display a temporary administrator dashboard.
        """

        self.clear_window()

        main_frame = ttk.Frame(
            self.root,
            padding=40
        )
        main_frame.pack(
            fill="both",
            expand=True
        )

        title_label = ttk.Label(
            main_frame,
            text="Administrator Dashboard",
            style="Title.TLabel"
        )
        title_label.pack(pady=(40, 15))

        welcome_label = ttk.Label(
            main_frame,
            text=f"Welcome, {self.current_user['full_name']}",
            style="Subtitle.TLabel"
        )
        welcome_label.pack(pady=(0, 30))

        information_label = ttk.Label(
            main_frame,
            text="Administrator features will be added later."
        )
        information_label.pack(pady=20)

        logout_button = ttk.Button(
            main_frame,
            text="Log Out",
            command=self.logout
        )
        logout_button.pack(pady=20)

    # ======================================================
    # GENERAL GUI FUNCTIONS
    # ======================================================

    def show_feature_message(self, feature_name):
        """
        Display a temporary message for features that have
        not yet been implemented.
        """

        messagebox.showinfo(
            feature_name,
            f"The {feature_name} feature will be added next."
        )

    def logout(self):
        """
        Log out the current user and return to the login page.
        """

        self.current_user = None
        self.show_login_page()

# ==========================================================
# PROGRAM START
# ==========================================================

def main():
    """
    Prepare the files and start the graphical application.
    """

    create_data_files()

    root = tk.Tk()
    AirlineBookingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
