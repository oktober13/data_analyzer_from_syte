# Телеграм-бот для анализа данных об актуальности на сайте

Этот телеграм-бот позволяет вам анализировать данные из файлов .docx (в котором содержится таблица с новыми данными для размещения на сайте), сравнивать их с данными онлайн-портала(сайта) и получать разхождения(в данном случае текущий список Бизнес-шерифов) в формате txt файла.

#### !!! Важно  
В данном проекте я рассматривал конкретную задачу под свои нужды,  
смысл алгоритма можете использовать по своему усмотрению.  

**Конкретная суть программы:**  
`mode_parse_portal.py` - **(можно настроить на любые данные)** настроен, чтобы парсить таблицу с портала(сайта) и заносить в базу данных.  
`mod_docx.py` - **(можно настроить на любые данные)** настроен, чтобы считывать таблицу с входного эталонного документа и сравнивать с текущими данными в существующей базе данных (данные с сайта).  
`main.py` - можно в режиме консоли запускать программу отсюда, результат будет сохранен в файл `differences.txt` и выведен на консоль.  
`parse_bsh_bot.py` - код телеграм бота, настроен на получение текущей информации из блока портала(сайта), а также есть возможность загрузить новые данные и сравнить с текущими данными на портале(сайте).  


## Возможности

- Анализ и сравнение данных в файлах .docx с данными онлайн-портала.
- Получение текущего списка Бизнес-шерифов.
- Удобный интерфейс с кнопками для легкой навигации.

## Начало работы

Чтобы начать использовать этого бота, выполните следующие шаги:

1. Клонируйте этот репозиторий на ваше локальное устройство.

2. Установите необходимые зависимости, перечисленные в `requirements.txt`, с помощью pip:

   ```shell
   pip install -r requirements.txt
   ```
3. Настройте своего телеграм-бота:

    *Создайте нового бота в Telegram и получите его токен.*

    *Замените переменную BOT_TOKEN в файле token_bot.py на токен вашего бота.*

4. Запустите скрипт parse_bsh_bot.py, чтобы запустить бота:
```shell
python parse_bsh_bot.py
```

5. Взаимодействуйте с ботом в вашем приложении Telegram, чтобы анализировать файлы .docx и получать текущий список предприятий.


## Использование

__Запустите бота, отправив команду /start.__  
Выберите одно из доступных действий:  
`"Проверить файл .docx"` - _для анализа файла .docx._  
`"Текущий список БШ"` - _для получения текущего списка предприятий._


## Лицензия

Вы можете свободно использовать, копировать, изменять и распространять этот проект без необходимости соблюдать какие-либо лицензии или ограничения.

Этот проект предоставляется "как есть" без каких-либо гарантий. 
Автор не несет ответственности за любой ущерб, вызванный использованием этого проекта.


## Благодарности

В этом проекте используется библиотека Telebot для разработки телеграм-ботов.  
Анализ данных выполняется с использованием Python и различных библиотек.  
Данные о предприятиях получаются с онлайн-портала.  
Не стесняйтесь вносить свой вклад в проект или настраивать бота под свои потребности.

_Замените `BOT_TOKEN` в `token_bot.py` на фактический токен вашего бота. Этот `README.md` предоставляет информацию о вашем проекте и как начать использовать бота._  
_Если у вас есть дополнительные вопросы или требуется дополнительная помощь, пожалуйста, дайте знать._
