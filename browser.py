import sys
import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QToolButton, QAction, QMessageBox
)
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView

class MyBrowser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyBrowseX - Enhanced Browser")
        self.setGeometry(100, 100, 1024, 768)

        self.history_log = []

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.vbox = QVBoxLayout()
        self.hbox = QHBoxLayout()
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Enter URL here...")
        self.url_bar.setFixedHeight(30)
        self.go_btn = QToolButton()
        self.go_btn.setText("Go")
        self.back_btn = QToolButton()
        self.back_btn.setText("Back")
        self.forward_btn = QToolButton()
        self.forward_btn.setText("Forward")
        self.refresh_btn = QToolButton()
        self.refresh_btn.setText("Refresh")
        self.home_btn = QToolButton()
        self.home_btn.setText("Home")

        self.hbox.addWidget(self.url_bar)
        self.hbox.addWidget(self.go_btn)
        self.hbox.addWidget(self.back_btn)
        self.hbox.addWidget(self.forward_btn)
        self.hbox.addWidget(self.refresh_btn)
        self.hbox.addWidget(self.home_btn)

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("http://www.google.com"))
        self.vbox.addLayout(self.hbox)
        self.vbox.addWidget(self.browser)
        self.central_widget.setLayout(self.vbox)

        self.go_btn.clicked.connect(lambda: self.navigate(self.url_bar.text()))
        self.back_btn.clicked.connect(self.browser.back)
        self.forward_btn.clicked.connect(self.browser.forward)
        self.refresh_btn.clicked.connect(self.browser.reload)
        self.home_btn.clicked.connect(self.navigate_home)
        self.browser.urlChanged.connect(lambda url: self.url_bar.setText(url.toString()))

        self.create_menu()

    def create_menu(self):
        menubar = self.menuBar()
        history_menu = menubar.addMenu("History")
        view_history = QAction("View History", self)
        view_history.triggered.connect(self.show_history)
        history_menu.addAction(view_history)

    def log_history(self, url: str) -> None:
        timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        entry = f"{timestamp} {url}"
        self.history_log.append(entry)

    def show_history(self):
        history_text = "\n".join(self.history_log) if self.history_log else "No history yet."
        QMessageBox.information(self, "Browsing History", history_text)

    def normalize_url(self, url: str) -> str:
        if not url.startswith(("http://", "https://")):
            return "http://" + url
        return url

    def navigate(self, url: str):
        normalized_url = self.normalize_url(url)
        self.url_bar.setText(normalized_url)
        self.browser.setUrl(QUrl(normalized_url))
        self.log_history(normalized_url)

    def navigate_home(self):
        home_url = "http://www.google.com"
        self.url_bar.setText(home_url)
        self.browser.setUrl(QUrl(home_url))
        self.log_history(home_url)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyBrowser()
    window.show()
    sys.exit(app.exec_())
