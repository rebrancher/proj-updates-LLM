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
            while True:
                print("\nDo you want to continue reading this file? (y/n)")
                user_input = input(">")
                if user_input.lower() == 'y':
                    print(file.read(200))
                elif user_input.lower() == 'n':
                    break
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

def main():
    current_directory = os.getcwd()
    page_dirs = page_files = 0
    while True:
        files = list_files(current_directory)
        directories = list_dirs(current_directory)

        paginated_directories = get_paginated_list(directories, page_dirs)
        paginated_files = get_paginated_list(files, page_files)

        print('\n' + '-' * 60)  # Line for separating sections
        print(f"Current directory: {current_directory}\n")

        print("Directories:")
        for i, directory in enumerate(paginated_directories):
            print(f"  {i}. {directory}")
        
        print("\nFiles:")
        for i, file in enumerate(paginated_files):
            print(f"  {i}. {file}")
        
        print('\n' + '-' * 60)  # Line for separating sections
        print("Enter a directory number to navigate, a file number to read its first 200 characters, 'u' to go up a directory, 'n' to next page, 'p' to previous page, or 'q' to quit")
        user_input = input("> ")


        if user_input.lower() == 'q':
            break
        elif user_input.lower() == 'u':
            current_directory = os.path.dirname(current_directory)
        elif user_input.lower() == 'n':
            # If user input is 'n', go to the next page
            if page_dirs < len(directories) / ITEMS_PER_PAGE:
                page_dirs += 1
            if page_files < len(files) / ITEMS_PER_PAGE:
                page_files += 1
        elif user_input.lower() == 'p':
            # If user input is 'p', go to the previous page
            if page_dirs > 0:
                page_dirs -= 1
            if page_files > 0:
                page_files -= 1
        elif user_input.isdigit():
            user_input = int(user_input)
            if 0 <= user_input < ITEMS_PER_PAGE:
                if user_input < len(paginated_directories):
                    current_directory = os.path.join(current_directory, get_item_by_index(directories, page_dirs, user_input))
                elif user_input < len(paginated_files) + len(paginated_directories):
                    read_file(os.path.join(current_directory, get_item_by_index(files, page_files, user_input - len(paginated_directories))))
                else:
                    print("Invalid input, please try again")
            else:
                print("Invalid input, please try again")
        else:
            print("Invalid input, please try again")

if __name__ == "__main__":
    main()



#print(list_files('/Users/hamad/Downloads'))