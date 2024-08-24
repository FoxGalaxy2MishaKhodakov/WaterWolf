import os
import zipfile
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
import sys
import winshell
from win32com.client import Dispatch
import ctypes  # Для проверки прав администратора

# Переменные
zip_app = "browser.zip"  # Название ZIP-файла с программой
app_name = "WaterWolf"  # Название программы

# Определяем директорию, на одну ступень ниже текущего файла
base_dir = os.path.join(os.path.dirname(__file__))

# Пути к файлам в поддиректории "resources"
zip_app_path = os.path.join(base_dir, zip_app)
background_image_path = os.path.join(base_dir, "background.png")

# Пути для установки и ярлыков
install_path = Path(rf"C:\Program Files (x86)\{app_name}")
desktop_path = winshell.desktop()
start_menu_path = winshell.start_menu()

# Файл ZIP в самом .exe
if hasattr(sys, '_MEIPASS'):
    embedded_zip_path = os.path.join(sys._MEIPASS, zip_app)
else:
    embedded_zip_path = zip_app_path

# Проверка прав администратора
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# Основное окно
root = tk.Tk()
root.title("Installer WaterWolf Web Browser")
root.geometry("800x600")
root.resizable(False, False)

# Фон
background_image = tk.PhotoImage(file=background_image_path)
background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)

# Функция установки
def install():
    install_button.pack_forget()
    #progress.pack(pady=20)
    
    try:
        # Извлечение файлов
        with zipfile.ZipFile(embedded_zip_path, 'r') as zip_ref:
            zip_ref.extractall(install_path)
        #progress.step(50)
        root.update_idletasks()

        # Создание ярлыков
        create_shortcut(install_path / "browser/browser.exe", desktop_path, f"{app_name}.lnk")
        create_shortcut(install_path / "browser/browser.exe", start_menu_path, f"{app_name}.lnk")
        #progress.step(50)
        root.update_idletasks()

        messagebox.showinfo("Установка завершена", f"Программа {app_name} успешно установлена!")
        root.quit()
    except Exception as e:
        messagebox.showerror("Ошибка", str(e))
        root.quit()

# Создание ярлыков
def create_shortcut(target_exe, shortcut_dir, shortcut_name):
    shortcut_path = os.path.join(shortcut_dir, shortcut_name)
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.Targetpath = str(target_exe)
    shortcut.WorkingDirectory = str(target_exe.parent)
    shortcut.IconLocation = str(target_exe)
    shortcut.save()

# Кнопка установки
install_button = tk.Button(root, text=f'Install "{app_name}"', command=install)
install_button.pack(pady=250)

# Проверка прав администратора при запуске
if not is_admin():
    messagebox.showerror("Ошибка", "Запуск программы возможен только от имени администратора.")
    sys.exit()

# Полоса прогресса
#progress = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")

root.mainloop()
