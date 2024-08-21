import sys
import configparser
import os
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QToolBar, QAction
from PyQt5.QtWebEngineWidgets import QWebEngineView

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()

        # Загружаем конфигурацию
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.search_engine = self.get_search_engine_url()

        # Настройка окна браузера
        self.browser = QWebEngineView()

        # Получаем абсолютный путь к файлу стартовой страницы
        start_page_path = os.path.join(sys.path[0], 'start_page.html')
        start_page_url = QUrl.fromLocalFile(start_page_path)
        self.browser.setUrl(start_page_url)

        self.setCentralWidget(self.browser)

        # Панель инструментов
        navtb = QToolBar("Navigation")
        self.addToolBar(navtb)

        # Адресная строка
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navtb.addWidget(self.url_bar)

        # Кнопка "Назад"
        back_btn = QAction("Back", self)
        back_btn.triggered.connect(self.browser.back)
        navtb.addAction(back_btn)

        # Кнопка "Вперед"
        forward_btn = QAction("Forward", self)
        forward_btn.triggered.connect(self.browser.forward)
        navtb.addAction(forward_btn)

        # Кнопка "Обновить"
        reload_btn = QAction("Reload", self)
        reload_btn.triggered.connect(self.browser.reload)
        navtb.addAction(reload_btn)

        # Кнопка "Домой"
        home_btn = QAction("Home", self)
        home_btn.triggered.connect(self.navigate_home)
        navtb.addAction(home_btn)

        # Отображаем окно
        self.show()

    def navigate_home(self):
        start_page_path = os.path.join(sys.path[0], 'start_page.html')
        start_page_url = QUrl.fromLocalFile(start_page_path)
        self.browser.setUrl(start_page_url)

    def navigate_to_url(self):
        url = self.url_bar.text()
        if "http" not in url:
            # Если в адресе нет http, то считаем его поисковым запросом
            url = f'{self.search_engine}{url}'
        self.browser.setUrl(QUrl(url))

    def get_search_engine_url(self):
        # Определяем поисковую систему
        search = self.config.get('Settings', 'search', fallback='google')
        if search == 'google':
            return 'https://www.google.com/search?q='
        elif search == 'duckduckgo':
            return 'https://duckduckgo.com/?q='
        else:
            return 'https://www.google.com/search?q='

if __name__ == '__main__':
    app = QApplication(sys.argv)
    QApp = Browser()
    app.exec_()
