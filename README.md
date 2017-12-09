# Password Strength Calculator
This Python script interactively scores cryptographic strength of the passwords. Weakness analysis is based on research [
Study Title: 2015 Trustwave Global Security Report](http://passwordresearch.com/stats/study143.html)

Script checks that password meet next requirements:
- contains letters of both cases
- contains digits
- contains special symbols
- does NOT contain blacklisted words (see below)
- does NOT contain digits in well-known forms: years, phone numbers and dates

and has length not less than twelve chars 

Password has a maximum score "10" if all listed conditions are satisfied. If not, score will be decreased proportionally by amount of unsatisfied requirements and missing chars in length. If user inputs well-known password than score will be "0".

# How to run
Code was designed and tested for Python 3.5. This script doesn't require any additional packages.

To execute just use command line environment of your choice. For instance, Terminal app in Mac OS X:
```shell
Host:Dir User$ python3 password_strength.py 
Input your password:
>ThisIsRe@lly1ongAndDiffultP@ssw0rd
The strongest of your password is 10 out from 10
```
Execution in Windows or Linux environments id the same except you must specify `python` instead of `python3` depends on system configuration.  

# How to adapt the code to your needs
You can enrich set of well-known passwords by adding new ones to `wellknown_passwords.txt` If you need to introduce new set of blacklisted words, for instance, localize them, just put new file into work directory and address name of the file in `BLACKLISTED_WORDS_FILE_NAMES` parameters dictionary. You can also include new banned formats: to do so, please specify new formats into `BLACKLISTED_FORMATS` parameters dictionary in standard regular expression way. Both dictionaries are located in main executable file: `password_strength.py`.

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
