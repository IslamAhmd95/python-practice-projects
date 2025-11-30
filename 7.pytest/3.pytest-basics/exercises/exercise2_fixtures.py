# exercise2_fixture.py

class Calculator:
    def __init__(self):
        self.memory = 0

    def remember(self, value):
        """Store a value in memory."""
        self.memory = value

    def recall(self):
        """Return the currently stored memory."""
        return self.memory

    def clear(self):
        """Clear the memory."""
        self.memory = 0


class UserDB:
    """A fake in-memory user database."""

    def __init__(self):
        self.users = {}

    def add_user(self, username, email):
        if username in self.users:
            raise ValueError("User already exists")

        self.users[username] = {"email": email}
        return True

    def get_user(self, username):
        return self.users.get(username)

    def clear(self):
        self.users = {}
