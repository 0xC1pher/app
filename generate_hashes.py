# generate_hashes.py

from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

if __name__ == '__main__':
    plain_password = input("Ingrese la contraseña: ")
    hashed_password = bcrypt.generate_password_hash(plain_password).decode('utf-8')
    print(f"Contraseña hasheada: {hashed_password}")
