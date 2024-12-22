import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from cryptography.fernet import Fernet
import os
import base64

# Function to generate, load or return the key
def get_key():
    key_path = "secret.key"
    if os.path.exists(key_path):
        with open(key_path, "rb") as key_file:
            return key_file.read()
    else:
        key = Fernet.generate_key()
        with open(key_path, "wb") as key_file:
            key_file.write(key)
        return key

# Function to encrypt and decrypt data
def process_data(data, encrypt=True):
    key = get_key()
    fernet = Fernet(key)
    if encrypt:
        encrypted_data = fernet.encrypt(data.encode())
        return base64.urlsafe_b64encode(encrypted_data).decode()
    else:
        try:
            decoded_data = base64.urlsafe_b64decode(data.strip() + "=" * (4 - len(data) % 4))  # Padding Base64 if necessary
            return fernet.decrypt(decoded_data).decode()
        except Exception as e:
            print(f"Decryption error: {e}")
            return None

# Function to check if a username already exists
def username_exists(username):
    try:
        with open("passwords.txt", "r") as f:
            for line in f:
                encrypted_username, _ = line.split(" | ")
                if process_data(encrypted_username.strip(), False) == username:
                    return True
    except FileNotFoundError:
        return False
    return False

# Function to save the username and password
def save_password():
    username = username_entry.get().strip()
    password = password_entry.get().strip()

    if not username or not password:
        messagebox.showerror("Error", "Both fields are required!")
        return

    if username_exists(username):
        messagebox.showerror("Error", f"Password for username '{username}' already exists!")
        return

    # Encrypt and save the data
    encrypted_username = process_data(username)
    encrypted_password = process_data(password)
    with open("passwords.txt", "a") as f:
        f.write(f"{encrypted_username} | {encrypted_password}\n")

    messagebox.showinfo("Success", "Password saved successfully!")
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)

# Function to retrieve the password for a given username
def retrieve_password():
    username = username_entry.get().strip()
    if not username:
        messagebox.showerror("Error", "Username is required!")
        return

    try:
        with open("passwords.txt", "r") as f:
            for line in f:
                encrypted_username, encrypted_password = line.split(" | ")
                decrypted_username = process_data(encrypted_username.strip(), False)
                if decrypted_username == username:
                    decrypted_password = process_data(encrypted_password.strip(), False)
                    messagebox.showinfo("Password", f"Password for {username}: {decrypted_password}")
                    return
        messagebox.showerror("Error", f"No password found for {username}")
    except FileNotFoundError:
        messagebox.showerror("Error", "No saved passwords found!")

# Initialize main window using customtkinter for modern UI
root = ctk.CTk()
root.title("Password Manager")

# Set window size and appearance
root.geometry("400x300")
ctk.set_appearance_mode("dark")  # Set dark mode for the app
ctk.set_default_color_theme("blue")  # Set default color theme to blue

# Create a frame for the input fields and buttons
frame = ctk.CTkFrame(root, width=350, height=250)
frame.pack(pady=20, padx=20, fill="both", expand=True)

# Username label and entry
username_label = ctk.CTkLabel(frame, text="Username:", anchor="w")
username_label.pack(pady=5)
username_entry = ctk.CTkEntry(frame, width=300, placeholder_text="Enter username")
username_entry.pack(pady=5)

# Password label and entry
password_label = ctk.CTkLabel(frame, text="Password:", anchor="w")
password_label.pack(pady=5)
password_entry = ctk.CTkEntry(frame, width=300, placeholder_text="Enter password", show="*")
password_entry.pack(pady=5)

# Save password button
save_button = ctk.CTkButton(frame, text="Save Password", command=save_password)
save_button.pack(pady=10)

# Retrieve password button
retrieve_button = ctk.CTkButton(frame, text="Retrieve Password", command=retrieve_password)
retrieve_button.pack(pady=10)

# Start the GUI loop
root.mainloop()
