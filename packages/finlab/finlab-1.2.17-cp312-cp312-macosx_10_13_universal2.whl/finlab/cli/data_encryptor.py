import os
import json
import uuid
from hashlib import md5
from getpass import getpass
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from base64 import urlsafe_b64encode, urlsafe_b64decode



def hash_value(val):
    return md5(val.encode('utf-8')).hexdigest()


class DataEncryptor:
    def __init__(self, data: dict, password: str = '', default_path: str = ''):
        self.data = data
        self.password = password or self.__get_machine_password()
        self.default_path = default_path
    
    def __generate_key_from_password(self, password, salt):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = urlsafe_b64encode(kdf.derive(password.encode()))
        return key
    
    def encrypt_data(self) -> str:
        salt = os.urandom(16)  # Generate a new salt for each encryption
        key = self.__generate_key_from_password(self.password, salt)
        cipher_suite = Fernet(key)
        data_str = json.dumps(self.data)
        encrypted_data = cipher_suite.encrypt(data_str.encode())
        
        # Combine the salt and the encrypted data for storage/transmission
        combined = urlsafe_b64encode(salt + encrypted_data).decode()
        return combined
    
    @classmethod
    def decrypt_data(cls, encrypted_data: str, password: str = ''):
        password = password or cls.__get_machine_password_static()
        combined = urlsafe_b64decode(encrypted_data.encode())
        salt = combined[:16]
        encrypted_data = combined[16:]
        key = cls.__generate_key_from_password_static(password, salt)
        cipher_suite = Fernet(key)
        decrypted_data = cipher_suite.decrypt(encrypted_data)
        data = json.loads(decrypted_data.decode())
        return data
    
    @staticmethod
    def __generate_key_from_password_static(password, salt):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = urlsafe_b64encode(kdf.derive(password.encode()))
        return key
    
    @staticmethod
    def __get_machine_password_static():
        mac = hash_value(str(uuid.getnode()))
        return mac
    
    def __get_machine_password(self):
        return self.__get_machine_password_static()
    
    def to_file(self, path=''):
        if not path:
            path = self.default_path
        if not path:
            raise ValueError("No path provided for saving the file.")
        
        encrypted_data = self.encrypt_data()
        with open(path, 'w') as file:
            file.write(encrypted_data)

    @classmethod
    def from_file(cls, path, password: str = ''):

        if os.path.exists(path):
            with open(path, 'r') as file:
                encrypted_data = file.read()
        else:
            return cls({}, password, path)

        data = cls.decrypt_data(encrypted_data, password)
        # decrypted = False
        # while not decrypted:
        #     try:
        #         decrypted = True
        #     except e as Exception:
        #         # print traceback
        #         print(e)
        #         password = getpass('Enter the password to decrypt the file: ')

            
        return cls(data, password, path)
    
    def change_password(self, new_password: str = ''):
        self.password = new_password or self.__get_machine_password()