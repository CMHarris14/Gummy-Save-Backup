import shutil
import tkinter as tk
from tkinter import simpledialog, filedialog, messagebox

import SaveHandles
from SaveHandles import GameSave, SaveHandler

manager = SaveHandler()
manager.load_from_file()


# Refresh the manager window and reload from the archive file.
# Saves current config by default. Pass False to not write current data to archive
def refresh_manager(save_on_refresh=True):
    if save_on_refresh:
        manager.write_out()
    reload_game_list()


def refresh_game_data(event=None):
    try:
        game = manager[game_list.curselection()[0]]
    except IndexError:
        return
    title_box.delete('1.0', 'end')
    files_box.delete(0, 'end')
    backup_box.delete(0, 'end')
    title_box.insert('insert', game.game_name)
    for target in game.folder_targets:
        files_box.insert('end', target)
    for backup in game.backups:
        backup_box.insert('end', backup.name + "  :  " + backup.date)


def add_file_path():
    try:
        game = manager[game_list.curselection()[0]]
    except IndexError:
        return
    new_path = filedialog.askdirectory()
    if new_path:
        game.folder_targets.append(new_path)
    refresh_manager()
    refresh_game_data()


def reload_game_list():
    game_list.delete(0, 'end')
    for game in manager:
        game_list.insert('end', game.game_name)


def add_game():
    title = simpledialog.askstring("New game", "Enter the game title")
    new_game = GameSave(title)
    manager.SaveList.append(new_game)
    refresh_manager()


def delete_game():
    try:
        game_index = game_list.curselection()[0]
    except IndexError:
        return
    deleted = manager.SaveList.pop(game_index)
    delete_backups = messagebox.askyesno("Delete backups", "Do you also want to delete any stored backups?")
    if delete_backups:
        try:
            shutil.rmtree(SaveHandles.backup_root + deleted.game_name)
        except Exception as e:
            messagebox.Message(f"Error while deleting files: {e}")
    title_box.delete('1.0', 'end')
    files_box.delete(0, 'end')
    backup_box.delete(0, 'end')
    refresh_manager()


def add_backup():
    try:
        game = manager[game_list.curselection()[0]]
    except IndexError:
        return
    backup_name = simpledialog.askstring("New backup", "Enter a name for the backup")
    game.make_backup(backup_name)
    refresh_manager()


root = tk.Tk()

root.title("Gummy Save Manager")

# Game list
game_list = tk.Listbox(root, width=50, height=30)
game_list.grid(row=0, column=0, rowspan=6, sticky="nes")
game_list.bind("<<ListboxSelect>>", refresh_game_data)

# Add game
add_game_butt = tk.Button(root, height=1, width=20)
add_game_butt.grid(row=6, padx=10, sticky="ew")
add_game_butt.config(text="Add Game", command=add_game)
# Delete game
del_game_butt = tk.Button(root, height=1, width=20)
del_game_butt.grid(row=7, padx=10, sticky="ew")
del_game_butt.config(text="Delete Game", command=delete_game)

# Title box
title_label = tk.Label(root, height=1)
title_label.grid(row=0, column=1, padx=2, pady=2)
title_label.config(text="Title ")
title_box = tk.Text(root, width=50, height=1)
title_box.grid(row=0, column=2, padx=10, pady=5)

# Files box
files_label = tk.Label(root, height=1)
files_label.grid(row=1, column=1, padx=2)
files_label.config(text="Save Paths")
files_box = tk.Listbox(root, height=15, width=30)
files_box.grid(row=2, column=1, columnspan=2, padx=10, sticky="new")

# Add file path
add_path_butt = tk.Button(root, height=1, width=20)
add_path_butt.grid(row=3, column=1, padx=10, sticky="n")
add_path_butt.config(text="Add File", command=add_file_path)
# Remove file path
rem_path_butt = tk.Button(root, height=1, width=20)
rem_path_butt.grid(row=3, column=2, padx=5, sticky="n")
rem_path_butt.config(text="Remove File")

# Backups box
backup_label = tk.Label(root, height=1)
backup_label.grid(row=4, column=1, padx=2)
backup_label.config(text="Backups")
backup_box = tk.Listbox(root, height=8, width=10)
backup_box.grid(row=5, column=1, columnspan=2, padx=10, sticky="new")

# Add backup
add_back_butt = tk.Button(root, height=1, width=20)
add_back_butt.grid(row=6, column=1, padx=10, sticky="n")
add_back_butt.config(text="Create Backup", command=add_backup)
# Remove backup
rem_back_butt = tk.Button(root, height=1, width=20)
rem_back_butt.grid(row=6, column=2, padx=5, sticky="n")
rem_back_butt.config(text="Delete Backup")
# Restore from backup
restore_back_butt = tk.Button(root, height=1, width=20)
restore_back_butt.grid(row=7, column=1, columnspan=2, padx=9, pady=10, sticky="ew")
restore_back_butt.config(text="Restore Backup")

# Row weighting
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=4)
root.rowconfigure(3, weight=8)
root.rowconfigure(4, weight=1)
root.rowconfigure(5, weight=4)

reload_game_list()

root.mainloop()
