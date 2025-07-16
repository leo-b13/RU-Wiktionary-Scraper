import requests
from bs4 import BeautifulSoup, Tag
from logger import load2excel

def get_russian(userInput):
    url = f"https://en.wiktionary.org/wiki/{userInput}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
 
    #1 - Locate the Russian section
    russian_section = None
    russian_section = soup.find("h2", id="Russian")
    if not russian_section:
        print("[ERROR] Russian section not found")
        return
    print("Russian section found!")
    russian_section.string = f"Definitions for: {userInput}"
    word_date, word_counter = load2excel(userInput) 
    russian_section = russian_section.parent 


    #2 - Remove "edit" text, and all hyperlinks
    for span in soup.find_all("span", class_="mw-editsection"):
        span.decompose()
    for link in soup.find_all("a"):
        link.unwrap()


    #3 - Loop through the Russian section, adding wanted parts to a list, skipping unwanted parts, and returning it
    content = []
    sections_to_skip = ["Descendants", "Etymology", "Alternative forms", "Pronunciation", "Derived terms", "Anagrams", "References", "Further reading"]
    skipSection = False
    content.append(russian_section)

    for sibling in russian_section.next_siblings: 
        if isinstance(sibling, Tag): 
            #print('TAG:', sibling.name, repr(sibling.get_text(strip=True)))

            if sibling.next_element.name == "h2":
                #print(sibling.next_element)
                break

            if skipSection:
                if isinstance(sibling.next_element, Tag) and sibling.next_element.name in ("h4", "h3"):
                    skipSection = False
                else:
                    continue

            if any(section in sibling.get_text() for section in sections_to_skip):
                #print(f"Skipping section: {sibling.get_text()}")
                skipSection = True
                continue

            content.append(sibling)       
    return "".join(str(tag) for tag in content), word_date, word_counter
