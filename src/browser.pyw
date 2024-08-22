import sys
import os
import configparser
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QToolBar, QAction, QTabWidget, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()

        # Загружаем конфигурацию
        self.config = configparser.ConfigParser()
        config_path = os.path.join(sys.path[0], '..', 'config.ini')
        self.config.read(config_path)
        self.search_engine = self.get_search_engine_url()

        # Создаем виджет с вкладками
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.setCentralWidget(self.tabs)

        # Панель инструментов
        navtb = QToolBar("Navigation")
        self.addToolBar(navtb)

        # Кнопка "Назад"
        back_btn = QAction("Back", self)
        back_btn.triggered.connect(self.navigate_back)
        navtb.addAction(back_btn)

        # Кнопка "Вперед"
        forward_btn = QAction("Forward", self)
        forward_btn.triggered.connect(self.navigate_forward)
        navtb.addAction(forward_btn)

        # Кнопка "Обновить"
        reload_btn = QAction("Reload", self)
        reload_btn.triggered.connect(self.reload_page)
        navtb.addAction(reload_btn)

        # Кнопка "Домой"
        home_btn = QAction("Home", self)
        home_btn.triggered.connect(self.navigate_home)
        navtb.addAction(home_btn)

        # Адресная строка
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navtb.addWidget(self.url_bar)

        # Кнопка "Новая вкладка"
        new_tab_btn = QAction("New Tab", self)
        new_tab_btn.triggered.connect(self.add_new_tab)
        navtb.addAction(new_tab_btn)

        # Добавляем первую вкладку
        self.add_new_tab(QUrl.fromLocalFile(os.path.join(sys.path[0], '..', 'start_page.html')), 'Home')

        # Отображаем окно
        self.show()

    def add_new_tab(self, qurl=None, label="New Tab"):
        # Проверяем, если URL не передан, используем стартовую страницу
        if qurl is None or not isinstance(qurl, QUrl):
            start_page_path = os.path.join(sys.path[0], '..', 'start_page.html')
            qurl = QUrl.fromLocalFile(start_page_path)
        
        # Создаем новый виджет для вкладки
        browser = QWebEngineView()
        browser.setUrl(qurl)

        # Добавляем вкладку в виджет с вкладками
        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)

        # Обновляем адресную строку при переключении вкладок
        browser.urlChanged.connect(lambda qurl, browser=browser: self.update_urlbar(qurl, browser))

        # Устанавливаем фокус на новую вкладку
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
            url = f'{self.search_engine}{url}'
        self.tabs.currentWidget().setUrl(QUrl(url))

    def update_urlbar(self, qurl, browser=None):
        if browser == self.tabs.currentWidget():
            self.url_bar.setText(qurl.toString())

    def current_tab_changed(self, i):
        qurl = self.tabs.currentWidget().url()
        self.update_urlbar(qurl, self.tabs.currentWidget())

    def tab_open_doubleclick(self, i):
        if i == -1:  # Если дважды щелкнули по пустому пространству вкладок, создается новая вкладка
            self.add_new_tab()

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
