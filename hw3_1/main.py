import os
import shutil
import patoolib
from concurrent.futures import ThreadPoolExecutor


CATEGORIES = {"Pictures": ['.jpeg', '.png', '.jpg', '.svg'],
              "Video": ['.avi', '.mp4', '.mov', '.mkv'],
              "Documents": ['.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx'],
              "Music": ['.mp3', '.ogg', '.wav', '.amr'],
              "Archive": ['.zip', '.gz', '.tar']}


# Функція для отримання списку файлів у папці та її підкаталогах
def list_files(folder):
    file_list = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            file_list.append(os.path.join(root, file))
    return file_list


# Функція для переміщення файлів в папки за категоріями
def move_files_by_category(files, target_folder):
    for file in files:
        _, extension = os.path.splitext(file)
        extension = extension.lower()
        for category, extensions in CATEGORIES.items():
            if extension in extensions:
                category_folder = os.path.join(target_folder, category)
                os.makedirs(category_folder, exist_ok=True)
                shutil.move(file, os.path.join(category_folder, os.path.basename(file)))
                break


# Функція для розархівування архівів в окрему папку
def extract_archives(archive_folder):
    for root, dirs, files in os.walk(archive_folder):
        for file in files:
            _, extension = os.path.splitext(file)
            extension = extension.lower()
            if extension in CATEGORIES["Archive"]:
                archive_path = os.path.join(root, file)
                target_directory = os.path.join(archive_folder, os.path.splitext(file)[0])
                os.makedirs(target_directory, exist_ok=True)
                patoolib.extract_archive(archive_path, outdir=target_directory)


# Функція для видалення порожніх папок
def remove_empty_folders(folder):
    for root, dirs, files in os.walk(folder, topdown=False):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            if not os.listdir(dir_path):
                os.rmdir(dir_path)


# Функція для обробки папки та сортування файлів
def process_folder(folder):
    files = list_files(folder)
    move_files_by_category(files, folder)
    extract_archives(folder)
    remove_empty_folders(folder)

    for category, extensions in CATEGORIES.items():
        category_files = [file for file in files if os.path.splitext(file)[1].lower() in extensions]
        print(f"{category}: {len(category_files)} файлів")


if __name__ == "__main__":
    folder_path = input("Введіть повний шлях до папки яку треба сортувати: ")
    num_threads = 4  # Кількість потоків для обробки

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        executor.submit(process_folder, folder_path)
