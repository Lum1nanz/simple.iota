
from InputHelper import convert_input_to_int
from UserManager import UserManager
from getpass import getpass

from Wallet import Wallet

class Client:
    def __init__(self) -> None:
        self.usermanager = UserManager()
    
    def print_menu(self):
        print("")
        print("Choose one of the following tasks:")
        print("[1] - List of all Users")
        print("[2] - Login into one User")
        print("[3] - Add new User to Client")
        print("[4] - Remove User from Client")
        print("[9] - Exit the Client")
        
    def check_choice(self, menu_choice):
        if menu_choice == 1:
            self.print_all_users()
            return
        if menu_choice == 2:
            username = self.login()
            wallet = Wallet(username)
            wallet.run()
            return
        if menu_choice == 3:
            self.create_new_user()
            return
        if menu_choice == 9:
            return
        print("Invalid Choice!")
    
    def print_all_users(self):
        users = self.usermanager.get_all_users()
        print("--- 🙋 Userlist 🙋 ---")
        if len(users) == 0:
            print("Nothing to see here...")
        count = 1
        for user in users:
            print(f"{count} - {user.name}")
            count = count + 1
    
    def create_new_user(self):
        username = self.get_username_from_cli()
        
        password = self.get_password_from_cli()
        
        self.usermanager.add_user(username, password)
        print(f"New user {username} added.")

    def get_username_from_cli(self):
        username = input("Username: ")
        user_exists = self.usermanager.user_exists(username)
        while user_exists:
            print("Error! Username already exists!\nChoose a different one...")
            username = input("Username: ")
            user_exists = self.usermanager.user_exists(username)
        return username

    def get_password_from_cli(self):
        password = getpass("Password: ")
        password_confirm = getpass("Re-Enter Password: ")
        while password != password_confirm:
            print("Passwords don't match! Try again...")
            password = getpass("Password: ")
            password_confirm = getpass("Re-Enter Password: ")
        return password

    def login(self) -> str:
        self.print_all_users()
        user_choice = convert_input_to_int(input("Choose the number of user you want to login into: "))
        while not 0 < user_choice <= len(self.usermanager.get_all_users()):
            print("Invalid User-Choice!")
            self.print_all_users()
            user_choice = convert_input_to_int(input("Choose the number of user you want to login into: "))
        
        username = self.usermanager.get_username_by_index(user_choice - 1)

        password = getpass("Password: ")
        password_match = self.usermanager.login(username, password)
        while not password_match:
            print("Invalid Password! Try again...")
            password = getpass("Password: ")
            password_match = self.usermanager.login(username, password)
        
        print("Login Successful!")
        return username

    def run(self):
        menu_choice = 0
        print("Welcome to simple.iota!")
        while menu_choice != 9:
            self.print_menu()
            menu_choice = convert_input_to_int(input("> "))
            self.check_choice(menu_choice)
        
        print("See ya...👋")

