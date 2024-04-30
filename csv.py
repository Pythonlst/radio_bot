import sqlite3


def insert(id, name, date, description, url, dowload):
    try:
        sqlite_connection = sqlite3.connect('data/random_data.db')
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        sqlite_insert_with_param = """CREATE TABLE IF NOT EXISTS 
                                                    pictures(id, name, date, description, url, download);"""
        cursor.execute(sqlite_insert_with_param)
        sqlite_connection.commit()
        sqlite_insert_with_param = '''INSERT INTO pictures(id, name, date, description, url, download)
                                                                                VALUES(?, ?, ?, ?, ?, ?);'''
        data_tuple = (id, name, date, description, url, dowload)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqlite_connection.commit()
        print("Переменные Python успешно вставлены в таблицу random_data.db")

        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")
