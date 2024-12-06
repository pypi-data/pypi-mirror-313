#!/usr/bin/env python3

from .password import *
import random

obj = ""
current_psswd = ""
dict_passwords = get_all_passwords()

def show_keys():
    global dict_passwords
    dict_passwords = get_all_passwords()

    for key in dict_passwords.keys():
        print(key)

def get_current_password():
    return current_psswd

def get_password(key):
    global dict_passwords
    dict_passwords = get_all_passwords()

    if key in dict_passwords:
        password = dict_passwords[key]
        return password.password
    else:
        raise IndexError("[!] The given key doesn't exist")

def del_password(key):
    global dict_passwords
    dict_passwords = get_all_passwords()

    if key in dict_passwords:
        delete_pass(key)
    else:
        raise IndexError("[!] The given key doesn't exist")

def change_password(key, new_value):
    global dict_passwords
    dict_passwords = get_all_passwords()

    if key in dict_passwords:
        password = dict_passwords[key]
        password.password = new_value
    else:
        raise IndexError("[!] The given key doesn't exist")

def save_password(key):
    global dict_passwords
    dict_passwords = get_all_passwords()

    if key in dict_passwords:
        raise ValueError(f"[!] The password with key '{key}', already exist")
    else:
        obj.key = key
        obj.save_password(key, obj)

def generate_object(pswd):
    global obj
    global current_psswd
    obj = Password(pswd)
    current_psswd = pswd

def generate_password(characters):

    pswd = ""
    letters_low = len(Password.LOW) - 1
    letters_high = len(Password.HIGH) - 1
    letters_special = len(Password.SPECIAL) - 1
    letters_number = len(Password.NUMBER) - 1

    for i in range(characters):
        x = random.randint(1,4)

        if x == 1:
            c = random.randint(0, letters_low)
            pswd += get_lower_value(c)
        elif x == 2:
            c = random.randint(0, letters_high)
            pswd += get_higher_value(c)
        elif x == 3:
            c = random.randint(0, letters_special)
            pswd += get_special_value(c)
        else:
            c = random.randint(0, letters_number)
            pswd += get_special_value(c)

    generate_object(pswd)

