import re
from config.config import PASSWORD_POLICY

def check_password_policy(st, password):
    val = True

    if len(password) < PASSWORD_POLICY["MIN_LENGTH"]:
        st.info(f'length should be at least {PASSWORD_POLICY["MIN_LENGTH"]}')
        val = False

    if len(password) > PASSWORD_POLICY["MAX_LENGTH"]:
        st.info(f'length should be not be greater than {PASSWORD_POLICY["MAX_LENGTH"]}')
        val = False

    dig_count = 0
    up_count = 0
    low_count = 0
    spec_count = 0
    for char in password:
        if char.isdigit():
            dig_count += 1
        elif char.isupper():
            up_count += 1
        elif char.islower():
            low_count += 1
        elif char in PASSWORD_POLICY["SPECIAL_CHARACTERS"]:
            spec_count += 1
        else:
            val = False
            st.info(f"Cant use {char} in password")

    if dig_count < PASSWORD_POLICY["MIN_DIGITS"]:
        st.info(f'Password should have at least {PASSWORD_POLICY["MIN_SPECIAL_CHARACTERS"]} numeral')
        val = False

    if up_count < PASSWORD_POLICY["MIN_UPPERCASE_CHARACTERS"]:
        st.info(f'Password should have at least {PASSWORD_POLICY["MIN_UPPERCASE_CHARACTERS"]} uppercase letter')
        val = False

    if low_count < PASSWORD_POLICY["MIN_LOWERCASE_CHARACTERS"]:
        st.info(f'Password should have at least {PASSWORD_POLICY["MIN_LOWERCASE_CHARACTERS"]} lowercase letter')
        val = False

    if spec_count < PASSWORD_POLICY["MIN_SPECIAL_CHARACTERS"]:
        st.info(f'Password should have at least {PASSWORD_POLICY["MIN_DIGITS"]} special symbols')
        val = False
    
    if password in PASSWORD_POLICY["PASSWORD_DICT"]:
        st.info("Password is too common")
        val = False

    return val


def check_password_match(password, confirm_password):
    return password == confirm_password


def check_email(email):
    format = r"^[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z0-9]+$"
    return re.match(format, email)