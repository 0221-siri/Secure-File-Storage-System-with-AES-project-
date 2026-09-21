Secure File Storage System Using AES

Introduction:
This project is a simple Secure File Storage System developed using Python.

It protects files by encrypting them before storage and decrypting them when required.

Objective:
- Encrypt files securely
- Decrypt encrypted files
- Verify file integrity using SHA-256 hash
- Store file metadata

Technologies Used:
- Python
- Cryptography
- Fernet
- SHA-256
- JSON
- Pydroid 3

 Features:
- File encryption
- File decryption
- Secure key generation
- SHA-256 integrity verification
- Metadata storage

How It Works:

 1. Encrypt File
The user selects a file and the system encrypts it.

The encrypted file is saved with `.enc` extension.
 2. Store Metadata
The system stores:
- Original filename
- Time
- SHA-256 hash
3. Decrypt File
The encrypted file can be decrypted using the generated key.    
4. Integrity Verification
After decryption, the SHA-256 hash is checked.

If the hashes match:

Integrity check: PASSED

How to Run:

Install the required package:

bash
pip installation encryption
