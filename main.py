#для начала скопируй сюда интерфейс "Умных заметок" и проверь его работу

#затем запрограммируй демо-версию функционала
# ---------- ІМПОРТ БІБЛІОТЕК ----------
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QListWidget, QLineEdit, 
                             QTextEdit, QInputDialog, QHBoxLayout, QVBoxLayout, QFormLayout)
import os  # модуль для роботи з файлами
import json

# ---------- СТВОРЕННЯ ЗАСТОСУНКУ ТА ДАНИХ ----------
app = QApplication([])   # головний об’єкт PyQt-додатку
notes = []               # список усіх заміток
# структура замітки: [назва, текст, [теги]]

if os.path.exists("notes_data.json"):

    with open("notes_data.json", "r", encoding="utf-8") as file:
        notes = json.load(file)

else:

    notes = {
        "Ласкаво просимо!" : {
            "текст" : "Це найкращий додаток для заміток у світі!",
            "теги" : ["додаток", "інструкція"]
        }
    }

    with open("notes_data.json", "w", encoding="utf-8") as file:
        json.dump(notes,file)

# ---------- НАЛАШТУВАННЯ ВІКНА ----------
notes_win = QWidget()                       # головне вікно
notes_win.setWindowTitle('Розумні замітки') # заголовок
notes_win.resize(900, 600)                  # розмір вікна


# ---------- ВІДЖЕТИ (ЕЛЕМЕНТИ ІНТЕРФЕЙСУ) ----------
list_notes = QListWidget()                  # список заміток
list_notes_label = QLabel('Список заміток') # підпис до списку


# кнопки для роботи із замітками
button_note_create = QPushButton('Створити замітку')  # створення нової
button_note_del = QPushButton('Видалити замітку')     # видалення
button_note_save = QPushButton('Зберегти замітку')    # збереження


# поле для введення тегу
field_tag = QLineEdit('')
field_tag.setPlaceholderText('Введіть тег...')

field_text = QTextEdit()                    # поле для тексту замітки

# кнопки для роботи з тегами
button_tag_add = QPushButton('Додати до замітки')
button_tag_del = QPushButton('Відкріпити від замітки')
button_tag_search = QPushButton('Шукати замітки по тегу')

list_tags = QListWidget()                   # список тегів
list_tags_label = QLabel('Список тегів')    # підпис до тегів


# ---------- РОЗТАШУВАННЯ ВІДЖЕТІВ (LAYOUTS) ----------
layout_notes = QHBoxLayout()  # головний горизонтальний лейаут

# ліва колонка (текст замітки)
col_1 = QVBoxLayout()
col_1.addWidget(field_text)

# права колонка (список заміток і теги)
col_2 = QVBoxLayout()
col_2.addWidget(list_notes_label)
col_2.addWidget(list_notes)

# рядок кнопок створення та видалення
row_1 = QHBoxLayout()
row_1.addWidget(button_note_create)
row_1.addWidget(button_note_del)

# рядок кнопки збереження
row_2 = QHBoxLayout()
row_2.addWidget(button_note_save)

col_2.addLayout(row_1)
col_2.addLayout(row_2)

# блок тегів
col_2.addWidget(list_tags_label)
col_2.addWidget(list_tags)
col_2.addWidget(field_tag)

# кнопки для роботи з тегами
row_3 = QHBoxLayout()
row_3.addWidget(button_tag_add)
row_3.addWidget(button_tag_del)

row_4 = QHBoxLayout()
row_4.addWidget(button_tag_search)

col_2.addLayout(row_3)
col_2.addLayout(row_4)

# додаємо колонки до головного лейауту
layout_notes.addLayout(col_1, stretch=2)  # більше місця для тексту
layout_notes.addLayout(col_2, stretch=1)

notes_win.setLayout(layout_notes)          # застосовуємо лейаут


# ---------- ЗАВАНТАЖЕННЯ ЗАМІТОК З ФАЙЛІВ ----------
def load_notes():
    index = 0  # номер файлу (0.txt, 1.txt, 2.txt...)

    # цикл працює, поки знаходить файли
    while True:
        filename = f"{index}.txt"  # формуємо ім'я файлу

        # якщо файл не існує — зупиняємо завантаження
        if not os.path.exists(filename):
            break

        # відкриваємо файл для читання
        with open(filename, "r", encoding="utf-8") as file:
            lines = file.read().split('\n')  # читаємо всі рядки

            name = lines[0]  # перший рядок — назва замітки
            text = lines[1]  # другий рядок — текст замітки

            # третій рядок — теги (якщо він існує)
            tags = lines[2].split() if len(lines) > 2 else []

            # додаємо замітку у список
            notes.append([name, text, tags])

            # додаємо назву замітки у список на екрані
            list_notes.addItem(name)

        index += 1  # переходимо до наступного файлу



