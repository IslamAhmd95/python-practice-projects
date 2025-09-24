class Database:
    """Simulating a basic user database table"""
    def __init__(self):
        self.data = {}

    def add_user(self, user_id, name):
        if user_id in self.data:
            raise ValueError("User already exists")
        self.data[user_id] = name
    
    def get_user(self, user_id):
        return self.data.get(user_id, None)
    
    def delete_user(self, user_id):
        if self.get_user(user_id):
            del self.data[user_id]