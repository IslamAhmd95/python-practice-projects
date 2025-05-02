# 📇 Contact Manager (CLI-based)

A simple command-line contact manager written in Python. You can **add**, **view**, **search**, **update**, and **delete** contacts. All data is stored locally in a `contacts.json` file.

---


## 🚀 Features

- ✅ Add new contact (with name, phone, and email)
- 📋 View all saved contacts
- 🔍 Search contacts by name
- ✏️ Update existing contact
- ❌ Delete a contact
- 💾 Data is saved in JSON format

---

## How to Run

1. Clone the repository and navigate to the project folder:

   `cd python-practice-projects/real-world-projects/2.contact-book` 


2. Run the script:

   `python main.py`

   You’ll be prompted with options like:

      - `add` – to add a new contact

      - `view` – to see all contacts

      - `search` – to find a contact by name

      - `update` – to update name, phone, or email

      - `delete` – to delete a contact

      - `exit` – to close the app

---

## 📌 Notes

1. ✅ Input Validation

   - Names must only contain letters, spaces, or hyphens (e.g., Islam, John Doe, Ali-Mahmoud).

   - Phone numbers must be digits (you can allow specific formats if needed).

   - Emails must follow a valid pattern (example@domain.com).

   - IDs must be numeric when updating or deleting.

2. 📦 Data Storage

   All contacts are stored in a simple `contacts.json` file in the same folder. The file is automatically created on first use.

3. You can type `q` when prompted for contact ID to cancel an update or delete action.

4. The app is beginner-friendly and designed to reinforce real-world Python skills like:

   - File I/O with JSON

   - Input validation

   - Modular design with helper functions

   - Error and exception handling