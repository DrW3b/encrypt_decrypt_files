import os
import argparse
from cryptography.fernet import Fernet

# Define a function to generate a key
def generate_key():
    key = Fernet.generate_key()
    with open('key.txt', 'wb') as key_file:
        key_file.write(key)

# Define a function to load a key from a file
def load_key(key_file):
    return open(key_file, 'rb').read()

# Define a function to encrypt a file with a key
def encrypt_file(filename, key):
    # Read the file contents
    with open(filename, 'rb') as f:
        contents = f.read()

    # Encrypt the contents with the key
    fernet = Fernet(key)
    encrypted_contents = fernet.encrypt(contents)

    # Write the encrypted contents back to the file
    with open(filename, 'wb') as f:
        f.write(encrypted_contents)
    print(f"Encrypted {filename}")

# Define a function to decrypt a file with a key
def decrypt_file(filename, key):
    # Read the file contents
    with open(filename, 'rb') as f:
        encrypted_contents = f.read()

    # Decrypt the contents with the key
    fernet = Fernet(key)
    decrypted_contents = fernet.decrypt(encrypted_contents)

    # Write the decrypted contents back to the file
    with open(filename, 'wb') as f:
        f.write(decrypted_contents)
    print(f"Decrypted {filename}")

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Encrypt or decrypt files in a folder.')
parser.add_argument('-p', '--path', help='Path to folder to encrypt/decrypt', required=True)
parser.add_argument('-e', '--encrypt', action='store_true', help='Encrypt files in the folder')
parser.add_argument('-d', '--decrypt', action='store_true', help='Decrypt files in the folder')
parser.add_argument('-k', '--keyfile', help='Path to key file (for decryption only)')
args = parser.parse_args()

# Generate a key if encrypting
if args.encrypt:
    generate_key()
    key = load_key('key.txt')
else:
    key = load_key(args.keyfile)

# Get the list of files in the folder
folder_path = args.path
file_list = os.listdir(folder_path)

# Encrypt or decrypt each file in the folder
for filename in file_list:
    full_path = os.path.join(folder_path, filename)
    if os.path.isfile(full_path):
        if args.encrypt:
            encrypt_file(full_path, key)
        elif args.decrypt:
            decrypt_file(full_path, key)

