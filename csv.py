import sqlite3


def insert(dev_id, name, join_date, description):
    try:
        sqlite_connection = sqlite3.connect('data/sqlite.db')
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        sqlite_insert_with_param = """INSERT INTO users
                              (id, name, date, description)
                              VALUES (?, ?, ?, ?);"""

        data_tuple = (dev_id, name, join_date, description)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqlite_connection.commit()
        print("Переменные Python успешно вставлены в таблицу sqlite.db")

        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")
