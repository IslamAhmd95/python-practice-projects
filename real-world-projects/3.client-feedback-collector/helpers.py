import re


def is_valid_name(name):
    return bool(re.match(r'^[A-Za-z][A-Za-z0-9\s\-]*$', name))

def is_valid_phone(phone):
    cleaned_phone = re.sub(r"[ \-\(\)]", "", phone)  # Remove spaces, dashes, parentheses
    return bool(re.match(r'^(\+?\d{5,15})$', cleaned_phone))

def is_valid_email(email):
    return bool(re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email))

def is_valid_feedback_message(feedback_message):
    return len(feedback_message) >= 30


def validate_feedback(feedback):
    
    for key, value in feedback.items():
        if not value:
            raise ValueError(f"{key.capitalize()} can't be empty.")

    # dict.get(key, default)
    # If "name" does not exist (i.e., missing), use "" instead (empty string), it's more safer then feedback["name"] which will give a keyerror if the name doesn't exist
    if not is_valid_name(feedback.get("name", "")):
        raise ValueError("Invalid name. Use only letters, spaces, or hyphens.")
    
    if not is_valid_phone(feedback.get("phone", "")):
        raise ValueError("Invalid phone number. Must be 5 to 15 digits, optionally starting with '+'.")
    
    if not is_valid_email(feedback.get("email", "")):
        raise ValueError("Invalid email. Format must be like 'name@example.com'.")
    
    if not is_valid_feedback_message(feedback.get("feedback_message", "")):
        raise ValueError("Invalid message. Message must contain at least 30 characters.")
