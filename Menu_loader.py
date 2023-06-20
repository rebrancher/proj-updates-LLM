class MenuLoader:
    def __init__(self, options):
        self.options = options

    def display(self):
        for key, value in self.options.items():
            print(f"{key}. {value['title']}")

    def select_option(self):
        self.display()
        option = input("Choose your option: ")
        if option in self.options:
            return self.options[option]['function']
        else:
            print("Invalid option.")
            return None

