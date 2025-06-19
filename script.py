import os
import shutil
import datetime
import tkinter as tk
from tkinter import filedialog, messagebox

file_types = {
    "Images": ['.jpg', '.gif', '.jpeg', '.png'],
    "Documents": ['.docx', '.pdf', '.txt', '.ppt', '.xlxs'],
    "Videos": ['.mp4', '.mkv', '.mov'],
    "Audios": ['.mp3', '.wav'],
    "Archives": ['.rar', '.zip', '.tar'],
    "Scripts": ['.py', '.js', '.cpp', '.bat'],
}

log_file = "organizer_log.txt"

def log(message):
    print(message)
    with open(log_file, "a") as f:
        f.write(message + "\n")

def org_by_type(folder_path):
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path):
            _, ext = os.path.splitext(file)
            for category, extensions in file_types.items():
                if ext.lower() in extensions:
                    category_path = os.path.join(folder_path, category)
                    os.makedirs(category_path, exist_ok=True)
                    shutil.move(file_path, os.path.join(category_path, file))
                    log(f"Moved: {file} --> {category}/")
                    break

def org_by_date(folder_path):
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path):
            modified_time = os.path.getmtime(file_path)
            date = datetime.datetime.fromtimestamp(modified_time).strftime('%Y-%m-%d')
            date_folder = os.path.join(folder_path, date)
            os.makedirs(date_folder, exist_ok=True)
            shutil.move(file_path, os.path.join(date_folder, file))
            log(f"Moved: {file} --> {date}/")

def ask_and_org():
    folder_path = filedialog.askdirectory(title="Select a folder to organize")
    if not folder_path:
        return

    option = tk.messagebox.askquestion("Choose Mode", "Do you want to organize by FILE TYPE?\nChoose 'No' to organize by DATE.")

    if option == 'yes':
        org_by_type(folder_path)
    else:
        org_by_date(folder_path)

    tk.messagebox.showinfo("Done", "Files organized successfully!\nCheck 'organizer_log.txt' for log.")

# GUI Setup
root = tk.Tk()
root.title("Python File Organizer")

tk.Label(root, text="Organize Files by Type or Date", font=("Arial", 14)).pack(pady=10)
tk.Button(root, text="Browse Folder and Organize", command=ask_and_org, padx=10, pady=5).pack(pady=20)

root.mainloop()
