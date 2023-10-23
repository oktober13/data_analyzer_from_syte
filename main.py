import os
import sqlite3
from mod_parse_portal import parse_and_store_data_from_portal
from mod_docx import parse_and_store_docx

def find_differences():
    # Устанавливаем соединение с базой данных
    conn = sqlite3.connect('biz_sherif.db')
    cursor = conn.cursor()

    # Создаем временную таблицу для идентификации различий
    cursor.execute('''
        CREATE TEMP TABLE IF NOT EXISTS temp_diff AS
        SELECT 
            a.id AS id,
            CASE 
                WHEN a.municipality <> b.municipality THEN 'municipality'
                WHEN a.full_name <> b.full_name THEN 'full_name'
                WHEN a.mobile_phone <> b.mobile_phone THEN 'mobile_phone'
            ELSE NULL END AS diff_column
        FROM biz_sherif AS a
        JOIN biz_sherif_docx AS b ON a.id = b.id
        WHERE 
            a.municipality <> b.municipality OR
            a.full_name <> b.full_name OR
            a.mobile_phone <> b.mobile_phone
    ''')

    # Выбираем различия из временной таблицы
    cursor.execute('''
        SELECT a.id, b.municipality, b.full_name, b.mobile_phone
        FROM temp_diff AS a
        JOIN biz_sherif AS b ON a.id = b.id
    ''')

    # Открываем файл для записи
    with open('differences.txt', 'w', encoding='cp1251') as differences_file:
        # Запишите сообщение, чтобы показать, что файл создан
        differences_file.write("Результаты сравнения:\n")

        differences = cursor.fetchall()

        # Если различия найдены, выведите их
        if differences:
            with open('differences.txt', 'a', encoding='cp1251') as differences_file:
                differences_file.write("Различия между таблицами biz_sherif и biz_sherif_docx:\n")
                print("Различия между таблицами biz_sherif и biz_sherif_docx:")
                for row in differences:
                    differences_file.write(str(row) + "\n")
                    print(row)
        else:
            with open('differences.txt', 'a', encoding='cp1251') as differences_file:
                differences_file.write("Таблицы biz_sherif и biz_sherif_docx идентичны.\n")
                print("Таблицы biz_sherif и biz_sherif_docx идентичны.")


def get_biz_sherif_table():
    # Устанавливаем соединение с базой данных
    conn = sqlite3.connect('biz_sherif.db')
    cursor = conn.cursor()

    # Выбираем все записи из таблицы biz_sherif
    cursor.execute('SELECT * FROM biz_sherif')
    biz_sherif_data = cursor.fetchall()

    # Формируем текст с данными
    table_text = "Текущий список БШ:\n\n"
    for row in biz_sherif_data:
        table_text += f"ID: {row[0]}\n"
        table_text += f"Municipality: {row[1]}\n"
        table_text += f"Full Name: {row[2]}\n"
        table_text += f"Work Phone: {row[3]}\n"
        table_text += f"Mobile Phone: {row[4]}\n"
        table_text += f"Email: {row[5]}\n\n"

    # Закрываем соединение с базой данных
    conn.close()

    return table_text


if __name__ == '__main__':
    file_name = input()  # 'Обновленный список БШ 18.10.2023.docx'
    parse_and_store_data_from_portal()
    parse_and_store_docx(file_name)
    find_differences()