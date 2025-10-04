import json
import hashlib


class User:
    def __init__(self, username, password_hash):
        self.username = username
        self.password_hash = password_hash
        self.transactions = []

    def verify_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest() == self.password_hash


class UserManager:
    def __init__(self, filename="users.json"):
        self.filename = filename
        self.users = self.load_users()

    def load_users(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                users = {}
                for username, info in data.items():
                    user = User(username, info["password"])
                    user.transactions = info.get("transactions", [])
                    users[username] = user
                return users
        except FileNotFoundError:
            return {}

    def save_users(self):
        data = {
            username: {
                "password": user.password_hash,
                "transactions": user.transactions
            }
            for username, user in self.users.items()
        }
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def register(self, username, password):
        if username in self.users:
            raise Exception("שם משתמש כבר קיים")
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        self.users[username] = User(username, password_hash)
        self.save_users()

    def login(self, username, password):
        user = self.users.get(username)
        if user and user.verify_password(password):
            return user
        else:
            raise Exception("שם משתמש או סיסמה לא נכונים")
