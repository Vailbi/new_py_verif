import time
import csv
from tempfile import NamedTemporaryFile
import shutil
import os
# начальное имя файла
name_file_csv = 'note.csv'


def first_file():
    with open(name_file_csv, 'w', newline='', encoding='UTF-8') as file:
        writer = csv.writer(file)
        content = ['id', 'Название заметки', 'Текст заметки', 'Дата создания']
        writer.writerow(content)


def get_data():
    return time.strftime("%d.%m.%Y - %H:%M:%S", time.localtime())


def get_listFile_csv():  # создает список файлов csv из рабочей директории
    csv_list = list(i for i in os.listdir() if 'csv' in i)
    return csv_list


def get_id():
    filedir = os.path.abspath(name_file_csv)
    with open(filedir, 'r', newline='', encoding='UTF-8') as file:
        reader = csv.reader(file)
        load = list(reader)[-1:][0][0]
        if load == 'id':
            load = 0
        else:
            load = int(load) + 1
    return str(load)



# Cоздание записи в заметках
def add_new_note():
    main = input('Введите название заметки: ')
    text = input('Введите текст заметки: ')
    with open(name_file_csv, 'a', newline='', encoding='UTF-8') as file:
        writer = csv.writer(file)
        try:
            writer.writerow([get_id(), main, text, get_data()])
        except:
            writer.writerow(['0', main, text, get_data()])


def read_csv():

    name = os.path.abspath(name_file_csv)
    with open(name, 'r', newline='', encoding='UTF-8') as file:
        reader = csv.reader(file)
        for i in reader:
            print(' | '.join(i))


def find_text_in_csv():
    global name_file_csv
    filedir = os.path.abspath(name_file_csv)
    with open(filedir, 'r', newline='', encoding='UTF-8') as file:
        reader = csv.reader(file)
        text = input('Введите данные для поиска заметки(id или название заметки): ')
        for i in reader:
            if text in str(i).lower():
                print(' | '.join(i))


def change_text_in_cvs():
    filedir = os.path.abspath(name_file_csv)

    read_csv()
    with open(filedir, 'r', newline='', encoding='UTF-8') as file:
        reader = csv.reader(file)
        find_id = input('Введите id заметки для изменения: ')
        temp = None
        for j in reader:
            for f_id in j:
                if f_id == find_id and f_id == j[0]:
                    temp = j
        print(temp)
        while True:
            print('Выберите поле для изменения:\n'
                  'Введите 1 - Для изм. названия\n'
                  'Введите 2 - Для изм. текста\n'
                  'Введите 0 - Для выхода в главное меню'
                  )
            num = input()
            if num == '1':
                print('Старое название:', temp[1])
                new_main = input('Введите новое название: ')
                temp.pop(1)
                temp.insert(1, new_main)
                delete_in_cvs(find_id)
                with open(filedir, 'a', newline='', encoding='UTF-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(temp)
            elif num == '2':
                print('Старый текст:', temp[2])
                new_text = input('Введите новый текст ')
                temp.pop(2)
                temp.insert(2, new_text)
                delete_in_cvs(find_id)
                with open(filedir, 'a', newline='', encoding='UTF-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(temp)
            elif num == '0':
                break
            else:
                print('Неверный ввод')


def delete_in_cvs(find_id):
    filedir = os.path.abspath(name_file_csv)
    tempfile = NamedTemporaryFile('w+t', newline='', delete=False,
                                  encoding='UTF-8')  # cоздает временный именной файл для записи
    with open(filedir, 'r', newline='', encoding='UTF-8') as file, tempfile:  # тут открываем два файла сsv и времменый
        reader = csv.reader(file)  # на чтение передаем цсв
        writer = csv.writer(tempfile)  # на запись передаем времменый
        for j in reader:
            if find_id == j[0]:  # если айди совпадают, то прпускаем, все остальное записываем
                continue
            else:
                writer.writerow(j)  # записываем строки с другими айди
    shutil.move(tempfile.name, filedir)  # производим замену временного файла на основной


def open_csv():
    global name_file_csv, dic_csv_file
    if len(get_listFile_csv()) == 0:
        print('В директории программы нет фаqлов csv!')
    else:
        dic_csv_file = dict((str(ind), val) for ind, val in enumerate(get_listFile_csv(),1))
    for i in dic_csv_file.items():
        print(f'№ {i[0]} - {i[1]}')
    select_file = input('Выберите файл и введите его номер: ')
    try:
        name_file_csv = dic_csv_file.pop(select_file)
    except:
        print('Ошибка')


def change_data():
    with open(name_file_csv, 'r', newline='', encoding='UTF-8') as file:
        reader = csv.reader(file)
        dict_data = dict((*i[-1:], i) for i in reader)
        user_data = input('Введите дату заметки (число.месяц.год) : ')
        print('id', 'Название заметки', 'Текст заметки', 'Дата создания', sep=' | ')
        for key, value in dict_data.items():
            if user_data in key:
                print(' | '.join(value))


def main_menu():
    if len(get_listFile_csv()) == 0:
        first_file()
        open_csv()
    while True:
        print('Выберите режим работы Заметок:\n'
              'Введите "open" - для открытия сторонего файла(из рабочей директории)\n'
              'Введите 1 - Для записи данных\n'
              'Введите 2 - Для отображения всех данных\n'
              'Введите 3 - Для поиска данных\n'
              'Введите 4 - Для изменения данных\n'
              'Введите 5 - Для удалению данных\n'
              'Введите 6 - Для выборки по дате\n'
              'Введите 0 - Для выхода из программы\n')
        num = input()
        if num == '1':
            add_new_note()
        elif num == '2':
            read_csv()
        elif num == 'open':
            open_csv()
        elif num == '3':
            find_text_in_csv()
        elif num == '4':
            change_text_in_cvs()
        elif num == '6':
            change_data()
        elif num == '5':
            read_csv()
            find_id = input('Введите id заметки для удаления: ')
            delete_in_cvs(find_id)
        elif num == '0':
            quit()
        else:
            print('Неверный ввод')



main_menu()

