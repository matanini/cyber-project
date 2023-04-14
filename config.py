
HOST_NAME = "localhost"
HOST_PORT = 80
DBFILE = "users.db"


############  Password Policy ############
PASSWORD_POLICY = {
'MIN_LENGTH': 8,
'MAX_LENGTH': 20,
'MIN_SPECIAL_CHARACTERS': 1,
'MIN_UPPERCASE_CHARACTERS': 1,
'MIN_LOWERCASE_CHARACTERS': 1,
'MIN_DIGITS': 1,
'SPECIAL_CHARACTERS': ['$', '@', '#', '%', '&', '*', '!', '?', '+', '-', '_', '~', '^', '[', ']', '{', '}', '<', '>', ',', '.'],

}

