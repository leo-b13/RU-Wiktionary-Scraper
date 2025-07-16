# RU-Wiktionary-Scraper
Scraper that grabs russian section of an entered word from wiktionary.

![Russian flag with a magnifying glass](https://myoctocat.com/assets/images/base-octocat.svg)

It additionally tracks the words you searched through an excel sheet and displays the times you've searched the word and last time you searched it.

Run this command to generate an .exe:
> pyinstaller --onefile --windowed --icon=ru_flag.ico --add-data "ru_flag.ico;." --name WiktionaryScraper main.py

Depending on where the exe is, it will create a new "russian_words_log" excel sheet if it is unable to find one.
