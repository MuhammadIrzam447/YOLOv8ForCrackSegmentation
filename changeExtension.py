import os
import shutil


def change_extension(directory):
    file_list = []

    # Traverse the directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.isfile(file_path):  # Check if it's a file
                # Change the extension from .jpg to .png
                new_file_path = os.path.splitext(file_path)[0] + '.png'
                # Rename the file
                shutil.move(file_path, new_file_path)
                file_list.append(new_file_path)

    return file_list



directory = "/share/hel/home/muhammad-liaqat/crackandpot/masks/"

file_list = change_extension(directory)
print("Files renamed:")
for file_path in file_list:
    print(file_path)
