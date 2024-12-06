import getpass
import os
import subprocess
import sys
import tempfile
import argparse
import base64

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt


class Color:
    okBlue = '\033[94m'
    okCyan = '\033[96m'
    okGreen = '\033[92m'
    warning = '\033[93m'
    error = '\033[91m'
    end = '\033[0m'


def __derive_key(vault_password: str, salt: bytes) -> bytes:
    """Derive a key for use as input for Scrypt encryption algorithm. 
    
    AKA 'Key Stretching' https://en.wikipedia.org/wiki/Key_stretching"""
    kdf = Scrypt(
        salt=salt,
        length=32,  # 32 bytes = 256 bits
        n=2 ** 18,  # CPU/memory cost factor
        r=8,  # block size
        p=1,  # parallelization factor
        backend=default_backend()
    )
    return kdf.derive(vault_password.encode())

def __base64_to_numbers(b64_string: str) -> str:
    """Takes a base64 string as input and converts it to a string of numbers.
    
    For each character, it converts to its ASCII value using ord(char) and then converts the
    ASCII value to a string. Finally, it pads the resulting string with leading zeroes to ensure its
    always 3 digits long using zfill(3)"""
    return ''.join(str(ord(char)).zfill(3) for char in b64_string)

def __numbers_to_base64(numbers_string: str) -> str:
    """Takes a string of numbers as input and converts it to a base64 string.
    
    Processes the input string in chunks of 3 digits. For each 3-digit chunk, it first converts it to an integer,
    then converts the integer back to a character using chr(), and finally joins all characters together into a
    single string.
    
    e.g: '065066' would output 'AB'"""
    chars = [chr(int(numbers_string[i:i+3])) for i in range(0, len(numbers_string), 3)]
    return ''.join(chars)

def encrypt_file(file_path: str, vault_password: str, output_path: str):
    """Encrypt the contents of a file and save as <file_name>.enc"""
    salt = os.urandom(16)
    key = __derive_key(vault_password, salt)
    aes_gcm = AESGCM(key)
    nonce = os.urandom(12)

    with open(file_path, 'rb') as file:
        unencrypted_data = file.read()

    encrypted_data = aes_gcm.encrypt(nonce, unencrypted_data, None)
    encoded_data = base64.b64encode(salt + nonce + encrypted_data).decode('utf-8')
    numerical_data = __base64_to_numbers(encoded_data)

    with open(output_path, 'w') as file:
        file.write(numerical_data)


def decrypt_file(file_path: str, vault_password: str) -> bytes:
    """Decrypt a vault using the supplied password.
    
    Used for viewing and editing contents of a vault.
    
    Use method: decrypt() instead if extracting contents of a vault in your own scripts"""
    try:
        with open(file_path, 'r') as file:
            numerical_data = file.read()

        encoded_data = __numbers_to_base64(numerical_data)
        decoded_data = base64.b64decode(encoded_data)
        salt = decoded_data[:16]
        nonce = decoded_data[16:28]
        encrypted_data = decoded_data[28:]

        key = __derive_key(vault_password, salt)
        aes_gcm = AESGCM(key)
        decrypt_data = aes_gcm.decrypt(nonce, encrypted_data, None)

        return decrypt_data

    except InvalidTag:
        sys.exit(f"{Color.warning}Error: Incorrect password or corrupted file.{Color.end}")
    except Exception as e:
        sys.exit(f"{Color.error}An unexpected error occurred: {e}{Color.end}")

def decrypt(file_path: str, decryption_password: str) -> str:
    """Decrypt the contents of a vault and return the decrypted content as a string"""
    decrypted_bytes = decrypt_file(file_path, decryption_password)
    return decrypted_bytes.decode('utf-8').strip()

def file_already_exists(file_path: str) -> bool:
    """If the encrypted file already exists, prompt the user to overwrite the file.
    If the user declines to overwrite the file, sys.exit(0)"""
    path = os.path.join(os.getcwd(), os.path.basename(file_path) + '.enc')
    temporary_path = os.path.join(os.getcwd(), os.path.basename(file_path))

    if os.path.exists(path):  # If the file already exists, prompt the user to overwrite it
        file_name = os.path.basename(file_path)
        overwrite = input(f"{Color.warning}File: [{file_name}] already exists. Overwrite? (y/n): {Color.end}")
        if overwrite.lower() != 'y':
            print("Operation cancelled")
            if os.path.exists(temporary_path):
                os.remove(temporary_path)
            sys.exit(0)

    return os.path.exists(file_path)

def is_file_encrypted(file_path: str) -> bool:
    """If file name ends in '.enc' then assume the file is encrypted and return True, if not, return False"""
    if file_path.endswith('.enc'):
        return True
    if not file_path.endswith('.enc'):
        return False


