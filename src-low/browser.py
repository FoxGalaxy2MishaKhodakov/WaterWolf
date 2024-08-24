import sys
import os
import configparser
import requests
import zipfile
import subprocess
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget, QLineEdit, QToolBar, QAction, QTabWidget, QMessageBox, QStyleOptionTab, QStyle, QTabBar, QPushButton
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QIcon, QPainter, QPalette, QColor, QPixmap
from PyQt5 import QtCore

class RoundedTabBar(QTabBar):
    def paintEvent(self, event):
        painter = QPainter(self)
        option = QStyleOptionTab()

        for i in range(self.count()):
            self.initStyleOption(option, i)
            # Округление вкладок на 20%
            option.rect = self.tabRect(i)
            painter.setRenderHint(QPainter.Antialiasing, True)
            painter.setBrush(option.palette.window())
            painter.setPen(Qt.NoPen)
            rounded_rect = option.rect.adjusted(5, 5, -5, -5)
            painter.drawRoundedRect(rounded_rect, rounded_rect.height() * 0.2, rounded_rect.height() * 0.2)
            self.style().drawControl(QStyle.CE_TabBarTabLabel, option, painter)

    def tabSizeHint(self, index):
        size = super().tabSizeHint(index)
        size.setHeight(35)  # Высота вкладки
        size.setWidth(120)  # Ширина вкладки
        return size

