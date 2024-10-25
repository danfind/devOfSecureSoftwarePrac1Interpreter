import os
import json
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
import shutil
import psutil

# Информация о логических дисках
def display_drive_info():
    print("Информация о логических дисках:")
    for partition in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            print(f"Диск: {partition.device}")
            print(f"Тип файловой системы: {partition.fstype}")
            print(f"Размер: {usage.total / (1024 ** 3):.2f} GB")
            print(f"Использовано: {usage.used / (1024 ** 3):.2f} GB")
            print(f"Доступно: {usage.free / (1024 ** 3):.2f} GB")
            print(f"Метка тома: {partition.mountpoint}")
            print("-" * 30)
        except PermissionError:
            print(f"Нет доступа к {partition.device}")

# Работа с файлами
def create_file(filename):
    Path(filename).with_suffix('.txt').touch()
    print(f"Файл {filename}.txt создан.")

def write_to_file(filename, text):
    filename = Path(filename).with_suffix('.txt')
    with open(filename, 'w') as f:
        f.write(text)
    print(f"Текст записан в {filename}.")

def read_file(filename):
    filename = Path(filename).with_suffix('.txt')
    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        with open(filename, 'r') as f:
            print(f"Содержимое {filename}:")
            print(f.read())
    else:
        print(f"Файл {filename} пуст или не найден.")

def delete_file(filename):
    filename = Path(filename).with_suffix('.txt')
    if os.path.exists(filename):
        os.remove(filename)
        print(f"Файл {filename} удален.")
    else:
        print(f"Файл {filename} не найден.")

# Работа с JSON
def create_json_file(filename, data):
    filename = Path(filename).with_suffix('.json')
    with open(filename, 'w') as f:
        json.dump([data], f, indent=4)
    print(f"JSON файл {filename} создан.")

def read_json_file(filename):
    filename = Path(filename).with_suffix('.json')
    if os.path.exists(filename):
        if os.path.getsize(filename) > 0:
            with open(filename, 'r') as f:
                print(f"Содержимое JSON файла {filename}:")
                print(json.load(f))
        else:
            print(f"Файл {filename} пуст.")
    else:
        print(f"Файл {filename} не найден.")

def add_object_to_json(filename, name, age):
    filename = Path(filename).with_suffix('.json')
    data = []

    if filename.exists() and os.path.getsize(filename) > 0:
        with open(filename, 'r') as f:
            try:
                data = json.load(f)
                if not isinstance(data, list):
                    data = [data]
            except json.JSONDecodeError:
                print(f"Ошибка при чтении JSON файла {filename}. Файл может быть поврежден.")
                return

    data.append({"name": name, "age": age})

    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Объект добавлен в JSON файл {filename}.")

def delete_json_file(filename):
    filename = Path(filename).with_suffix('.json')
    if os.path.exists(filename):
        os.remove(filename)
        print(f"JSON файл {filename} удален.")
    else:
        print(f"JSON файл {filename} не найден.")

# Работа с XML
def create_xml_file(filename):
    filename = Path(filename).with_suffix('.xml')
    root = ET.Element("users")
    tree = ET.ElementTree(root)
    tree.write(filename)
    print(f"XML файл {filename} создан.")

def write_to_xml_file(filename, name, age):
    filename = Path(filename).with_suffix('.xml')
    if os.path.exists(filename):
        tree = ET.parse(filename)
        root = tree.getroot()
        user = ET.SubElement(root, "user")
        ET.SubElement(user, "name").text = name
        ET.SubElement(user, "age").text = str(age)
        tree.write(filename)
        print("Данные добавлены в XML файл.")
    else:
        print(f"Файл {filename} не найден.")

def read_xml_file(filename):
    filename = Path(filename).with_suffix('.xml')
    if os.path.exists(filename):
        tree = ET.parse(filename)
        root = tree.getroot()
        print(f"Содержимое XML файла {filename}:")
        for user in root.findall("user"):
            name = user.find("name").text
            age = user.find("age").text
            print(f"Имя: {name}, Возраст: {age}")
    else:
        print(f"Файл {filename} не найден.")

def delete_xml_file(filename):
    filename = Path(filename).with_suffix('.xml')
    if os.path.exists(filename):
        os.remove(filename)
        print(f"XML файл {filename} удален.")
    else:
        print(f"XML файл {filename} не найден.")

# Работа с ZIP
def create_zip_file(zip_filename):
    zip_filename = Path(zip_filename).with_suffix('.zip')
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        print(f"ZIP архив {zip_filename} создан.")

