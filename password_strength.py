import sys
import string

BLACKLIST_FILEPATH = 'blacklist.txt'
PERSONAL_DATA_FILEPATH = 'personal.txt'
COMPANY_DATA_FILEPATH = 'company.txt'
WELLKNOWN_PASSWORDS_FILEPATH = 'wellknown_passwords.txt'


def is_case_sensitive(password):
    # the use of both upper-case and lower-case letters (case sensitivity)
    def has_lowercase(password):
        for char in string.ascii_lowercase:
            if char in password:
                return True

    def has_uppercase(password):
        for char in string.ascii_uppercase:
            if char in password:
                return True

    return has_lowercase(password) and has_uppercase(password)


def has_digits(password):
    # inclusion of one or more numerical digits
    for char in string.digits:
        if char in password:
            return True


def has_special_chars(password):
    # inclusion of special characters, such as @, #, $
    for char in string.punctuation:
        if char in password:
            return True


def load_prohibited_words(filepath):
    with open(filepath, mode='r') as prohibited_words_file:
        prohibited_passwords = []
        for line in prohibited_words_file:
            if not line.startswith('#'):
                prohibited_passwords.append(line.rstrip())
    return prohibited_passwords


def is_not_wellknown_password(password, well_known_passwords):
    for well_known_password in well_known_passwords:
        if well_known_password.lower() == password.lower():
            return False
    return True


def is_not_prohibited(password, prohibited_words):
    # prohibition of words found in a password blacklist
    # prohibition of words found in the user's personal information
    # prohibition of use of company name or an abbreviation
    for prohibited_word in prohibited_words:
        if (prohibited_word in password
                or prohibited_word.upper() in password
                or prohibited_word.lower() in password):
            return False
    return True


def has_not_formats():
    # prohibition of passwords that match the format of calendar dates,
    # license plate numbers, telephone numbers, or other common numbers
    raise NotImplemented


def get_password_content(password, prohibited_words):
    password_checklist = [
        is_case_sensitive(password),
        has_digits(password),
        has_special_chars(password),
        is_not_prohibited(password, prohibited_words),
        # has_not_formats()
    ]
    return password_checklist.count(True) / len(password_checklist)


def get_password_length(password):
    # initial research states that 12 symbols password is still Ok:
    if len(password) >= 12:
        return 1
    else:
        return len(password) / 12


def get_password_strength(password_content, password_length):
    return password_content * password_length


if __name__ == '__main__':
    try:
        prohibited_words = load_prohibited_words(BLACKLIST_FILEPATH)
        prohibited_words += load_prohibited_words(PERSONAL_DATA_FILEPATH)
        prohibited_words += load_prohibited_words(COMPANY_DATA_FILEPATH)
        well_known_passwords = load_prohibited_words(WELLKNOWN_PASSWORDS_FILEPATH)
    except FileNotFoundError as exception:
        sys.exit(exception)
    password = input('Введите пароль:\n>')
    if is_not_wellknown_password(password, well_known_passwords):
        password_strength = int(10 * get_password_strength(
            get_password_content(password, prohibited_words),
            get_password_length(password)
        ))
        print('The strongest of your password is {level} out from 10'.format(
            level=password_strength))
    else:
        print('The strongest of your password is 0 out from 10.\n'
              'You are using well-known password!')
