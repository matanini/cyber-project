from app.config.config import DBFILE, PASSWORD_HISTORY_LENGTH, DATE_TIME_FORMAT, USER_BLOCK_TIME, TOKEN_ALIVE_TIME

from datetime import datetime, timedelta
import sqlite3
import secrets



async def create_database():
    conn = sqlite3.connect(DBFILE)
    cursor = conn.cursor()
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS `users` (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT, 
        user_name TEXT NOT NULL UNIQUE,
        user_password TEXT NOT NULL, 
        user_email TEXT NOT NULL UNIQUE,
        password_history TEXT
        )"""
    )
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS `clients` (
        client_id INTEGER PRIMARY KEY AUTOINCREMENT, 
        client_name TEXT, 
        client_email TEXT NOT NULL UNIQUE, 
        client_phone TEXT NOT NULL, 
        client_city TEXT
        )"""
    )
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS `tokens` (
        user_email TEXT PRIMARY KEY, 
        token TEXT NOT NULL UNIQUE, 
        expiry TEXT NOT NULL
        )"""
    )
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS `app` (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        key TEXT NOT NULL UNIQUE, 
        value TEXT NOT NULL
        )"""
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS `login_attempts` (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            username TEXT NOT NULL UNIQUE, 
            attempts_number INTEGER NOT NULL,
            last_time_changed TEXT
            )"""
    )
    conn.commit()
    conn.close()


async def init_app():
    await create_database()
    if len(await get_app_data("salt")) == 0:
        await set_app_data("salt", secrets.token_hex(32))


async def set_app_data(key, value):
    q = "INSERT INTO `app` (key, value) VALUES (?,?)"
    await exec_insert_query(q, key, value)


async def get_app_data(key):
    q = "SELECT value FROM `app` WHERE key=?"
    value = await exec_select_query(q, key)
    return value


# async def exec_select_query(q, *params):

#     # Connect to the database
#     conn = sqlite3.connect(DBFILE)
#     cursor = conn.cursor()
#     if len(params) > 0:
#         cursor.execute(q, params)
#     else:
#         cursor.executescript(q)
#     result = cursor.fetchall()
#     # Close the connection
#     conn.close()
#     return result

async def exec_select_query(q, *params):
    # Connect to the database
    conn = sqlite3.connect(DBFILE)
    cursor = conn.cursor()
    if len(params) > 0:
        cursor.execute(q, params)
    else:
        split_q = q.split(';')
        for sub_q in split_q:
            cursor.execute(sub_q)
    result = cursor.fetchall()
    # Close the connection
    conn.close()
    return result


async def exec_insert_query(q, *params):
    # Connect to the database
    conn = sqlite3.connect(DBFILE)
    cursor = conn.cursor()
    if len(params) > 0:
        cursor.execute(q, params)
    else:
        cursor.executescript(q)
    conn.commit()

    # Close the connection
    conn.close()


async def get_all_clients():
    q = "SELECT * FROM `clients`"
    results = await exec_select_query(q)
    return results


async def get_all_users():
    q = "SELECT * FROM `users`"
    results = await exec_select_query(q)
    return results


async def get_client_by_id(client_id, secure_mode= True):
    if not secure_mode:
        q = f"SELECT * FROM `clients` WHERE client_id='{client_id}'"
        return await exec_select_query(q)
    else:
        q = "SELECT * FROM `clients` WHERE client_id=?"
        return await exec_select_query(q, client_id)


async def get_client_by_email(email, secure_mode):
    if not secure_mode:
        q = f"SELECT * FROM `clients` WHERE client_email='{email}'"
        return await exec_select_query(q)
    q = "SELECT * FROM `clients` WHERE client_email=?"
    return await exec_select_query(q, email)


async def get_user_by_email(email, secure_mode):
    if not secure_mode:
        q = f"SELECT * FROM `users` WHERE user_email='{email}'"
        return await exec_select_query(q)
    q = "SELECT * FROM `users` WHERE user_email=?"
    return await exec_select_query(q, email)


async def get_user_by_user_id(user_id):
    q = "SELECT * FROM `users` WHERE user_id=?"
    return await exec_select_query(q, user_id)


async def get_user_by_username(username, secure_mode):
    if not secure_mode:
        q = f"SELECT * FROM 'users' WHERE user_name='{username}'"

        return await exec_select_query(q)
    else:
        q = "SELECT * FROM `users` WHERE user_name=?"
        return await exec_select_query(q, username)


async def create_new_user(username, hashed_password, email, secure_mode):
    if not secure_mode:
        q = f"INSERT INTO `users` (user_name, user_password, user_email, password_history) VALUES ('{username}', '{hashed_password}', '{email}', '{hashed_password}')"
        await exec_insert_query(q)
    else:
        q = "INSERT INTO `users` (user_name, user_password, user_email, password_history) VALUES (?, ?, ?, ?)"
        await exec_insert_query(q, username, hashed_password, email, hashed_password)


async def create_new_client(name, email, phone, city, secure_mode):
    if not secure_mode:
        q = f"INSERT INTO `clients` (client_name, client_email, client_phone, client_city) VALUES ('{name}', '{email}', '{phone}', '{city}')"
        await exec_insert_query(q)
    else:
        q = "INSERT INTO `clients` (client_name, client_email, client_phone, client_city) VALUES (?, ?, ?, ?)"
        await exec_insert_query(q, name, email, phone, city)


async def update_user(user_id, username, password, email):
    q = "UPDATE `users` SET user_name=?, user_password=?, user_email=? WHERE user_id=?"
    await exec_insert_query(q, username, password, email, user_id)
    return await get_user_by_user_id(user_id)


async def reset_password(email, password, password_history, secure_mode):
    if len(password_history) > PASSWORD_HISTORY_LENGTH:
        password_history = password_history[-PASSWORD_HISTORY_LENGTH:]

    q = "UPDATE `users` SET user_password=?, password_history=? WHERE user_email=?"
    await exec_insert_query(q, password, ",".join(password_history), email)
    return await get_user_by_email(email, secure_mode)


async def change_password(username, password, password_history, secure_mode):
    # make sure we don't have more than PASSWORD_HISTORY_LENGTH passwords in the history
    if len(password_history) > PASSWORD_HISTORY_LENGTH:
        password_history = password_history[-PASSWORD_HISTORY_LENGTH:]

    q = "UPDATE `users` SET user_password=?, password_history=? WHERE user_name=?"
    await exec_insert_query(q, password, ",".join(password_history), username)
    return await get_user_by_username(username, secure_mode)


def check_old_passwords(password, old_passwords):
    if len(old_passwords) == 0:
        return True
    return password not in old_passwords


async def save_new_token(email, token):
    db_token = await get_token_by_mail(email)
    if len(db_token) > 0:
        await remove_token_by_mail(email)
    q = "INSERT INTO `tokens` (user_email, token, expiry) VALUES (?, ?, ?)"
    await exec_insert_query(q, email, token, 
                            (datetime.now() + 
                             timedelta(days=TOKEN_ALIVE_TIME["day"], hours=TOKEN_ALIVE_TIME["hour"], minutes=TOKEN_ALIVE_TIME["minute"])).strftime(DATE_TIME_FORMAT))


async def get_token_by_mail(email):
    q = "SELECT token FROM `tokens` WHERE user_email=?"
    return await exec_select_query(q, email)

async def get_token_data_by_mail(email):
    q = "SELECT * FROM `tokens` WHERE user_email=?"
    return await exec_select_query(q, email)


async def get_token_data_by_token(token):
    q = "SELECT * FROM `tokens` WHERE token=?"
    return await exec_select_query(q, token)


async def remove_token_by_mail(email):
    q = "DELETE FROM `tokens` WHERE user_email=?"
    await exec_insert_query(q, email)


async def remove_token(token):
    q = "DELETE FROM `tokens` WHERE token=?"
    await exec_insert_query(q, token)


async def delete_login_attempt(username):
    q = "DELETE FROM `login_attempts` WHERE username=?"
    await exec_insert_query(q, username)


async def get_login_attempts(username):
    q = "SELECT * FROM `login_attempts` WHERE username=?"
    data = await exec_select_query(q, username)

    if len(data) > 0:
        data = list(data[0])
        data[3] = datetime.strptime(data[3], DATE_TIME_FORMAT)
        if (
            data[3]
            + timedelta(days=USER_BLOCK_TIME["day"], hours=USER_BLOCK_TIME["hour"], minutes=USER_BLOCK_TIME["minute"])
            < datetime.now()
        ):
            await delete_login_attempt(username)
            data = []
    return data


async def increment_login_attempts(username):
    res_login_attempts = await get_login_attempts(username)
    if len(res_login_attempts) == 0:
        q = "INSERT INTO `login_attempts` (username, attempts_number, last_time_changed) VALUES (?, ? ,?)"
        await exec_insert_query(q, username, 0, datetime.now().strftime(DATE_TIME_FORMAT))
        res_login_attempts = await get_login_attempts(username)

    q = "UPDATE `login_attempts` SET attempts_number=?, last_time_changed=? WHERE username=?"
    await exec_insert_query(q, res_login_attempts[2] + 1, datetime.now().strftime(DATE_TIME_FORMAT), username)

    return await get_login_attempts(username)
