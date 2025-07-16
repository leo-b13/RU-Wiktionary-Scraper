import sys
import os

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QGridLayout, QLineEdit, QPushButton, QTextBrowser, QSystemTrayIcon
from PyQt5.QtGui import QIcon, QFont

from datetime import datetime, timedelta

from scraper import get_russian

'''
Things to maybe add:
Go back to previous word (only one?)
Show colors how for how many times you've google it + counter itself (l) and last time searched + if new word say "New word!"
Make a quizlet (? optional)
Go to page itself button -> opens up url for you
'''

if hasattr(sys, '_MEIPASS'):
    icon_path = os.path.join(sys._MEIPASS, 'ru_flag.ico')
else:
    icon_path = 'ru_flag.ico'  # fallback for running as .py


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Russian Wiktionary Scraper")
        self.setGeometry(0, 0, 1500, 1500)
        self.setWindowIcon(QIcon(icon_path))    
 
        self.initUI()
 
    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
 
        self.label = QLabel("Enter a russian word:", self)
 
        self.entry = QLineEdit()
        self.entry.setPlaceholderText("e.g. кошка")
 
        self.button = QPushButton("Search", self)
        self.button.clicked.connect(self.search_word)
       
        today = datetime.now().strftime("%Y-%m-%d")
        self.date_label = QLabel(f"Date: {today}")
        self.date_label.setAlignment(Qt.AlignRight)

        self.word_date_label = QLabel("Last searched on: N/A")
        self.date_label.setAlignment(Qt.AlignRight)

        self.word_counter_label = QLabel("Times searched: N/A")

        self.output = QTextBrowser()
 

        grid = QGridLayout()
        grid.addWidget(self.label, 0, 0)
        grid.addWidget(self.entry, 0, 1)
        grid.addWidget(self.button, 0, 2)
        grid.addWidget(self.date_label, 0, 3)
        grid.addWidget(self.word_date_label, 1, 3)
        grid.addWidget(self.word_counter_label, 1, 0)
        grid.addWidget(self.output, 3, 0, 1, 4)
 
        central_widget.setLayout(grid)

    def search_word(self):
        word = self.entry.text().strip().lower()
        if not word:
            self.output.setText("[ERROR] Please enter a word.")
            return

        try:
            result, word_date, word_counter = get_russian(word)
            if not result:
                self.output.setText("[ERROR] No Russian section found.")
                return
            self.output.setHtml(result)
            self.word_date_label.setText(f"Last searched on: {word_date}")
            self.word_counter_label.setText(f"Times searched: {word_counter}")

        except Exception as e:
            self.output.setText(f"[ERROR] {str(e)}")
        

def main():      
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(icon_path))

    tray_icon = QSystemTrayIcon(QIcon(icon_path), parent=app)
    tray_icon.setVisible(True)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

 
if __name__ == "__main__":
    main()