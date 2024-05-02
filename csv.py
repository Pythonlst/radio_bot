import sqlite3


def insert(data, table=False, file_name='data/data.db'):
    try:
        # подключение бд
        sqlite_connection = sqlite3.connect(file_name)
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        # создание столбиков и маски вставки значений
        if table == 'pictures':
            param = 'id, name, date, description, url, download'
            sqlite_insert_with_param = f"""CREATE TABLE IF NOT EXISTS {table}({param});"""
            cursor.execute(sqlite_insert_with_param)
        elif table == 'users':
            param = 'id UNIQUE, nickname, username, date, language, last_send'
            sqlite_insert_with_param = f"""CREATE TABLE IF NOT EXISTS {table}({param});"""
            cursor.execute(sqlite_insert_with_param)
            param = 'id, nickname, username, date, language, last_send'

        # проверка наличия записи
        marks_ids = [x[0] for x in cursor.execute(f"select id from {table}").fetchall()]
        if data[0] in marks_ids:
            buf = ', '.join(map(lambda x: str(x) + ' = ?', param.split(', ')))
            sqlite_insert_with_param = f'UPDATE {table} SET {buf} WHERE id = {data[0]}'
            print('обновление записи...')
        else:
            sqlite_insert_with_param = f'''INSERT INTO {table}({param}) 
                    VALUES({', '.join(['?'] * len(param.split(',')))});'''
            print('новая запись...')

        # применение шаблона
        cursor.execute(sqlite_insert_with_param, data)
        sqlite_connection.commit()
        print(f"операция прошла успешно, таблица: {file_name}")
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")