# ---------- ЗБЕРЕЖЕННЯ ВСІХ ЗАМІТОК ----------
def save_all_notes():
    # перебираємо всі замітки разом з їх індексами
    for i, note in enumerate(notes):
        # відкриваємо файл для запису
        with open(f"{i}.txt", "w", encoding="utf-8") as file:
            file.write(note[0] + '\n')       # записуємо назву
            file.write(note[1] + '\n')       # записуємо текст
            file.write(' '.join(note[2]) + '\n')  # записуємо теги



# ---------- ПОКАЗ ВИБРАНОЇ ЗАМІТКИ ----------
def show_note():
    # отримуємо назву вибраної замітки зі списку
    key = list_notes.selectedItems()[0].text()

    # шукаємо замітку з такою ж назвою
    for note in notes:
        if note[0] == key:
            field_text.setText(note[1])  # показуємо текст замітки

            # оновлюємо список тегів
            list_tags.clear()
            list_tags.addItems(note[2])


# ---------- СТВОРЕННЯ НОВОЇ ЗАМІТКИ ----------
def add_note():
    # показуємо вікно введення назви замітки
    note_name, ok = QInputDialog.getText(
        notes_win, "Додати замітку", "Назва замітки: "
    )

    # якщо користувач натиснув OK і ввів назву
    if ok and note_name != "":
        # створюємо порожню замітку
        note = [note_name, '', []]

        # додаємо її у список
        notes.append(note)

        # додаємо назву в список на екрані
        list_notes.addItem(note_name)

        # зберігаємо всі замітки
        save_all_notes()



# ---------- ЗБЕРЕЖЕННЯ ТЕКСТУ ЗАМІТКИ ----------
def save_note():
    # перевіряємо, чи вибрана замітка
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()

        # шукаємо замітку за назвою
        for note in notes:
            if note[0] == key:
                # оновлюємо текст замітки
                note[1] = field_text.toPlainText()
                break

        # зберігаємо зміни у файли
        save_all_notes()



# ---------- ВИДАЛЕННЯ ЗАМІТКИ ----------
def del_note():
    # перевіряємо, чи вибрана замітка
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()

        # шукаємо замітку та видаляємо її зі списку
        for i, note in enumerate(notes):
            if note[0] == key:
                notes.pop(i)
                break

        # очищаємо інтерфейс
        list_notes.clear()
        list_tags.clear()
        field_text.clear()

        # видаляємо старі файли заміток
        for i in range(1000):
            try:
                os.remove(f"{i}.txt")
            except:
                break

        # оновлюємо список заміток на екрані
        for note in notes:
            list_notes.addItem(note[0])

        # зберігаємо оновлений список
        save_all_notes()


# ---------- ДОДАВАННЯ ТЕГУ ДО ЗАМІТКИ ----------
def add_tag():
    # перевіряємо, чи вибрана замітка
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = field_tag.text()

        # додаємо тег, якщо його ще немає
        for note in notes:
            if note[0] == key and tag not in note[2]:
                note[2].append(tag)
                list_tags.addItem(tag)
                field_tag.clear()

        # зберігаємо зміни
        save_all_notes()



# ---------- ВИДАЛЕННЯ ТЕГУ ----------
def del_tag():
    # перевіряємо, чи вибрані тег і замітка
    if list_tags.selectedItems() and list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = list_tags.selectedItems()[0].text()

        # видаляємо тег зі списку
        for note in notes:
            if note[0] == key and tag in note[2]:
                note[2].remove(tag)

        # оновлюємо список тегів
        list_tags.clear()
        for note in notes:
            if note[0] == key:
                list_tags.addItems(note[2])

        # зберігаємо зміни
        save_all_notes()


# ---------- ПОШУК ЗАМІТОК ЗА ТЕГОМ ----------
def search_tag():
    tag = field_tag.text()

    # режим пошуку
    if button_tag_search.text() == "Шукати замітки по тегу" and tag:
        list_notes.clear()

        # показуємо тільки замітки з цим тегом
        for note in notes:
            if tag in note[2]:
                list_notes.addItem(note[0])

        button_tag_search.setText("Скинути пошук")

    # режим скидання пошуку
    else:
        list_notes.clear()

        # показуємо всі замітки
        for note in notes:
            list_notes.addItem(note[0])

        button_tag_search.setText("Шукати замітки по тегу")
        field_tag.clear()



# ---------- ОБРОБНИКИ ПОДІЙ ----------
list_notes.itemClicked.connect(show_note)
button_note_create.clicked.connect(add_note)
button_note_save.clicked.connect(save_note)
button_note_del.clicked.connect(del_note)
button_tag_add.clicked.connect(add_tag)
button_tag_del.clicked.connect(del_tag)
button_tag_search.clicked.connect(search_tag)


# ---------- ЗАПУСК ПРОГРАМИ ----------
load_notes()      # завантажуємо замітки з файлів
notes_win.show()  # показуємо вікно
app.exec_()       # запускаємо цикл програми