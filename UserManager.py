import hashlib
import os
import pickle


from typing import Dict, List


class User:
    def __init__(self, username: str, password: str) -> None:
        self.name = username
        self.salt = self._generate_salt()
        self.key = self._get_key(password, self.salt)
    
    def _generate_salt(self) -> bytes:
        return os.urandom(32)
    
    def _get_key(self, password: str, salt: str) -> bytes:
        return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    
    def check_password(self, password: str) -> bool:
        if self.key == self._get_key(password, self.salt):
            return True
        return False

class UserManager:
    def __init__(self) -> None:
        self.file_path: str = "users.data"
        self.users: Dict[str, User] = self.__read_users_from_file()
    
    def __del__(self) -> None:
        self.__dump_users_to_file()
    
    def __dump_users_to_file(self):
        f = open(self.file_path, 'wb')
        pickle.dump(self.users, f)
    
    def __read_users_from_file(self) -> Dict[str, User]:
        if not os.path.exists(self.file_path):
            return {}
        f = open(self.file_path, 'rb')
        users = pickle.load(f)
        return users
    
    def add_user(self, username: str, password: str) -> None:
        new_user = User(username, password)
        self.users[username] = new_user
    
    def login(self, username: str, password: str) -> bool:
        user = self.users.get(username)
        if user is None:
            print(f"User {username} does not exist")
            return False
        success = user.check_password(password)
        if not success:
            print(f"Password incorrect")
            return False
        return True
    
    def remove_user(self, username: str, password: str) -> None:
        self.users.pop(username)

    # def get_all_users(self) -> Dict[str, User]:
    #     return self.users
    
    def get_all_users(self) -> List[User]:
        return self.users.values()
    
    def user_exists(self, username: str) -> bool:
        user = self.users.get(username)
        if user is not None: 
            return True
        return False
    
    def get_username_by_index(self, index) -> str:
        return list(self.users.values())[index].name