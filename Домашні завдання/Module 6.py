import string
import sys
import os
import shutil

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
PATH_TO_SORTED_DIRECTORY = '/Users/anatoliysafonov/Desktop/sorted/'
PATH_TO_UNSORTED_DIRECTORY = sys.argv[1] + '/'
print(PATH_TO_UNSORTED_DIRECTORY)
LIST_OF_FOLDERS = {'pictures':     ['JPEG', 'PNG', 'JPG', 'SVG'],
                   'video':     ['AVI', 'MP4', 'MOV', 'MKV'],
                   'documents':    ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'],
                   'audio': ['MP3', 'OGG', 'WAV', 'AMR'],
                   'archives':  ['ZIP', 'GZ', 'TAR'],
                   'others': []
                   }

# -------------- функція для нормалізації імені файлу ------------------


def normalize_name(name) -> str:
    TRANS = {}
    for i, j in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(i)] = j
        TRANS[ord(i.upper())] = j.upper()
    asc2_name = name.translate(TRANS)
    normalized_name = ''
    for char in asc2_name:
        if char in string.punctuation:
            normalized_name += '_'
        else:
            normalized_name += char
    return normalized_name

# Перевіряємо чи існуть каталоги для розміщення відсортированих файлів


def check_folders_exists():
    for folder_name in LIST_OF_FOLDERS:
        if not os.path.isdir(PATH_TO_SORTED_DIRECTORY + folder_name):
            os.mkdir(PATH_TO_SORTED_DIRECTORY + folder_name)


def sort_files_in_directory(path):

    # функція  яка шукає і повертає рядок, який в вказує на тип файла та на каталог в який знайдений файл буде переміщений
    def find_type_of_file(ext):
        ext = ext[1:]
        type_founded = None
        for type_of_file in LIST_OF_FOLDERS:
            if ext.upper() in LIST_OF_FOLDERS[type_of_file]:
                type_founded = str(type_of_file)
        if not type_founded:
            type_founded = 'others'
        return type_founded

    # шукаємо все, що є в каталогу (файли + вкладені каталоги)
    list_of_files_in_directory = os.listdir(path)

    for file in list_of_files_in_directory:
        full_path = path + file
        # блок якщо в нас файл
        if os.path.isfile(full_path):
            # отримуємо окремо назву файла та його розширення
            name_file = os.path.splitext(file)[0]
            ext = os.path.splitext(file)[1]

            # будуємо шлях до новго каталога на основі типу файла якого ми переміщаємо
            new_full_path = PATH_TO_SORTED_DIRECTORY + \
                find_type_of_file(ext) + '/'

            # нормалізуємо імʼя файла
            name_of_file_normalized = normalize_name(
                name_file) + ext

            # якщо файл це архів, то розрхівовуємо його в папці для архівів
            if ext[1:].upper() in LIST_OF_FOLDERS['archives']:
                os.mkdir(new_full_path + normalize_name(name_file))
                shutil.unpack_archive(
                    path + file, new_full_path + normalize_name(name_file))
                os.remove(path + file)
                continue

            # переносимо файл з нормалізованою назвою в папку для файлів такого типу
            print(PATH_TO_UNSORTED_DIRECTORY + file)
            print(new_full_path + name_of_file_normalized)
            os.replace(path + file,
                       new_full_path + name_of_file_normalized)

        # якщо в нас каталог, то ми рекурсивно викликаємо функцію soft_files_in_dictionary і передаємо знайдений каталог як агрумент
        if os.path.isdir(full_path):
            print(full_path)
            sort_files_in_directory(full_path + '/')
            shutil.rmtree(full_path)
    return


if __name__ == '__main__':
    check_folders_exists()
    sort_files_in_directory(PATH_TO_UNSORTED_DIRECTORY)
