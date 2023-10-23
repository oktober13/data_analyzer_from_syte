import docx
import sqlite3


def parse_and_store_docx(file_name):
    # Устанавливаем соединение с базой данных (или создаем новую, если она не существует)
    conn = sqlite3.connect('biz_sherif.db')
    cursor = conn.cursor()

    # Удаляем существующую таблицу (если она существует)
    cursor.execute('DROP TABLE IF EXISTS biz_sherif_docx')

    # Создаем новую таблицу
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS biz_sherif_docx (
            id INTEGER PRIMARY KEY,
            municipality TEXT,
            full_name TEXT,
            work_phone TEXT,
            mobile_phone TEXT,
            email TEXT
        )
    ''')

    # Теперь извлекаем данные из файла .docx
    doc = docx.Document(file_name)

    # Пропускаем первую строку, так как она содержит заголовки
    for row in doc.tables[0].rows[1:]:
        cells = row.cells
        # punct = cells[0].text.strip()
        municipality = cells[1].text.strip().replace('\n', ' ')
        municipality = ' '.join(municipality.split()).strip()
        full_name = cells[2].text.strip().replace('\n', ' ')
        full_name = ' '.join(full_name.split()).strip()
        work_phone = cells[4].text.strip()
        mobile_phone = cells[5].text.strip()
        email = cells[6].text.strip().replace('\n', ' ')
        email = ' '.join(email.split()).strip()
        work_phone = work_phone.replace('-', '').replace(' (', '').replace(') ', '').replace('(', '').replace(')', '').replace('\n', ' ').replace('+7 ', '8')
        work_phone = ' '.join(work_phone.split()).strip()
        mobile_phone = mobile_phone.replace('-', '').replace(' (', '').replace(') ', '').replace('(', '').replace(')', '').replace('\n', ' ').replace('+7 ', '8').replace(',', ' ')
        mobile_phone = ' '.join(mobile_phone.split()).strip()
        if len(mobile_phone) <= 13:
            mobile_phone = mobile_phone.replace(' ', '')

        # Вставляем данные в базу данных
        cursor.execute('INSERT INTO biz_sherif_docx (municipality, full_name, work_phone, mobile_phone, email) VALUES (?, ?, ?, ?, ?)',
                       (municipality, full_name, work_phone, mobile_phone, email))

    # Сохраняем изменения
    conn.commit()

    # Закрываем соединение с базой данных
    conn.close()


if __name__ == '__main__':
    parse_and_store_docx('Обновленный список БШ 18.10.2023.docx')