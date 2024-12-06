# A Password Generator Library

This library can help you to generate and manage passwords in your programs.

## Table of content

- [Installation](#Installation)
- [PyPi Package](#PyPi-Package)
- [Usage](#Usage)

## Installation

```python3
pip3 install psswd_manager
```

## PyPi Package

- [Url Password Generator](https://pypi.org/project/psswd-manager/)

## Usage

### Geneate password

You can generate a password selecting the numbers of characters.

```python
from password_gen import generate_password

generate_password(number_of_characters)
```

### Save password

You can save the password in a dictionary with a key value (the object is saved as a value).

```python
from password_gen import save_password

save_password(key_value)
```

### Get password with key_value

You can get a saved password with key value.

```python
from password_gen import get_password

get_password(key_value)
```

### Get current password (recently created)

You can get the last password has been created if you didn't save it.

```python
from password_gen import get_current_password

get_current_password()
```

### Change password saved

You can change the password for an existing and saved password.

```python
from password_gen import change_password

change_password(key, new_password)
```

### Delete password saved

You can delete a saved password, with key value.

```python
from password_gen import del_password

del_password(key)
```

### Show all keys of the passwords saved

You can show all keys of the passwords saved.

```python
from password_gen import show_keys

show_keys()
```
