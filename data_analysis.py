import pandas
import requests
from bs4 import BeautifulSoup
from pprint import pprint

f = open("storytext.txt", "w")
NUMPAGES = 53
for i in range(0, NUMPAGES):
    url = ""
    data = requests.get(url)
    # print(data.text)
    html = BeautifulSoup(data.text, "html.parser")
    story = html.select(".storyText")
    text = ""
    for st in story:
        text += st.get_text() + " "
    newtext = text.replace("“", '"')
    newtext = newtext.replace("”", '"')
    newtext = newtext.replace("/", "/")
    newtext = newtext.replace("’", "'")
    newtext = newtext.replace(":", ":")
    newtext = newtext.replace("&ensp;", "    ")
    newtext = newtext.replace("<br/>", "\n")
    newtext = newtext.replace("&amp;", "&")
    newtext = newtext.replace("ensp", "    ")
    try:
        f.write(str(newtext))
    except:
        print("---------------------- " + str(i))
        f.write("[MANUAL REPLACE: PAGE" + str(i) + "]")
        print(newtext)
