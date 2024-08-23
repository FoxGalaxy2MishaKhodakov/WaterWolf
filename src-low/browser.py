import sys
import os
import configparser
import requests
import zipfile
import subprocess
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QToolBar, QAction, QTabWidget, QMessageBox, QStyleOptionTab, QStyle, QTabBar, QPushButton
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QIcon, QPainter, QPalette, QColor, QPixmap

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
    CURRENT_VERSION = "1.1.7"  # Версия текущего браузера

    def __init__(self):
        super().__init__()


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
        self.tabs.setTabBar(RoundedTabBar())
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.setCentralWidget(self.tabs)

        # Панель инструментов
        navtb = QToolBar("Navigation")
        navtb.setMovable(False)  # Запрещаем перетаскивание панели
        self.addToolBar(navtb)

        # Кнопка "Назад"
        back_btn = QAction(QIcon(os.path.join(icons_path, 'back.png')), "", self)
        back_btn.setToolTip("Back")
        back_btn.triggered.connect(self.navigate_back)
        navtb.addAction(back_btn)

        # Кнопка "Вперед"
        forward_btn = QAction(QIcon(os.path.join(icons_path, 'forward.png')), "", self)
        forward_btn.setToolTip("Forward")
        forward_btn.triggered.connect(self.navigate_forward)
        navtb.addAction(forward_btn)

        # Кнопка "Обновить"
        reload_btn = QAction(QIcon(os.path.join(icons_path, 'reload.png')), "", self)
        reload_btn.setToolTip("Reload")
        reload_btn.triggered.connect(self.reload_page)
        navtb.addAction(reload_btn)

        # Кнопка "Домой"
        home_btn = QAction(QIcon(os.path.join(icons_path, 'home.png')), "", self)
        home_btn.setToolTip("Home")
        home_btn.triggered.connect(self.navigate_home)
        navtb.addAction(home_btn)

        # Адресная строка
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navtb.addWidget(self.url_bar)

        # Кнопка "Новая вкладка"
        new_tab_btn = QAction(QIcon(os.path.join(icons_path, 'new_tab.png')), "", self)
        new_tab_btn.setToolTip("New Tab")
        new_tab_btn.triggered.connect(self.add_new_tab)
        navtb.addAction(new_tab_btn)

        # Добавляем первую вкладку
        self.add_new_tab(QUrl.fromLocalFile(os.path.join(sys.path[0], '..', 'start_page.html')), 'Home')

        # Отображаем окно
        self.show()

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
    # add_new_tab, close_current_tab, navigate_home, navigate_back, navigate_forward и т.д.
    def add_new_tab(self, qurl=None, label="New Tab"):
        # Проверяем, если URL не передан, используем стартовую страницу
        if qurl is None or not isinstance(qurl, QUrl):
            start_page_path = os.path.join(sys.path[0], '..', 'start_page.html')
            qurl = QUrl.fromLocalFile(start_page_path)
        
        # Создаем новый виджет для вкладки
        browser = QWebEngineView()
        browser.setUrl(qurl)

        # Добавляем кнопку закрытия вкладки
        close_btn = QPushButton()
        close_btn.setIcon(QIcon(os.path.join(sys.path[0], '..', 'icons', 'close.png')))
        close_btn.setIconSize(QPixmap(os.path.join(sys.path[0], '..', 'icons', 'close.png')).size())
        close_btn.setFlat(True)  # Убираем фон кнопки
        close_btn.clicked.connect(lambda: self.close_current_tab(self.tabs.indexOf(browser)))

        # Создаем вкладку с кнопкой закрытия
        i = self.tabs.addTab(browser, label)
        self.tabs.setTabText(i, label)
        self.tabs.setTabIcon(i, QIcon(os.path.join(sys.path[0], '..', 'icons', 'tab_icon.png')))
        self.tabs.tabBar().setTabButton(i, QTabBar.RightSide, close_btn)
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