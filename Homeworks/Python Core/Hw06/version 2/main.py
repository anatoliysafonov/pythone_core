from ast import arg, parse
import string
from pathlib import Path
import shutil
import argparse

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
PATH_TO_SORTED_DIRECTORY = Path('/Users/anatoliysafonov/Documents/sorted/')
PATH_TO_UNSORTED_DIRECTORY = Path('/Users/anatoliysafonov/Desktop/unsorted/')

LIST_OF_FOLDERS = {'pictures':     ['JPEG', 'PNG', 'JPG', 'SVG'],
                   'video':        ['AVI', 'MP4', 'MOV', 'MKV'],
                   'documents':    ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'],
                   'audio':        ['MP3', 'OGG', 'WAV', 'AMR'],
                   'archives':     ['ZIP', 'GZ', 'TAR'],
                   'others':       []
                   }
LOG_LIST = []
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
def check_create_folder(*args):
    for folder_name in args:
        if not folder_name.exists():
            folder_name.mkdir()


# функція яка шукає і повертає рядок, який в вказує на тип файла та на каталог в який знайдений файл буде переміщений
def find_type_of_file(file_ext: str) -> str:
    founded = None
    for type_of_file in LIST_OF_FOLDERS:
        if file_ext.upper() in LIST_OF_FOLDERS[type_of_file]:
            founded = str(type_of_file)
    if not founded:
        founded = 'others'
    return founded

def do_delete(path):
    ans = input('file {} is broken or is not archive. Delete file Y/N:'.format(path))
    if ans == 'Y' or ans == 'y':
        path.unlink()
        return True
    return False
        

def sort_folder(source_path):
    files_folders = source_path.iterdir()
    for current_file_folder in files_folders:

        if current_file_folder.is_file():
            file_ext = current_file_folder.suffix
            normalize_file_name = normalize_name(current_file_folder.stem)
            full_file_name = normalize_file_name + file_ext
            path_to_sorted_folder = PATH_TO_SORTED_DIRECTORY.joinpath(find_type_of_file(file_ext[1:]))
            path_to_sorted_file = path_to_sorted_folder.joinpath(full_file_name)
            check_create_folder(path_to_sorted_folder)
            
            if file_ext[1:].upper() in LIST_OF_FOLDERS['archives']:
                try:
                    shutil.unpack_archive(current_file_folder, path_to_sorted_folder)
                except shutil.ReadError:
                    if do_delete(current_file_folder):
                        continue
            current_file_folder.rename(path_to_sorted_file)
            continue

        if current_file_folder.is_dir():
            if current_file_folder.stem in LIST_OF_FOLDERS.keys():
                continue
            sort_folder(current_file_folder)
            current_file_folder.rmdir()
            continue


def main():
    global PATH_TO_UNSORTED_DIRECTORY
    global PATH_TO_SORTED_DIRECTORY

    parser = argparse.ArgumentParser()
    parser.add_argument('source', nargs='?', type=str, help='-> Requaired. Path to source folder')
    parser.add_argument('destination', nargs='?', type=str, help='-> Optional. Path to distanation folder')
    parser.add_argument('-l','--log', nargs='?', default=False, help='-> Output log info')
    args = parser.parse_args()
    if (not args.source) and (not args.destination):
        print('Source folder non specified.Try -h or --help for some help')
        quit()

    PATH_TO_UNSORTED_DIRECTORY = Path(args.source)
    if not args.destination:
        PATH_TO_SORTED_DIRECTORY = PATH_TO_UNSORTED_DIRECTORY
    else:
        PATH_TO_SORTED_DIRECTORY = Path(args.destination)
    
    if not PATH_TO_UNSORTED_DIRECTORY.is_dir():
        print('Source path non exists.\nChoose -h --help for some help')
        quit()

    check_create_folder(PATH_TO_SORTED_DIRECTORY)
    sort_folder(PATH_TO_UNSORTED_DIRECTORY)
    print('\nDone')


if __name__ == '__main__':
    main()
