import os
import sys
import re
import argparse
import uuid

# USAGE:
# python3 projectRename.py -d "originalProjectDirectory" -f "originalProjectDirectory" -r "newProjectName"
# note the second reference to originalProjectDirectory is the project name
# this program will make a new directory

_ignored_directory_names = [".vs", ".git", ".svn"]
_replace_in_files_count = 0
_replace_in_file_names_count = 0
_replace_in_directory_names_count = 0

def replace_last_occurrence(source, find_text, replace_text):
    start_index = source.rfind(find_text)
    return source[:start_index] + replace_text + source[start_index + len(find_text):]

def replace_in_files(directory_path, find_text, replace_text, delete_vs_user_settings_directory):
    global _replace_in_files_count

    if delete_vs_user_settings_directory and os.path.basename(directory_path) in _ignored_directory_names:
        return

    for file in os.listdir(directory_path):
        file_path = os.path.join(directory_path, file)
        if os.path.isfile(file_path):
            try:
                with open(file_path, 'r') as f:
                    file_text = f.read()
                count = len(re.findall(find_text, file_text))
                if count > 0:
                    contents = file_text.replace(find_text, replace_text)
                    with open(file_path, 'w') as f:
                        f.write(contents)
                    _replace_in_files_count += count
            except UnicodeDecodeError:
                print(f"Skipping file '{file_path}' due to decoding error.")
        elif os.path.isdir(file_path):
            replace_in_files(file_path, find_text, replace_text, delete_vs_user_settings_directory)

def replace_in_file_names(directory_path, find_text, replace_text, delete_vs_user_settings_directory):
    global _replace_in_file_names_count

    if delete_vs_user_settings_directory and os.path.basename(directory_path) in _ignored_directory_names:
        return

    for file in os.listdir(directory_path):
        file_path = os.path.join(directory_path, file)
        if os.path.isfile(file_path):
            count = len(re.findall(find_text, file))
            if count > 0:
                new_file_name = file.replace(find_text, replace_text)
                original_file_name = file
                if new_file_name.lower() == original_file_name.lower():
                    temp_file_name = f"temp_{original_file_name}_{uuid.uuid4()}"
                    temp_full_file_name = replace_last_occurrence(file_path, file, temp_file_name)
                    os.rename(file_path, temp_full_file_name)
                    new_full_file_name = replace_last_occurrence(file_path, file, new_file_name)
                    os.rename(temp_full_file_name, new_full_file_name)
                else:
                    new_full_file_name = replace_last_occurrence(file_path, file, new_file_name)
                    os.rename(file_path, new_full_file_name)
                _replace_in_file_names_count += count
        elif os.path.isdir(file_path):
            replace_in_file_names(file_path, find_text, replace_text, delete_vs_user_settings_directory)

def replace_in_directory_names(directory_path, find_text, replace_text, delete_vs_user_settings_directory):
    global _replace_in_directory_names_count

    if delete_vs_user_settings_directory and os.path.basename(directory_path) in _ignored_directory_names:
        return

    count = len(re.findall(find_text, os.path.basename(directory_path)))

    directory_info_full_name = directory_path

    if count > 0:
        new_directory_name = os.path.basename(directory_path).replace(find_text, replace_text)
        original_directory_name = os.path.basename(directory_path)
        if new_directory_name.lower() == original_directory_name.lower():
            temp_directory_name = f"temp_{original_directory_name}_{uuid.uuid4()}"
            temp_full_directory_name = replace_last_occurrence(directory_path, os.path.basename(directory_path), temp_directory_name)
            os.rename(directory_path, temp_full_directory_name)
            new_full_directory_name = replace_last_occurrence(directory_path, os.path.basename(directory_path), new_directory_name)
            os.rename(temp_full_directory_name, new_full_directory_name)
        else:
            directory_info_full_name = replace_last_occurrence(directory_path, os.path.basename(directory_path), new_directory_name)
            os.rename(directory_path, directory_info_full_name)
        _replace_in_directory_names_count += count

    for directory in os.listdir(directory_info_full_name):
        sub_directory_path = os.path.join(directory_info_full_name, directory)
        if os.path.isdir(sub_directory_path):
            replace_in_directory_names(sub_directory_path, find_text, replace_text, delete_vs_user_settings_directory)

def main(args):
    ignored_folders = ', '.join([f"'{name}'" for name in _ignored_directory_names])
    print(f"This application is best run with administrator privileges. Directories with the following names will be ignored to try and prevent access / corruption issues: {ignored_folders}")

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--directory-path', required=False, help="Directory path")
    parser.add_argument('-f', '--find-text', required=False, help="Find text")
    parser.add_argument('-r', '--replace-text', required=False, help="Replace text")
    opts = parser.parse_args(args)

    directory_path = opts.directory_path
    find_text = opts.find_text
    replace_text = opts.replace_text

    if not directory_path:
        directory_path = input("\nEnter root directory path: ")
    else:
        print(f"\nRoot directory path: {directory_path}")

    if not find_text:
        find_text = input("\nEnter find text (case sensitive): ")
    else:
        print(f"\nFind text: {find_text}")

    if not replace_text:
        replace_text = input("\nEnter replace text (case sensitive): ")
    else:
        print(f"\nReplace text: {replace_text}")

    print("\nWorking...")

    replace_in_files(directory_path, find_text, replace_text, delete_vs_user_settings_directory=True)
    replace_in_file_names(directory_path, find_text, replace_text, delete_vs_user_settings_directory=True)
    replace_in_directory_names(directory_path, find_text, replace_text, delete_vs_user_settings_directory=True)

    print("\nFinished.")
    print(f"Replaced {_replace_in_files_count} occurrences in files")
    print(f"Replaced {_replace_in_file_names_count} occurrences in file names")
    print(f"Replaced {_replace_in_directory_names_count} occurrences in directory names")
    print()

if __name__ == "__main__":
    main(sys.argv[1:])
