import sys
import os
import webbrowser
 
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QGridLayout, QLineEdit, QPushButton, QTextBrowser, QSystemTrayIcon, QTableWidget, QTableWidgetItem, QStackedWidget
from PyQt5.QtGui import QIcon, QFont
 
from datetime import datetime, timedelta
 
from scraper import get_russian
from logger import get_excel_data
 
 
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
 
        self.searchButton = QPushButton("Search", self)
        self.searchButton.clicked.connect(self.search_word)
 
        self.urlButton = QPushButton("Go to page!", self)
        self.urlButton.clicked.connect(self.open_url)

        self.excelButton = QPushButton("Show excel data", self)
        self.excelButton.clicked.connect(self.show_excel)

        today = datetime.now().strftime("%Y-%m-%d")
        self.date_label = QLabel(f"Date: {today}")
        self.date_label.setAlignment(Qt.AlignRight)
 
        self.word_date_label = QLabel("Last searched on: N/A")
        self.word_date_label.setAlignment(Qt.AlignRight)
 
        self.word_counter_label = QLabel("Times searched: N/A")
        self.word_counter_label.setAlignment(Qt.AlignRight)

        self.output = QTextBrowser()
        self.table = QTableWidget()
        self.stack = QStackedWidget()
        self.stack.addWidget(self.output)
        self.stack.addWidget(self.table)
 
 
        grid = QGridLayout()
        grid.addWidget(self.label, 0, 0)
        grid.addWidget(self.entry, 0, 1)
        grid.addWidget(self.searchButton, 0, 2)
        grid.addWidget(self.date_label, 0, 3)
        grid.addWidget(self.urlButton, 1, 1)
        grid.addWidget(self.word_date_label, 1, 3)
        grid.addWidget(self.word_counter_label, 2, 3)
        grid.addWidget(self.excelButton, 2, 1)
        grid.addWidget(self.stack, 3, 0, 1, 4)
 
        central_widget.setLayout(grid)
 
    def search_word(self):
        self.excelButton.setText("Show excel data")
        self.stack.setCurrentIndex(0)

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
   
    def open_url(self):
        word = self.entry.text().strip().lower()
        url = f"https://en.wiktionary.org/wiki/{word}#Russian"
        webbrowser.open(url)

    def show_excel(self):
        if self.stack.currentIndex() == 1: #0 = HTML, 1 = Table
            self.stack.setCurrentIndex(0)
            self.excelButton.setText("Show excel data")
            return

        excel_data, max_r, max_c = get_excel_data()
        self.table.setRowCount(max_r)
        self.table.setColumnCount(max_c)
        self.table.setHorizontalHeaderLabels(excel_data[0])
        
        row_index = 0
        for data_tuple in excel_data[1:]:
            col_index = 0
            for data in data_tuple:
                self.table.setItem(row_index, col_index, QTableWidgetItem(str(data)))
                col_index += 1
            row_index += 1

        self.table.resizeColumnsToContents()
        self.stack.setCurrentIndex(1)
        self.excelButton.setText("Show current word definition")


def main():      
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(icon_path))
    font = QFont("Arial", 16)
    app.setFont(font)
 
    tray_icon = QSystemTrayIcon(QIcon(icon_path), parent=app)
    tray_icon.setVisible(True)
 
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
 
 
if __name__ == "__main__":

    main()