def add_file_to_zip(zip_filename, filename_to_add):
    zip_filename = Path(zip_filename).with_suffix('.zip')
    filename_to_add = Path(filename_to_add)
    if os.path.exists(filename_to_add):
        with zipfile.ZipFile(zip_filename, 'a') as zipf:
            zipf.write(filename_to_add, filename_to_add.name)
        print(f"Файл {filename_to_add} добавлен в архив {zip_filename}. Размер архива: {os.path.getsize(zip_filename)} байт")
    else:
        print(f"Файл {filename_to_add} не найден.")

def extract_zip_file(zip_filename, extract_to='.'):
    zip_filename = Path(zip_filename).with_suffix('.zip')
    if os.path.exists(zip_filename):
        try:
            with zipfile.ZipFile(zip_filename, 'r') as zipf:
                zipf.extractall(extract_to)
                print(f"Файлы из архива {zip_filename} извлечены в {extract_to}.")
                print("Содержимое архива:")
                for file in zipf.namelist():
                    print(file)
        except zipfile.BadZipFile:
            print(f"Ошибка: файл {zip_filename} не является корректным ZIP архивом.")
        except Exception as e:
            print(f"Произошла ошибка при извлечении: {e}")
    else:
        print(f"Архив {zip_filename} не найден.")

def delete_zip_file(zip_filename):
    zip_filename = Path(zip_filename).with_suffix('.zip')
    if os.path.exists(zip_filename):
        os.remove(zip_filename)
        print(f"ZIP архив {zip_filename} удален.")
    else:
        print(f"ZIP архив {zip_filename} не найден.")

# Главная функция с меню
def main():
    while True:
        print("\nВыберите действие:")
        print("1. Информация о дисках")
        print("2. Работа с файлами")
        print("3. Работа с JSON")
        print("4. Работа с XML")
        print("5. Работа с ZIP")
        print("6. Выход")
        choice = input("Введите номер действия: ")

        if choice == '1':
            display_drive_info()

        elif choice == '2':
            filename = input("Введите имя файла: ")
            print("a. Создать файл")
            print("b. Записать в файл")
            print("c. Прочитать файл")
            print("d. Удалить файл")
            file_choice = input("Выберите операцию: ")

            if file_choice == 'a':
                create_file(filename)
            elif file_choice == 'b':
                text = input("Введите текст для записи: ")
                write_to_file(filename, text)
            elif file_choice == 'c':
                read_file(filename)
            elif file_choice == 'd':
                delete_file(filename)
            else:
                print("Неверный ввод")

        elif choice == '3':
            json_filename = input("Введите имя JSON файла: ")
            print("a. Создать JSON файл")
            print("b. Прочитать JSON файл")
            print("c. Добавить объект в JSON файл")
            print("d. Удалить JSON файл")
            json_choice = input("Выберите операцию: ")

            if json_choice == 'a':
                name = input("Введите имя пользователя: ")
                age = int(input("Введите возраст пользователя: "))
                create_json_file(json_filename, {"name": name, "age": age})
            elif json_choice == 'b':
                read_json_file(json_filename)
            elif json_choice == 'c':
                name = input("Введите имя пользователя: ")
                age = int(input("Введите возраст пользователя: "))
                add_object_to_json(json_filename, name, age)
            elif json_choice == 'd':
                delete_json_file(json_filename)
            else:
                print("Неверный ввод")


        elif choice == '4':
            xml_filename = input("Введите имя XML файла: ")
            print("a. Создать XML файл")
            print("b. Добавить данные в XML файл")
            print("c. Прочитать XML файл")
            print("d. Удалить XML файл")
            xml_choice = input("Выберите операцию: ")

            if xml_choice == 'a':
                create_xml_file(xml_filename)
            elif xml_choice == 'b':
                name = input("Введите имя пользователя: ")
                age = input("Введите возраст пользователя: ")
                write_to_xml_file(xml_filename, name, age)
            elif xml_choice == 'c':
                read_xml_file(xml_filename)
            elif xml_choice == 'd':
                delete_xml_file(xml_filename)
            else:
                print("Неверный ввод")


        elif choice == '5':
            zip_filename = input("Введите имя ZIP архива: ")
            print("a. Создать ZIP архив")
            print("b. Добавить файл в ZIP архив")
            print("c. Извлечь файлы из ZIP архива")
            print("d. Удалить ZIP архив")
            zip_choice = input("Выберите операцию: ")

            if zip_choice == 'a':
                create_zip_file(zip_filename)
            elif zip_choice == 'b':
                filename_to_add = input("Введите имя файла для добавления в архив: ")
                add_file_to_zip(zip_filename, filename_to_add)
            elif zip_choice == 'c':
                extract_zip_file(zip_filename)
            elif zip_choice == 'd':
                delete_zip_file(zip_filename)
            else:
                print("Неверный ввод")

        elif choice == '6':
            print("Выход из программы.")
            break
        else:
            print("Неверный ввод")

if __name__ == "__main__":
    main()
