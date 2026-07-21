# AIRLINE / FLIGHT BOOKING MANAGEMENT SYSTEM

import hashlib
import json
import secrets
import uuid
from pathlib import Path


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

# PROGRAM START

def main():
    """
    Prepare the data files and test user registration.
    """

    create_data_files()

    print("\nTesting user registration:")

    success, message = register_user(
        "Test Passenger",
        "test@example.com",
        "+44 7123 456789",
        "Airline123",
        "Airline123"
    )

    print(f"Registration successful: {success}")
    print(f"Message: {message}")

    users = load_json_file(USERS_FILE)

    print(f"\nRegistered users: {len(users)}")

    if len(users) > 0:
        print(f"User ID: {users[0]['user_id']}")
        print(f"Name: {users[0]['full_name']}")
        print(f"Email: {users[0]['email']}")
        print(f"Role: {users[0]['role']}")

if __name__ == "__main__":
    main()
