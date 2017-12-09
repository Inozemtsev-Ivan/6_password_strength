import sys
import string
import re

BLACKLISTED_FORMATS = [
    r'.*\d{2}-\d{2}-\d{2}.*',
    r'.*\d{3}-\d{3}.*',
    r'.*\d{6}.*',
    r'.*(19|20)\d{2}.*',
    r'.*[0-3]\d[-/\.]*[01]\d.*',
    r'.*[01]\d[-/\.]*[0-3]\d.*',
]

BLACKLISTED_WORDS_FILES = {
    'WORLD_CITIES':         'world_city_names.txt',
    'US_CITIES':            'us_city_names.txt',
    'US_STATES':            'us_states_names.txt',
    'BABY_NAMES':           'baby_names.txt',
    'DOG_NAMES':            'dog_names.txt',
    'PERSONAL_DATA':        'personal.txt',
    'COMPANY_DATA':         'company.txt',
}

WELLKNOWN_PASSWORDS_FILENAME = 'wellknown_passwords.txt'


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


def load_blacklist(filepath):
    with open(filepath, mode='r') as prohibited_words_file:
        prohibited_passwords = []
        for line in prohibited_words_file:
            if not line.startswith('#'):
                prohibited_passwords.extend(line.rstrip().split())
    return prohibited_passwords


def is_not_wellknown_password(password, well_known_passwords):
    for well_known_password in well_known_passwords:
        if well_known_password.lower() == password.lower():
            return False
    return True


def is_not_blacklisted(password, blacklisted_words):
    # prohibition of words found in a password blacklist
    # prohibition of words found in the user's personal information
    # prohibition of use of company name or an abbreviation
    for prohibited_word in blacklisted_words:
        if any([prohibited_word in password,
                prohibited_word.upper() in password,
                prohibited_word.lower() in password]):
            return False
    return True


def has_not_formats(password, formats):
    # prohibition of passwords that match the format of calendar dates,
    # license plate numbers, telephone numbers, or other common numbers
    patterns = [re.compile(_format) for _format in formats]
    for pattern in patterns:
        if re.search(pattern, password):
            return False
    return True


def check_content(password, blacklisted_words, blacklisted_formats):
    password_checklist = [
        is_case_sensitive(password),
        has_digits(password),
        has_special_chars(password),
        is_not_blacklisted(password, blacklisted_words),
        has_not_formats(password, blacklisted_formats),
    ]
    return password_checklist.count(True) / len(password_checklist)


def check_length(password):
    # initial research states that 12 symbols password is still Ok:
    if len(password) >= 12:
        return 1
    else:
        return len(password) / 12


def get_password_strength(password_content, password_length):
    return password_content * password_length


if __name__ == '__main__':
    try:
        blacklisted_words = []
        for blacklisted_type in BLACKLISTED_WORDS_FILES.keys():
            blacklisted_words.extend(
                load_blacklist(BLACKLISTED_WORDS_FILES[blacklisted_type])
            )
        well_known_passwords = load_blacklist(WELLKNOWN_PASSWORDS_FILENAME)
    except FileNotFoundError as exception:
        sys.exit(exception)
    password = input('Input your password:\n>')
    if is_not_wellknown_password(password, well_known_passwords):
        password_strength = int(10 * get_password_strength(
            check_content(password, blacklisted_words, BLACKLISTED_FORMATS),
            check_length(password)
        ))
        print('The strongest of your password is {level} out from 10'.format(
            level=password_strength))
    else:
        print('The strongest of your password is 0 out from 10.\n'
              'You are using well-known password!')
