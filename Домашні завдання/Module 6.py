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
                   'video':        ['AVI', 'MP4', 'MOV', 'MKV'],
                   'documents':    ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'],
                   'audio':        ['MP3', 'OGG', 'WAV', 'AMR'],
                   'archives':     ['ZIP', 'GZ', 'TAR'],
                   'others':       []
                   }

# -------------- функція для нормалізації імені файлу ------------------


def normalize_name(name) -> str:
    TRANS_DICT = {}
    for i, j in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS_DICT[ord(i)] = j
        TRANS_DICT[ord(i.upper())] = j.upper()
    asc2_name = name.translate(TRANS_DICT)
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

 # функція  яка шукає і повертає рядок, який в вказує на тип файла та на каталог в який знайдений файл буде переміщений


def find_type_of_file(extention: str) -> str:
    extention = extention[1:]
    founded: str = None
    for type_of_file in LIST_OF_FOLDERS:
        if extention.upper() in LIST_OF_FOLDERS[type_of_file]:
            founded = str(type_of_file)
    if not founded:
        founded = 'others'
    return founded


def sort_files_in_directory(source_path) -> bool:
    # шукаємо все, що є в каталогу (файли + вкладені каталоги)
    list_of_files_in_directory = os.listdir(source_path)
    # якщо папка пуста, виходимо з поточної папки, якщо це верхній рівень, то виходимо з программи
    if not list_of_files_in_directory:
        return True
    for current_item in list_of_files_in_directory:
        full_path_current_item = source_path + current_item
        # блок якщо в нас файл
        if os.path.isfile(full_path_current_item):
            # отримуємо окремо назву файла та його розширення
            name_current_item = os.path.splitext(current_item)[0]
            extention_current_item = os.path.splitext(current_item)[1]
            # будуємо шлях до новго каталога на основі типу файла якого ми переміщаємо
            destination_path_current_item = PATH_TO_SORTED_DIRECTORY + \
                find_type_of_file(extention_current_item) + '/'
            # нормалізуємо імʼя файла
            name_of_file_normalized = normalize_name(
                name_current_item) + extention_current_item
            # якщо файл це архів, то розрхівовуємо його в папці для архівів
            if extention_current_item[1:].upper() in LIST_OF_FOLDERS['archives']:
                if not os.path.exists(destination_path_current_item + normalize_name(name_current_item)):
                    os.mkdir(destination_path_current_item +
                             normalize_name(name_current_item))
                try:
                    shutil.unpack_archive(
                        source_path + current_item, destination_path_current_item + normalize_name(name_current_item))
                except shutil.ReadError:
                    print('{} архів не є архівом, або він пошкоджений'.format(
                        current_item))
                else:
                    os.remove(source_path + current_item)
                continue

            # переносимо файл з нормалізованою назвою в папку для файлів такого типу
            os.replace(source_path + current_item,
                       destination_path_current_item + name_of_file_normalized)

        # якщо в нас каталог, то ми рекурсивно викликаємо функцію sort_files_in_dictionary і передаємо знайдений каталог як агрумент
        if os.path.isdir(full_path_current_item):
            print(full_path_current_item)
            sort_files_in_directory(full_path_current_item + '/')
            shutil.rmtree(full_path_current_item)
    return True


if __name__ == '__main__':
    check_folders_exists()
    if sort_files_in_directory(PATH_TO_UNSORTED_DIRECTORY):
        print('Done')

# Продивитись else ;
