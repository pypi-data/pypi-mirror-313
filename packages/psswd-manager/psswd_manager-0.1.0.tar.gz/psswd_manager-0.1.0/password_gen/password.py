class Password:

    LOW = "qwertyuiopasdfghjklzxcvbnm" # 26 characters
    HIGH = "QWERTYUIOPASDFGHJKLZXCVBNM" # 26 characters
    SPECIAL = "!\";#$%&'()*+,-./:;<=>?@[]^_`{|}~" # 32 characters
    NUMBER = "1234567890" # 10 characters

    all_passwords={}

    def __init__(self, password, key=""):
        self.key = key
        self._password = password

    def __repr__(self):
        return f"Password object with {len(self._password)} characters"

    @classmethod
    def save_password(cls, key, self): # class.save_object(key, obj)
        cls.all_passwords[key] = self

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = password


def get_lower_value(num):

    if num < len(Password.LOW):
        return Password.LOW[num]
    else:
        raise IndexError(f"[!] El valor que ingrese tiene que ser menor a {len(Password.LOW)}")

def get_higher_value(num):

    if num < len(Password.HIGH):
        return Password.HIGH[num]
    else:
        raise IndexError(f"[!] El valor que ingrese tiene que ser menor a {len(Password.HIGH)}")

def get_special_value(num):

    if num < len(Password.SPECIAL):
        return Password.SPECIAL[num]
    else:
        raise IndexError(f"[!] El valor que ingrese tiene que ser menor a {len(Password.SPECIAL)}")

def get_number_value(num):

    if num < len(Password.NUMBER):
        return Password.NUMBER[num]
    else:
        raise IndexError(f"[!] El valor que ingrese tiene que ser menor a {len(Password.SPECIAL)}")


def get_all_passwords():
    return Password.all_passwords

def delete_pass(key):
    Password.all_passwords.pop(key)
