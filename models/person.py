class Person:
    def __init__(self, id, first_name, last_name):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def to_dict(self):
        return {
            "id" : self.id,
            "first name" : self.first_name,
            "last name" : self.last_name,
            "full name" : self.get_full_name()
        }