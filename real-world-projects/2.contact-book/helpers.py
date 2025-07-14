import re
import os
import json


def is_valid_name(name):
    return bool(re.match(r'^[A-Za-z][A-Za-z0-9\s\-]*$', name.strip()))


def is_valid_phone(phone):
    phone = phone.replace(" ", "").strip()
    return bool(re.match(r'^(\+?\d{5,15})$', phone))


def is_valid_email(email):
    return bool(re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email.strip()))


def validate_contact(contact):
    # dict.get(key, default)
    # If "name" does not exist (i.e., missing), use "" instead (empty string).
    if not is_valid_name(contact.get("name", "")):
        raise ValueError("Invalid name. Use only letters, spaces, or hyphens.")
    
    if not is_valid_phone(contact.get("phone", "")):
        raise ValueError("Invalid phone number. Must be 5 to 15 digits, optionally starting with '+'.")
    
    if not is_valid_email(contact.get("email", "")):
        raise ValueError("Invalid email. Format must be like 'name@example.com'.")


def get_contacts():
    if not os.path.exists('contacts.json') or os.path.getsize('contacts.json') == 0:
        contacts = []
    else:
        with open('contacts.json') as rf:
            contacts = json.load(rf)

    return contacts


def get_last_contact():
    contacts = get_contacts()

    if contacts:
        return contacts[-1]
    else:
        return None


def search_contacts(contacts, query):
    results = []

    for contact in contacts:
        if any(query in str(value).lower() for value in contact.values()):
            results.append(contact)

    return results


def get_contact_by_id(contacts, contact_id):
    for contact in contacts:
        if contact['id'] == contact_id:
            return contact
    return None


def get_contact_id(action_name):
    contact_id = input(f"Enter contact ID or (type q to cancel {action_name}): ").strip()
    if contact_id.lower() == 'q':
        print(f"{action_name.capitalize()} cancelled.\n")
        return None
    if not contact_id.isdigit():
        print("The contact ID has to be a numeric value.\n")
        return False
    return int(contact_id)
