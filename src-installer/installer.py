import os
import zipfile
import tkinter as tk
from tkinter import messagebox
from pathlib import Path
import sys
import winshell
from win32com.client import Dispatch
import ctypes  # Для проверки прав администратора
import shutil  # Для удаления директорий

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

# Функция установки приложения
def install_app():
    if not is_admin():
        messagebox.showerror("Ошибка", "Для установки требуется запуск от имени администратора.")
        sys.exit()
        return
    with zipfile.ZipFile(embedded_zip_path, 'r') as zip_ref:
        zip_ref.extractall(install_path)
    create_shortcuts()
    messagebox.showinfo("Установка", "Приложение успешно установлено.")
    sys.exit()

# Функция обновления приложения
def update_app():
    if not is_admin():
        messagebox.showerror("Ошибка", "Для обновления требуется запуск от имени администратора.")
        sys.exit()
        return
    # Удаление старой версии приложения
    if install_path.exists():
        shutil.rmtree(install_path)
    # Установка новой версии
    install_app()

# Функция удаления приложения
def uninstall_app():
    if not is_admin():
        messagebox.showerror("Ошибка", "Для удаления требуется запуск от имени администратора.")
        sys.exit()
        return
    if install_path.exists():
        shutil.rmtree(install_path)
    remove_shortcuts()
    messagebox.showinfo("Удаление", "Приложение успешно удалено.")
    sys.exit()

# Функция создания ярлыков
def create_shortcuts():
    # Создание ярлыка на рабочем столе
    desktop_shortcut = os.path.join(desktop_path, f"{app_name}.lnk")
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(desktop_shortcut)
    shortcut.Targetpath = str(install_path / "browser" / "browser.exe")
    shortcut.WorkingDirectory = str(install_path)
    shortcut.IconLocation = str(install_path / "browser" / "browser.exe")
    shortcut.save()

    # Создание ярлыка в меню Пуск
    start_menu_shortcut = os.path.join(start_menu_path, f"{app_name}.lnk")
    shortcut = shell.CreateShortCut(start_menu_shortcut)
    shortcut.Targetpath = str(install_path / "browser" / "browser.exe")
    shortcut.WorkingDirectory = str(install_path)
    shortcut.IconLocation = str(install_path / "browser" / "browser.exe")
    shortcut.save()

# Функция удаления ярлыков
def remove_shortcuts():
    # Удаление ярлыка с рабочего стола
    desktop_shortcut = os.path.join(desktop_path, f"{app_name}.lnk")
    if os.path.exists(desktop_shortcut):
        os.remove(desktop_shortcut)

    # Удаление ярлыка из меню Пуск
    start_menu_shortcut = os.path.join(start_menu_path, f"{app_name}.lnk")
    if os.path.exists(start_menu_shortcut):
        os.remove(start_menu_shortcut)

# Инициализация интерфейса
def init_ui():
    root = tk.Tk()
    root.title("Установщик")
    root.geometry("300x200")
    root.resizable(False, False)  # Отключаем изменение размеров окна

    # Загружаем фон (обои)
    background_image = tk.PhotoImage(file=background_image_path)
    background_label = tk.Label(root, image=background_image)
    background_label.place(relwidth=1, relheight=1)

    # Создаем контейнер для кнопок
    button_frame = tk.Frame(root, bg='#FFFFFF', bd=5)
    button_frame.place(relx=0.5, rely=0.5, anchor='center')

    if install_path.exists():
        # Если приложение установлено, показываем кнопки "Обновление" и "Удаление"
        btn_update = tk.Button(button_frame, text="Обновление", command=update_app)
        btn_update.pack(pady=10)
        
        btn_uninstall = tk.Button(button_frame, text="Удаление", command=uninstall_app)
        btn_uninstall.pack(pady=10)
    else:
        # Если приложение не установлено, показываем кнопку "Установка"
        btn_install = tk.Button(button_frame, text="Установка", command=install_app)
        btn_install.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    init_ui()
