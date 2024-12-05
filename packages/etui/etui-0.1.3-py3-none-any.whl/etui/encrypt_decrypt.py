from pathlib import Path

from cryptography.fernet import Fernet


def generate_key() -> str:
    key = Fernet.generate_key()
    return key


def loaad_key() -> str:
    with open("key.txt", "r") as f:
        return f.read()


def store_key(key: str) -> None:
    with open("key.txt", "wb") as f:
        f.write(key)


def get_key() -> str:
    if Path("key.txt").exists():
        print("\nKey exists, tyring to load..\n")
        return loaad_key()
    else:
        print("\nKey does not exist, generating..")
        key = generate_key()
        print("Storing key..\n")
        store_key(key)
        return key


def encrypt(input: str) -> str:
    key = get_key()
    return Fernet(key).encrypt(input.encode()).decode()


def decrypt(input: str) -> str:
    key = get_key()
    return Fernet(key).decrypt(input.encode()).decode()


if __name__ == "__main__":
    operation = input("Encrypt or Decrypt: ")
    input = input("Input: ")

    if operation.lower() == "encrypt":
        out = encrypt(input)
    elif operation.lower() == "decrypt":
        out = decrypt(input)

    print(out)
