import os

# Define a constant for the number of items per page
ITEMS_PER_PAGE = 10

def list_files(directory):
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

def list_dirs(directory):
    return [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]

def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            print(file.read(200))
            print("\nDo you want to read the rest of this file? (y/n)")
            user_input = input(">")
            if user_input.lower() == 'y':
                print(file.read())
                print("\nPress M to go back to the main menu")
                user_input = input(">")
                if user_input.lower() == 'm':
                    return

            elif user_input.lower() == 'n':
                return
            else:
                print("Invalid input, please try again")
    except Exception as e:
        print(f"Failed to read file: {e}")

# Function to get a paginated list
def get_paginated_list(items, page):
    # Calculate the start and end indices for slicing the list
    start_index = page * ITEMS_PER_PAGE
    end_index = start_index + ITEMS_PER_PAGE
    return items[start_index:end_index]

# Function to get an item by its index in the paginated list
def get_item_by_index(items, page, index):
    paginated_items = get_paginated_list(items, page)
    if index < len(paginated_items):
        return paginated_items[index]
    else:
        return None


def print_directory_files(files, directories, page_files, page_dirs):
    paginated_directories = get_paginated_list(directories, page_dirs)
    paginated_files = get_paginated_list(files, page_files)

    print('\n' + '-' * 60)
    print(f"Current directory: {os.getcwd()}\n")
    print("Directories:")
    for i, directory in enumerate(paginated_directories):
        print(f"  {i}. {directory}")
    
    print("\nFiles in:")
    for i, file in enumerate(paginated_files):
        print(f"  {i}. {file}")

    print('\n' + '-' * 60)

def handle_user_input(user_input, directories, files, current_directory, page_dirs, page_files):
    if user_input.lower() == 'q':
        return False, current_directory, page_dirs, page_files
    elif user_input.lower() == 'u':
        current_directory = os.path.dirname(current_directory)
    elif user_input.lower() == 'n':
        page_dirs, page_files = go_to_next_page(directories, files, page_dirs, page_files)
    elif user_input.lower() == 'p':
        page_dirs, page_files = go_to_previous_page(directories, files, page_dirs, page_files)
    elif user_input.isdigit():
        user_input = int(user_input)
        current_directory = handle_digit_input(directories, files, user_input, current_directory, page_dirs, page_files)
    elif user_input.lower() == 'w':
        write_new_file(current_directory)
    elif user_input.lower() == 'r':
        print("Enter the name of the file you want to read:")
        filename = input(">")
        filepath = os.path.join(current_directory, filename)
        if os.path.exists(filepath):
            read_file(filepath)
        else:
            print(f"File {filename} does not exist in this directory.")
    else:
        print("Invalid input, please try again")
    return True, current_directory, page_dirs, page_files

def go_to_next_page(directories, files, page_dirs, page_files):
    if page_dirs < len(directories) / ITEMS_PER_PAGE:
        page_dirs += 1
    if page_files < len(files) / ITEMS_PER_PAGE:
        page_files += 1
    return page_dirs, page_files

def go_to_previous_page(directories, files, page_dirs, page_files):
    if page_dirs > 0:
        page_dirs -= 1
    if page_files > 0:
        page_files -= 1
    return page_dirs, page_files

def handle_digit_input(directories, files, user_input, current_directory, page_dirs, page_files):
    paginated_directories = get_paginated_list(directories, page_dirs)
    paginated_files = get_paginated_list(files, page_files)
    if 0 <= user_input < ITEMS_PER_PAGE:
        if user_input < len(paginated_directories):
            current_directory = os.path.join(current_directory, get_item_by_index(directories, page_dirs, user_input))
        elif user_input < len(paginated_files) + len(paginated_directories):
            read_file(os.path.join(current_directory, get_item_by_index(files, page_files, user_input - len(paginated_directories))))
        else:
            print("Invalid input, please try again")
    else:
        print("Invalid input, please try again")
    return current_directory

def write_new_file(current_directory):
    filename = input("Enter the name of the new file: ")
    filepath = os.path.join(current_directory, filename)
    if os.path.exists(filepath):
        print(f"A file named {filename} already exists in this directory.")
        return
    content = input("Enter the content for the new file: ")
    try:
        with open(filepath, 'w') as file:
            file.write(content)
        print(f"New file {filename} has been created.")
    except Exception as e:
        print(f"Failed to create file: {e}")

def main():
    continue_loop = True
    current_directory = os.getcwd()
    page_dirs = page_files = 0
    while continue_loop:
        files = list_files(current_directory)
        directories = list_dirs(current_directory)
        print_directory_files(files, directories, page_files, page_dirs)
        print("Enter a directory number to navigate, a file number to read its first 200 characters, 'u' to go up a directory, 'n' to next page, 'p' to previous page, or 'q' to quit")
        user_input = input("> ")
        continue_loop, current_directory, page_dirs, page_files = handle_user_input(user_input, directories, files, current_directory, page_dirs, page_files)

if __name__ == "__main__":
    main()