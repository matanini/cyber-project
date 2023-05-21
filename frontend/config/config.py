def read_pass_dict(file):
    pass_list = []
    with open(file, 'r') as f:
        for line in f.readlines():
            pass_list.append(line.strip())
    return pass_list

PASSWORD_DICT_FILE= 'config/1000000-password-seclists.txt'
PASSWORD_POLICY = {
'MIN_LENGTH': 10,
'MAX_LENGTH': 20,
'MIN_SPECIAL_CHARACTERS': 1,
'MIN_UPPERCASE_CHARACTERS': 1,
'MIN_LOWERCASE_CHARACTERS': 1,
'MIN_DIGITS': 1,
'SPECIAL_CHARACTERS': ['$', '@', '#', '%', '&', '*', '!', '?', '+', '-', '_', '~', '^', '[', ']', '{', '}', '<', '>', ',', '.'],
'PASSWORD_DICT' : read_pass_dict(PASSWORD_DICT_FILE)
}
