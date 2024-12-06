# pyvaulter
A very simple Python module that can be used to encrypt sensitive data. Emulates much of the functionality of Ansible Vaults but for Python.

## Basic Usage (Creating/Editing Encrypted Files)

All encrypted files are placed in the current working directory.

`pyvaulter [--help] <edit|create|view|encrypt> <file_name>`

`pyvaulter create <file_name>`: Create and encrypt a new file

`pyvaulter edit <file_name>`: Edit an encrypted file that has been encrypted by pyvaulter

`pyvaulter view <file_name>`: View an encrypted file a file that has been encrypted by pyvaulter

`pyvaulter encrypt <file_name>`: Encrypt an existing, unencrypted file (path). This is intended to encrypt a copy of an
already-existing file on your system. It will not encrypt the original file, but rather create a copy of it.

## Basic Usage (In a script)

You can use `pyvaulter` in your script or application to decrypt the contents of files at runtime. So, in practice the
workflow looks like this:

1. Encrypt an existing file, or create a new encrypted file with pyvault
2. In your script or application, decrypt the file like so:
```python
from pyvaulter import decrypt
from getpass import getpass

# You could also just pass in the decryption password using an environment variable, that way you're not prompted to
# type it each time, but for the sake of simplicity, you can also do it this way.
secure_password = getpass('Enter decryption password')

# Decrypt the file, returning the contents as a string
my_secret_file_content = decrypt(file_path='/path/to/encrypted/file', decryption_password=secure_password)
```
