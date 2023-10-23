import requests
from bs4 import BeautifulSoup
import sqlite3

def parse_and_store_data_from_portal():
    # Устанавливаем соединение с базой данных (или создаем новую, если она не существует)
    conn = sqlite3.connect('biz_sherif.db')
    cursor = conn.cursor()

    # Удаляем существующую таблицу (если она существует)
    cursor.execute('DROP TABLE IF EXISTS biz_sherif')

    # Создаем новую таблицу
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS biz_sherif (
            id INTEGER PRIMARY KEY,
            municipality TEXT,
            full_name TEXT,
            work_phone TEXT,
            mobile_phone TEXT,
            email TEXT
        )
    ''')

    st_accept = "text/html"  # желаемый заголовок Accept
    st_useragent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15"

    # Создаем заголовки
    headers = {
        "Accept": st_accept,
        "User-Agent": st_useragent
    }

    # Отключаем проверку сертификата
    response = requests.get("https://www.YOUR_PARSING_SITE.ru/ru/business/biznes-sherify/", headers=headers, verify=False)

    src = response.text
    soup = BeautifulSoup(src, 'lxml')

    # Все элементы <tr>
    all_tr_elements = soup.find_all('tr')[1:]  # Исключаем первый элемент, так как он содержит заголовки

    # Итерируемся по каждому <tr> элементу и извлекаем данные
    for tr_element in all_tr_elements:
        td_elements = tr_element.find_all('td')

        municipality = td_elements[0].text.strip().replace('\n', ' ')
        municipality = ' '.join(municipality.split()).strip()
        full_name = td_elements[1].text.strip().replace('\n', ' ')
        full_name = ' '.join(full_name.split()).strip()
        work_phone = td_elements[2].text.strip()
        mobile_phone = td_elements[3].text.strip()
        email = td_elements[4].text.strip().replace('\n', ' ')
        email = ' '.join(email.split()).strip()
        work_phone = work_phone.replace('-', '').replace(' (', '').replace(') ', '').replace('(', '').replace(')', '').replace('\n', ' ').replace('+7 ', '8')
        work_phone = ' '.join(work_phone.split()).strip()
        mobile_phone = mobile_phone.replace('-', '').replace(' (', '').replace(') ', '').replace('(', '').replace(')', '').replace('\n', ' ').replace('+7 ', '8').replace(',', ' ')
        mobile_phone = ' '.join(mobile_phone.split()).strip()
        if len(mobile_phone) <= 13:
            mobile_phone = mobile_phone.replace(' ', '')

        # Вставляем данные в базу данных
        cursor.execute('INSERT INTO biz_sherif (municipality, full_name, work_phone, mobile_phone, email) VALUES (?, ?, ?, ?, ?)',
                       (municipality, full_name, work_phone, mobile_phone, email))

    # Сохраняем изменения
    conn.commit()

    # Закрываем соединение с базой данных
    conn.close()

if __name__ == '__main__':
    parse_and_store_data_from_portal()