def main():
    usage = "pyvaulter [--help] <edit|create|view|encrypt> <file_name>"
    parser = argparse.ArgumentParser(description="Encrypt files", usage=usage)
    subparsers = parser.add_subparsers(dest="command")
    
    # Edit command
    parser_edit = subparsers.add_parser("edit", help="Edit an encrypted file")
    parser_edit.add_argument("file_name", help="Name of the file to edit")
    
    # Create command
    parser_create = subparsers.add_parser("create", help="Create and encrypt a new file")
    parser_create.add_argument("file_name", help="Name of the file to create")
    
    # View command
    parser_view = subparsers.add_parser("view", help="View an encrypted file")
    parser_view.add_argument("file_name", help="Name of the file to view")
    
    # Encrypt command
    parser_encrypt = subparsers.add_parser("encrypt", help="Encrypt an existing, unencrypted file (path)")
    parser_encrypt.add_argument("file_name", help="Name of the file to encrypt")
    
    args = parser.parse_args()

    # If no argument is provided, show the help output
    if args.command is None:
        parser.print_help()
        sys.exit(1)
    
    command = args.command
    file_name = args.file_name

    # Exit if the file targeted to edit or view isn't encrypted
    if (command == "edit" or command == "view") and not is_file_encrypted(file_name):
        sys.exit(f"{Color.warning}File is not encrypted{Color.end}")
    
    # Exit if the target file to encrypt is already encrypted
    if (command == "encrypt") and is_file_encrypted(file_name):
        sys.exit(f"{Color.warning}File is already encrypted{Color.end}")
    
    # Exit if file being created is manually appended with `.enc`
    if (command == "create") and is_file_encrypted(file_name):
        sys.exit(f"{Color.warning}Invalid file name: Do not manually append with `.enc`{Color.end}")
    
    # File must not already exist, use encrypt option instead
    if (command == "create") and os.path.exists(file_name):
        sys.exit(f"{Color.warning}File already exists: Use <encrypt> option instead of <create>{Color.end}")
    
    password = getpass.getpass(f"{Color.okBlue}Enter password: {Color.end}")
    
    if command == "edit":
        if os.path.exists(file_name):
            original_data = decrypt_file(file_name, password)
    
            # Create temp file with contents of original file
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file_path = temp_file.name
                temp_file.write(original_data)
    
            # Edit the temp file
            subprocess.run(['vim', temp_file_path])
    
            # Read the contents of the temp file
            with open(temp_file_path, 'rb') as temp_file:
                modified_data = temp_file.read()
    
            # Compare the contents of the original data to the temp file.
            # If the content changed, overwrite the file with the new contents from temp file and encrypt it
            if original_data != modified_data:
                encrypt_file(temp_file_path, password, file_name)
                print(f"{Color.okGreen}File encrypted and saved in working directory{Color.end}")
            else:
                print(f"{Color.okCyan}No changes were made{Color.end}")
            # Then delete the temp file
            os.remove(temp_file_path)
            sys.exit(0)
        else:
            sys.exit(f"{Color.warning}File {file_name} does not exist.{Color.end}")
    
    elif command == "create":
        # open vim for editing new file_name
        subprocess.run(['vim', file_name])
    
        # If output file (<file_name>.enc) already exists in vaults/ directory, ask to overwrite
        file_already_exists(file_name)
        # set the encrypted file name to be appended with .enc
        file_output_path = os.path.join(os.getcwd(), os.path.basename(file_name) + '.enc')
        # encrypt the file
        encrypt_file(file_name, password, file_output_path)
        # delete the initial file created, since the new encrypted file now exists
        os.remove(file_name)
    
        print(f"{Color.okGreen}File encrypted and saved in current working directory{Color.end}")
        sys.exit(0)
    
    elif command == "view":
        if os.path.exists(file_name):
            # Decrypt the data
            decrypted_data = decrypt_file(file_name, password)
            # Then write to a temp file
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file_path = temp_file.name
                temp_file.write(decrypted_data)
            # Then view the temp file with `less`
            subprocess.run(['less', temp_file_path])
            # Then remove the temp file after it's been closed
            os.remove(temp_file_path)
            sys.exit(0)
        else:
            sys.exit(f"{Color.warning}File {file_name} does not exist.{Color.end}")
    
    elif command == "encrypt":
        if os.path.exists(file_name):
            file_already_exists(file_name)
    
            file_output_path = os.path.join(os.getcwd(), os.path.basename(file_name) + '.enc')
    
            encrypt_file(file_name, password, file_output_path)
    
            print(f"{Color.okGreen}File encrypted and saved in current working directory{Color.end}")
            sys.exit(0)
        else:
            sys.exit(f"{Color.warning}File {file_name} does not exist.{Color.end}")

if __name__ == '__main__':
    main()
