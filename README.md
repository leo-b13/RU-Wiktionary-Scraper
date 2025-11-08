# RU-Wiktionary-Scraper
Scraper that grabs russian section of an entered word from wiktionary.

![Russian flag with a magnifying glass](/assets/ru_flag.png)

It additionally tracks the words you searched through an excel sheet and displays the times you've searched the word and last time you searched it.
<br>
<br>
Planned future functionality includes: Button to show words from this week/month/year, button to create a quizlet of flashcards from selected words/definitions, dark/light theme toggle

# Download 
Download [here](https://github.com/leo-b13/RU-Wiktionary-Scraper/releases)

<br> Depending on where the exe is, it will create a new "russian_words_log" excel sheet if it is unable to find one.

## Additional Info
If you want to generate an .exe yourself, run this command:
> pyinstaller --onefile --windowed --icon=ru_flag.ico --add-data "ru_flag.ico;." --name WiktionaryScraper main.py


