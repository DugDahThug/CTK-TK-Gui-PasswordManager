# Password Manager

This is a simple, modern, and secure password manager built using Python and `CustomTkinter`. It allows users to store and retrieve passwords safely using encryption. The passwords are encrypted before being stored and decrypted when needed, ensuring that sensitive information is protected.

## Features

- **Save Passwords**: Store usernames and passwords securely.
- **Retrieve Passwords**: Retrieve stored passwords by entering the associated username.
- **Encryption**: Passwords and usernames are encrypted using `cryptography.fernet` to keep them secure.
- **Dark Mode**: The app has a sleek, dark-themed user interface created using `CustomTkinter`.
- **Prevents Duplicate Entries**: A username can only be saved once, avoiding duplicate entries in the password storage.

## Requirements

To run this project, you'll need Python 3.x and the following libraries:

- `customtkinter` - For creating modern GUI components.
- `cryptography` - For secure encryption and decryption of passwords.

### Installation

1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/DugDahThug/CTK-TK-Gui-PasswordManager.git
