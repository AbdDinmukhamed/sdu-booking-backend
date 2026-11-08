from abc import ABC, abstractmethod


class LoginAPI(ABC):
    @abstractmethod
    def RequestPassword(self,data):
        pass

class SDU_API(LoginAPI):
    def RequestPassword(self,data):
        pass #probably adapter would be user here if it was a real deal

class TEST_API(LoginAPI):
    def __init__(self):
        self.TEST_USERS = [
          { "login": "240107001", "password": "student123", "role": "student", "name": "Student 240107001" },
          { "login": "240107002", "password": "student123", "role": "student", "name": "Student 240107002" },
          { "login": "240107003", "password": "student123", "role": "student", "name": "Student 240107003" },
          { "login": "staff01", "password": "staff123", "role": "staff", "name": "Staff 01 (Registrar)" },
          { "login": "staff02", "password": "staff123", "role": "staff", "name": "Staff 02 (Faculty)" },
        ]
    def RequestPassword(self,data):
        result = 0
        hasAccount = 0
        account = 0
        while account < len(self.TEST_USERS):
            if self.TEST_USERS[account]["login"] == data[0] and self.TEST_USERS[account]["password"] == data[1]:
                hasAccount = 1
                break
            account += 1
        if hasAccount == 0:
            result = 1
        elif self.TEST_USERS[account]["role"] != data[2]:
            result = 2
        return (result, "ERROR" if result == 1 else self.TEST_USERS[account]["name"])