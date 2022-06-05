class User:
    def __init__(self, email, password):
         self.email = email
         self.password = password
    
    def to_string(self):
        return f"Login details: {self.email}, {self.password}"
