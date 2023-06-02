import os

def handle_quit_command():
    return False

def handle_up_command(current_directory):
    return os.path.dirname(current_directory), 0, 0

def handle_next_command(page_dirs, page_files):
    return page_dirs + 1, page_files

def handle_previous_command(page_dirs, page_files):
    return max(0, page_dirs - 1), max(0, page_files - 1)

def handle_copy_command(files, page_files, paginated_directories):
    print("Enter the file number to copy:")
    file_index = int(input("> "))
    print("Enter the destination directory:")
    destination_directory = input("> ")
    copy_file(file_index - len(paginated_directories), files, page_files, destination_directory)

def handle_digit_command(user_input, directories, files, page_dirs, page_files, paginated_directories):
    if 0 <= user_input < len(paginated_directories):
        new_directory = process_directory_input(user_input, directories, page_dirs)
        if new_directory is not None:
            return new_directory, 0, 0
    elif user_input < len(paginated_files) + len(paginated_directories):
        process_file_input(user_input - len(paginated_directories), files, page_files)
    else:
        print("Invalid input, please try again")
    return None

def handle_user_input(current_directory, page_dirs, page_files, directories, files, paginated_directories, paginated_files):
    print("Enter a directory number to navigate, a file number to read its first 200 characters, 'u' to go up a directory, 'n' to next page, 'p' to previous page, 'c' to copy a file, or 'q' to quit")
    user_input = input("> ")

    if user_input.lower() == 'q':
        return handle_quit_command()
    elif user_input.lower() == 'u':
        return handle_up_command(current_directory)
    elif user_input.lower() == 'n':
        return current_directory, *handle_next_command(page_dirs, page_files)
    elif user_input.lower() == 'p':
        return current_directory, *handle_previous_command(page_dirs, page_files)
    elif user_input.lower() == 'c':
        handle_copy_command(files, page_files, paginated_directories)
        return current_directory, page_dirs, page_files
    elif user_input.isdigit():
        user_input = int(user_input)
        result = handle_digit_command(user_input, directories, files, page_dirs, page_files, paginated_directories)
        if result is not None:
            return result
        else:
            return current_directory, page_dirs, page_files
    else:
        print("Invalid input, please try again")
        return current_directory, page_dirs, page_files
