import tkinter as tk
from tkinter import filedialog, messagebox
import os
import json
from encryption import generate_key, encrypt_file, decrypt_file, load_key
from file_sharing import generate_rsa_keys, encrypt_aes_key, decrypt_aes_key
from auth import register, authenticate

class SecureFileApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure File Encryption App")
        self.root.geometry("450x400")
        self.root.configure(bg="#f4f4f4")

        self.file_path = ""
        self.current_user = None

        self.show_login_screen()

    # Login Screen
    def show_login_screen(self):
        self.clear_window()

        tk.Label(self.root, text="🔐 Secure File App Login", font=("Arial", 18, "bold"), bg="#f4f4f4").pack(pady=10)

        tk.Label(self.root, text="Username:", bg="#f4f4f4").pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack(pady=5)

        tk.Label(self.root, text="Password:", bg="#f4f4f4").pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5)

        tk.Button(self.root, text="Login", command=self.login).pack(pady=5)
        tk.Button(self.root, text="Register", command=self.show_register_screen).pack(pady=5)

    # Registration Screen
    def show_register_screen(self):
        self.clear_window()

        tk.Label(self.root, text="📝 Register New Account", font=("Arial", 18, "bold"), bg="#f4f4f4").pack(pady=10)

        tk.Label(self.root, text="Username:", bg="#f4f4f4").pack()
        self.new_username_entry = tk.Entry(self.root)
        self.new_username_entry.pack(pady=5)

        tk.Label(self.root, text="Password:", bg="#f4f4f4").pack()
        self.new_password_entry = tk.Entry(self.root, show="*")
        self.new_password_entry.pack(pady=5)

        tk.Button(self.root, text="Register", command=self.register_user).pack(pady=5)
        tk.Button(self.root, text="Back to Login", command=self.show_login_screen).pack(pady=5)

    # Clear the window for new screens
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # Login Function
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        success, message = authenticate(username, password)

        if success:
            self.current_user = username  # Set the logged-in user
            messagebox.showinfo("Success", message)
            self.show_main_app()
        else:
            messagebox.showerror("Error", message)

    # Register User
    def register_user(self):
        username = self.new_username_entry.get()
        password = self.new_password_entry.get()
        success, message = register(username, password)

        if success:
            messagebox.showinfo("Success", message)
            self.show_login_screen()
        else:
            messagebox.showerror("Error", message)

    # Main App Interface
    def show_main_app(self):
        self.clear_window()

        try:
            self.key = load_key()
        except FileNotFoundError:
            self.key = generate_key()

        title_label = tk.Label(self.root, text="🔐 Secure File App", font=("Arial", 20, "bold"), bg="#f4f4f4")
        title_label.pack(pady=10)

        file_frame = tk.LabelFrame(self.root, text="File Operations", padx=10, pady=10, bg="#ffffff")
        file_frame.pack(padx=10, pady=5, fill="both")

        tk.Button(file_frame, text="Select File", command=self.select_file, width=20).pack(pady=5)
        self.file_label = tk.Label(file_frame, text="No file selected", wraplength=300, bg="#ffffff")
        self.file_label.pack(pady=5)

        tk.Button(file_frame, text="Encrypt File", command=self.encrypt_selected_file, width=20).pack(pady=5)
        tk.Button(file_frame, text="Decrypt File", command=self.decrypt_selected_file, width=20).pack(pady=5)

        key_frame = tk.LabelFrame(self.root, text="Key Management", padx=10, pady=10, bg="#ffffff")
        key_frame.pack(padx=10, pady=5, fill="both")

        tk.Button(key_frame, text="Generate RSA Keys", command=self.generate_keys, width=20).pack(pady=5)
        tk.Button(key_frame, text="Secure Share File", command=self.secure_share_file, width=20).pack(pady=5)
        tk.Button(key_frame, text="Decrypt Shared Key", command=self.decrypt_shared_key, width=20).pack(pady=5)

    # File Selection
    def select_file(self):
        self.file_path = filedialog.askopenfilename()
        if self.file_path:
            self.file_label.config(text=self.file_path)
        else:
            self.file_label.config(text="No file selected")

    # Encrypt File
    def encrypt_selected_file(self):
        if self.file_path:
            encrypt_file(self.file_path, self.key)
            os.remove(self.file_path)

            # Save metadata with the username
            metadata = {"username": self.current_user}
            with open(self.file_path + ".meta", "w") as meta_file:
                json.dump(metadata, meta_file)

            messagebox.showinfo("Success", "File Encrypted and Original File Removed Successfully!")
        else:
            messagebox.showwarning("Warning", "Please select a file to encrypt.")

    # Decrypt File
    def decrypt_selected_file(self):
        if self.file_path.endswith('.enc'):
            meta_path = self.file_path + ".meta"
            if os.path.exists(meta_path):
                with open(meta_path, "r") as meta_file:
                    metadata = json.load(meta_file)
                if metadata.get("username") != self.current_user:
                    messagebox.showerror("Error", "You are not authorized to decrypt this file.")
                    return

            decrypt_file(self.file_path, self.key)
            os.remove(self.file_path)

            if os.path.exists(meta_path):
                os.remove(meta_path)

            messagebox.showinfo("Success", "File Decrypted Successfully!")
        else:
            messagebox.showwarning("Warning", "Please select an encrypted (.enc) file to decrypt.")

    # Generate RSA Keys
    def generate_keys(self):
        private_key, public_key = generate_rsa_keys()
        messagebox.showinfo("Success", "RSA Key Pair Generated Successfully!")

    # Secure File Sharing (Encrypt AES Key)
    def secure_share_file(self):
        if self.file_path:
            encrypted_aes_key = encrypt_aes_key(self.key, "public.pem")
            with open(self.file_path + ".key.enc", "wb") as key_file:
                key_file.write(encrypted_aes_key)
            messagebox.showinfo("Success", "File Shared Securely! AES Key Encrypted.")
        else:
            messagebox.showwarning("Warning", "Please select a file to share securely.")

    # Decrypt Shared Key
    def decrypt_shared_key(self):
        key_file_path = filedialog.askopenfilename(filetypes=[("Encrypted Key Files", "*.key.enc")])
        if key_file_path:
            try:
                with open(key_file_path, "rb") as key_file:
                    encrypted_key = key_file.read()
                decrypted_aes_key = decrypt_aes_key(encrypted_key, "private.pem")
                messagebox.showinfo("Success", f"AES Key Decrypted Successfully: {decrypted_aes_key.decode()}")
            except Exception as e:
                messagebox.showerror("Error", f"Decryption failed: {str(e)}")
        else:
            messagebox.showwarning("Warning", "Please select an encrypted key file.")

# Run the App
if __name__ == "__main__":
    root = tk.Tk()
    app = SecureFileApp(root)
    root.mainloop()
