# RU-Wiktionary-Scraper
Scraper that grabs russian section of an entered word from wiktionary

Run this command to generate an .exe:
pyinstaller --onefile --windowed --icon=ru_flag.ico --add-data "ru_flag.ico;." --name WiktionaryScraper main.py

Depending on where the exe is, it will create a new "russian_words_log" excel sheet if it is unable to find one.
