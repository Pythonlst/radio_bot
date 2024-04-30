import sqlite3


def insert(data, table=False, file_name='data/data.db'):
    try:
        sqlite_connection = sqlite3.connect(file_name)
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        if table == 'pictures':
            param = 'id, name, date, description, url, download'
        elif table == 'users':
            param = 'id, nickname, username, date, language, last_send'

        sqlite_insert_with_param = f"""CREATE TABLE IF NOT EXISTS {table}({param});"""
        cursor.execute(sqlite_insert_with_param)
        sqlite_insert_with_param = f'''INSERT INTO {table}({param}) 
                    VALUES({', '.join(['?'] * len(param.split(',')))});'''
        cursor.execute(sqlite_insert_with_param, data)
        sqlite_connection.commit()
        print(f"Переменные Python успешно вставлены в таблицу {file_name}")
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")