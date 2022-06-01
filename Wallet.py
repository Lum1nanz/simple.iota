import os
import random
import string
import iota_wallet as iw

from InputHelper import convert_input_to_int

class Wallet:
    def __init__(self, username) -> None:
        self.username = username
        self.first_creation = False
        self.password_length = 32
        self.wallet_db_storage_path = 'databases'
        sh_password = self._get_stronghold_password()
        self._create_account_manager(sh_password)
        self.account = self._create_account(self.username)

    def _create_account_manager(self, sh_password: str):
        storage_path = f"./{self.wallet_db_storage_path}/{self.username}-db"
        if not os.path.exists(storage_path):
            self.first_creation = True
        self.account_manager = iw.AccountManager(storage_path=storage_path)
        self.account_manager.set_stronghold_password(sh_password)
        if self.first_creation:
            mnemonic = self.account_manager.generate_mnemonic()
            self.account_manager.store_mnemonic("Stronghold",mnemonic)
            print("########################################################")
            print("Seed generated! Make sure you save the following phrase!")
            print("########################################################")
            print(mnemonic)
        
    def _create_account(self, username: str):
        if self.first_creation:
            account_initialiser = self.account_manager.create_account(self.__get_client_options())
            account_initialiser.alias(username)

            account = account_initialiser.initialise()
            print(f"Account created inside IOTA-Wallet: {account.alias()}")
        else:
            account = self.account_manager.get_account(username)
        return account

    def _get_stronghold_password(self) -> str:
        dotenv_path = os.path.join('.env')
        if os.path.exists(dotenv_path):
            f = open(dotenv_path, 'r')
            lines = f.readlines()
            f.close()

            sh_password = ''
            for line in lines:
                if 'SH_PASSWORD=' in line:
                    helper = line.split('=',1)
                    sh_password = helper[-1]
                    sh_password = sh_password[1:-1]
                    break
            
            if sh_password is not None and len(sh_password) >= self.password_length:
                return sh_password
        
        sh_password = self._generate_stronghold_password(self.password_length)
        print("No SH_PASSWORD found in .env-file\nCreated password and saved to .env-file.\nPassword: " + sh_password)
        self._write_stronghold_password_to_env_file(sh_password, dotenv_path)
        return sh_password

    def _set_stronghold_password_env(self, password) -> None:
        os.environ["SH_PASSWORD"] = password

    def _generate_stronghold_password(self, length) -> str:
        lower = string.ascii_lowercase
        upper = string.ascii_uppercase
        numbers = string.digits
        symbols = string.punctuation
        all_chars = lower + upper + numbers + symbols
        
        gen = random.sample(all_chars, length)
        password = "".join(gen)
        
        return password
    
    def _write_stronghold_password_to_env_file(self, password: str, dotenv_path: str) -> None:
        with open(dotenv_path, 'w') as f:
            f.write("SH_PASSWORD=\"" + password + "\"")
    
    def __get_client_options(self) -> dict:
        client_options = {
            "nodes": [
                {
                    "url": "https://api.thin-hornet-0.h.chrysalis-devnet.iota.cafe",
                    "auth": None,
                    "disabled": False
                }
            ],
            "local_pow": True
        }
        return client_options

    def __synchronize(self) -> None:
        status = self.account.sync().execute()
    
    def __get_balance(self) -> dict:
        self.__synchronize()
        return self.account.balance()

    def __generate_new_address(self) -> list:
        self.__synchronize()
        return self.account.generate_address()

    def __get_address_to(self):
        to_address = input("Address of Receiver: ")
        return to_address

    def __get_transfer_amount(self):
        amount = 0
        while amount == 0:
            amount = convert_input_to_int(input("Amount to transfer (Integer Only): "))
        return amount

    def __get_latest_unused_address(self):
        return self.account.latest_address()

    def print_menu(self) -> None:
        print("")
        print("Choose an Operation:")
        print(" [1] - Check Balance")
        print(" [2] - Generate Address")
        print(" [3] - Send IOTA")
        print(" [4] - List all transactions")
        print(" [5] - Get latest unused address")
        print(" [9] - Logout")

    def exec(self, user_choice: int) -> None:
        if user_choice == 1:
            balance = self.__get_balance()
            print("--- Balance ---")
            print(f"Incoming: {balance.get('incoming')}")
            print(f"Outgoing: {balance.get('outgoing')}")
            print(f"Available: {balance.get('available')}")
            print(f"Total: {balance.get('total')}")
            return
        if user_choice == 2:
            new_address = self.__generate_new_address()
            print(f"New Address generated: {new_address.get('address').get('inner')}")
            return
        if user_choice == 3:
            to_address = self.__get_address_to()
            amount = self.__get_transfer_amount()
            transfer = iw.Transfer(amount=amount, address=to_address, remainder_value_strategy='ReuseAddress')
            try:
                node_response = self.account.transfer(transfer)
                print(f"{amount} IOTA sent 🎉\nShould arrive soon ⏳")
            except Exception as e:
                print("Oops...something unexpected happened")
                print(e)
                print(node_response)
                return
            return
        if user_choice == 4:
            self.__synchronize()
            print("")
            print("--- 💰 Transactions 💰 ---")
            for transaction in self.account.list_messages():
                print(f"[{transaction['id']}] - Confirmed = {transaction['confirmed']}")
            return
        if user_choice == 5:
            self.__synchronize()
            print("")
            if not self.account.is_latest_address_unused():
                print(f"No unused address found -> Generate one first (Option 2)")
                return
            unused_address = self.__get_latest_unused_address()
            unused_address = unused_address['address']['inner']
            print(f"Latest unused address: {unused_address}")
            return
        if user_choice == 9:
            print()
            print(f"Bye {self.username} 👋")
            return
        print("Invalid Operation!")

    def run(self):
        user_choice = 0
        while user_choice != 9:
            self.print_menu()
            user_choice = convert_input_to_int(input("> "))
            self.exec(user_choice)
        pass
