from cryptography.fernet import Fernet, InvalidToken
import os
import hashlib
import json
from datetime import datetime

# -----------------------------
# FOLDER AND FILE SETTINGS
# -----------------------------

KEY_FILE = "key.key"
ENCRYPTED_FOLDER = "encrypted_files"
DECRYPTED_FOLDER = "decrypted_files"


# -----------------------------
# 1. GENERATE ENCRYPTION KEY
# -----------------------------

def generate_key():

    if not os.path.exists(KEY_FILE):

        key = Fernet.generate_key()

        with open(KEY_FILE, "wb") as file:
            file.write(key)

        print("Encryption key generated successfully.")

    else:
        print("Encryption key already exists.")


# -----------------------------
# 2. LOAD ENCRYPTION KEY
# -----------------------------

def load_key():

    with open(KEY_FILE, "rb") as file:
        return file.read()


# -----------------------------
# 3. CALCULATE SHA-256 HASH
# -----------------------------

def calculate_hash(filename):

    sha256 = hashlib.sha256()

    with open(filename, "rb") as file:

        while True:

            data = file.read(4096)

            if not data:
                break

            sha256.update(data)

    return sha256.hexdigest()


# -----------------------------
# 4. ENCRYPT FILE
# -----------------------------

def encrypt_file(filename):

    # Check whether file exists
    if not os.path.exists(filename):

        print("File not found.")
        return

    # Load encryption key
    key = load_key()

    fernet = Fernet(key)

    # Read original file
    with open(filename, "rb") as file:

        original_data = file.read()

    # Encrypt the file
    encrypted_data = fernet.encrypt(original_data)

    # Create encrypted folder
    os.makedirs(ENCRYPTED_FOLDER, exist_ok=True)

    # Create encrypted filename
    original_name = os.path.basename(filename)

    encrypted_name = original_name + ".enc"

    encrypted_path = os.path.join(
        ENCRYPTED_FOLDER,
        encrypted_name
    )

    # Save encrypted file
    with open(encrypted_path, "wb") as file:

        file.write(encrypted_data)

    # Calculate original file hash
    file_hash = calculate_hash(filename)

    # Create metadata
    metadata = {

        "original_filename": original_name,

        "encrypted_filename": encrypted_name,

        "created_at":
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

        "sha256": file_hash
    }

    # Save metadata
    metadata_path = encrypted_path + ".json"

    with open(metadata_path, "w") as file:

        json.dump(metadata, file, indent=4)

    print()
    print("File encrypted successfully!")
    print("Encrypted file:", encrypted_path)
    print("Metadata file:", metadata_path)


# -----------------------------
# 5. DECRYPT FILE
# -----------------------------

def decrypt_file(encrypted_path):

    # Check encrypted file
    if not os.path.exists(encrypted_path):

        print("Encrypted file not found.")
        return

    # Load key
    key = load_key()

    fernet = Fernet(key)

    try:

        # Read encrypted file
        with open(encrypted_path, "rb") as file:

            encrypted_data = file.read()

        # Decrypt
        decrypted_data = fernet.decrypt(encrypted_data)

    except InvalidToken:

        print()
        print("Decryption failed!")
        print("Wrong key or damaged/tampered file.")
        return

    # Create decrypted folder
    os.makedirs(DECRYPTED_FOLDER, exist_ok=True)

    # Get original filename
    filename = os.path.basename(encrypted_path)

    if filename.endswith(".enc"):

        filename = filename[:-4]

    decrypted_path = os.path.join(
        DECRYPTED_FOLDER,
        filename
    )

    # Save decrypted file
    with open(decrypted_path, "wb") as file:

        file.write(decrypted_data)

    print()
    print("File decrypted successfully!")
    print("Decrypted file:", decrypted_path)

    # -----------------------------
    # INTEGRITY VERIFICATION
    # -----------------------------

    metadata_path = encrypted_path + ".json"

    if os.path.exists(metadata_path):

        with open(metadata_path, "r") as file:

            metadata = json.load(file)

        original_hash = metadata["sha256"]

        decrypted_hash = calculate_hash(
            decrypted_path
        )

        print()

        if original_hash == decrypted_hash:

            print("Integrity check: PASSED")

        else:

            print("Integrity check: FAILED")

    else:

        print("Metadata file not found.")


# -----------------------------
# 6. MAIN MENU
# -----------------------------

def main():

    # Generate key when program starts
    generate_key()

    while True:

        print()
        print("==============================")
        print("  SECURE FILE STORAGE SYSTEM")
        print("==============================")

        print("1. Encrypt a file")
        print("2. Decrypt a file")
        print("3. Exit")

        print()

        choice = input(
            "Enter your choice: "
        )

        # -------------------------
        # ENCRYPT
        # -------------------------

        if choice == "1":

            print()

            filename = input(
                "Enter the file path: "
            )

            encrypt_file(filename)

        # -------------------------
        # DECRYPT
        # -------------------------

        elif choice == "2":

            print()

            encrypted_path = input(
                "Enter encrypted file path: "
            )

            decrypt_file(encrypted_path)

        # -------------------------
        # EXIT
        # -------------------------

        elif choice == "3":

            print()
            print("Thank you for using Secure File Storage System.")

            break

        # -------------------------
        # INVALID OPTION
        # -------------------------

        else:

            print()
            print("Invalid choice.")
            print("Please select 1, 2 or 3.")


# -----------------------------
# PROGRAM START
# -----------------------------

if __name__ == "__main__":

    main()