class Browser(QMainWindow):
    GITHUB_REPO = "FoxGalaxy2MishaKhodakov/WaterWolf"  # Замените на ваше имя пользователя и репозиторий
    CURRENT_VERSION = "1.2.2"  # Версия текущего браузера

    def __init__(self):
        super().__init__()

        # Убираем стандартную панель заголовка окна
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)

        # Устанавливаем минимальные размеры для окна
        self.setMinimumSize(800, 600)

        # Путь к конфигурационным файлам
        self.config = configparser.ConfigParser()
        config_path = os.path.join(sys.path[0], '..', 'config.ini')
        self.config.read(config_path)

        # Устанавливаем путь к папке с иконками, которая находится на одну директорию ниже
        icons_path = os.path.join(sys.path[0], '..', 'icons')

        # Проверяем обновления при запуске
        self.check_for_updates()

        # Создаем виджет с вкладками
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.setCentralWidget(self.tabs)

        # Создаем кастомную панель заголовка
        self.create_custom_title_bar()

        # Добавляем первую вкладку
        self.add_new_tab(QUrl.fromLocalFile(os.path.join(sys.path[0], '..', 'start_page.html')), 'Home')

        # Отображаем окно
        self.show()

    def create_custom_title_bar(self):
        # Создаем кастомную панель заголовка
        title_bar = QWidget()
        title_bar.setObjectName("title_bar")
        title_bar.setStyleSheet("""
            #title_bar {
                background-color: #2E2E2E;
                color: white;
                padding: 5px;
            }
            QPushButton {
                background-color: #4A4A4A;
                border: none;
                color: white;
                padding: 5px;
                margin: 2px;
            }
            QPushButton:hover {
                background-color: #6A6A6A;
            }
        """)
        title_bar_layout = QHBoxLayout()

        # Кнопка "Назад"
        back_btn = QPushButton("←")
        back_btn.clicked.connect(self.navigate_back)
        title_bar_layout.addWidget(back_btn)

        # Кнопка "Вперед"
        forward_btn = QPushButton("→")
        forward_btn.clicked.connect(self.navigate_forward)
        title_bar_layout.addWidget(forward_btn)

        # Кнопка "Обновить"
        reload_btn = QPushButton("↻")
        reload_btn.clicked.connect(self.reload_page)
        title_bar_layout.addWidget(reload_btn)

        # Кнопка "Домой"
        home_btn = QPushButton("🏠")
        home_btn.clicked.connect(self.navigate_home)
        title_bar_layout.addWidget(home_btn)

        # Адресная строка
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        title_bar_layout.addWidget(self.url_bar)

        # Кнопки управления окном
        minimize_btn = QPushButton("–")
        maximize_btn = QPushButton("[]")
        close_btn = QPushButton("X")

        minimize_btn.clicked.connect(self.showMinimized)
        maximize_btn.clicked.connect(self.toggle_maximized)
        close_btn.clicked.connect(self.close)

        title_bar_layout.addWidget(minimize_btn)
        title_bar_layout.addWidget(maximize_btn)
        title_bar_layout.addWidget(close_btn)

        title_bar.setLayout(title_bar_layout)

        # Устанавливаем кастомную панель заголовка
        self.setMenuWidget(title_bar)

        # Подключаем обработчик событий для перетаскивания окна
        title_bar.mousePressEvent = self.mouse_press_event
        title_bar.mouseMoveEvent = self.mouse_move_event

    def mouse_press_event(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.globalPos()

    def mouse_move_event(self, event):
        if event.buttons() & Qt.LeftButton:
            delta = event.globalPos() - self.drag_start_position
            self.move(self.pos() + delta)
            self.drag_start_position = event.globalPos()

    def toggle_maximized(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def tab_open_doubleclick(self, index):
        if index == -1:  # Если дважды щелкнули по пустому пространству вкладок
            self.add_new_tab()

    def add_new_tab(self, qurl=None, label="New Tab"):
        if qurl is None or not isinstance(qurl, QUrl):
            start_page_path = os.path.join(sys.path[0], '..', 'start_page.html')
            qurl = QUrl.fromLocalFile(start_page_path)

        browser = QWebEngineView()
        browser.setUrl(qurl)

        close_btn = QPushButton()
        close_btn.setIcon(QIcon(os.path.join(sys.path[0], '..', 'icons', 'close.png')))
        close_btn.setIconSize(QPixmap(os.path.join(sys.path[0], '..', 'icons', 'close.png')).size())
        close_btn.setFlat(True)
        close_btn.clicked.connect(lambda: self.close_current_tab(self.tabs.indexOf(browser)))

        i = self.tabs.addTab(browser, label)
        self.tabs.setTabText(i, label)

        # Заменяем иконку сайта
        browser.iconChanged.connect(lambda icon, i=i: self.tabs.setTabIcon(i, icon))

        self.tabs.tabBar().setTabButton(i, QTabBar.RightSide, close_btn)
        self.tabs.setCurrentIndex(i)

        browser.urlChanged.connect(lambda qurl, browser=browser: self.update_urlbar(qurl, browser))
        browser.titleChanged.connect(lambda title, browser=browser: self.update_tab_title(title, browser))

        self.update_urlbar(qurl, browser)

    def close_current_tab(self, i):
        if self.tabs.count() > 1:
            self.tabs.removeTab(i)

    def navigate_home(self):
        start_page_path = os.path.join(sys.path[0], '..', 'start_page.html')
        start_page_url = QUrl.fromLocalFile(start_page_path)
        self.tabs.currentWidget().setUrl(start_page_url)

    def navigate_back(self):
        if self.tabs.currentWidget():
            self.tabs.currentWidget().back()

    def navigate_forward(self):
        if self.tabs.currentWidget():
            self.tabs.currentWidget().forward()

    def reload_page(self):
        if self.tabs.currentWidget():
            self.tabs.currentWidget().reload()

    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith('http'):
            # Если в адресе нет http, то считаем его поисковым запросом
            url = f'{self.get_search_engine_url()}{url}'
        self.tabs.currentWidget().setUrl(QUrl(url))

    def update_tab_title(self, title, browser):
        if browser == self.tabs.currentWidget():
            self.setWindowTitle(title)
        index = self.tabs.indexOf(browser)
        if index != -1:
            self.tabs.setTabText(index, title)

    def update_urlbar(self, qurl, browser=None):
        if browser == self.tabs.currentWidget():
            self.url_bar.setText(qurl.toString())

    def current_tab_changed(self, i):
        qurl = self.tabs.currentWidget().url()
        self.update_urlbar(qurl, self.tabs.currentWidget())

    def check_for_updates(self):
        try:
            response = requests.get(f"https://api.github.com/repos/{self.GITHUB_REPO}/releases/latest")
            latest_release = response.json()
            latest_version = latest_release["tag_name"]
            if latest_version > self.CURRENT_VERSION:
                reply = QMessageBox.question(
                    self, "Обновление доступно",
                    f"Вышла новая версия {latest_version}. Обновить сейчас?",
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No
                )
                if reply == QMessageBox.Yes:
                    asset_url = None
                    for asset in latest_release["assets"]:
                        if asset["name"] == "update.zip":
                            asset_url = asset["browser_download_url"]
                            break

                    if asset_url:
                        self.download_and_install_update(asset_url, latest_version)
                    else:
                        QMessageBox.critical(self, "Ошибка", "Не удалось найти файл update.zip в последнем релизе.")
        except Exception as e:
            print(f"Ошибка при проверке обновлений: {e}")

    def download_and_install_update(self, url, latest_version):
        updater_dir = os.path.join(sys.path[0], '..', '..')
        update_zip_path = os.path.join(updater_dir, "update.zip")

        try:
            # Загружаем update.zip
            with requests.get(url, stream=True) as r:
                with open(update_zip_path, 'wb') as f:
                    total_length = r.headers.get('content-length')
                    if total_length is None:  # Нет информации о размере
                        f.write(r.content)
                    else:
                        dl = 0
                        total_length = int(total_length)
                        for chunk in r.iter_content(chunk_size=8192):
                            if chunk:
                                dl += len(chunk)
                                f.write(chunk)
                                done = int(50 * dl / total_length)
                                print(f"\rЗагрузка обновления: [{'=' * done}{' ' * (50-done)}] {2*done}%")

            # Запускаем update.bat для установки обновления
            update_bat_path = os.path.join(updater_dir, "update.bat")
            subprocess.Popen([update_bat_path], shell=True)

            # Закрываем приложение
            sys.exit()

        except Exception as e:
            print(f"Ошибка при загрузке и установке обновления: {e}")

    def get_search_engine_url(self):
        # Определяем поисковую систему из конфигурации
        search = self.config.get('Settings', 'search', fallback='google')
        if search == 'google':
            return 'https://www.google.com/search?q='
        elif search == 'duckduckgo':
            return 'https://duckduckgo.com/?q='
        else:
            return 'https://www.google.com/search?q='

if __name__ == '__main__':
    app = QApplication(sys.argv)
    browser = Browser()
    app.exec_()
