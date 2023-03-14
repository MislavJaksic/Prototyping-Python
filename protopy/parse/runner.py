from bs4 import BeautifulSoup

with open("protopy/parse/data/index.htm", "r", encoding="utf-8") as fp:
    soup = BeautifulSoup(fp)

counter = 0
for link in soup.find_all('a'):
    if link.get("title") == "Show document details":
        counter = counter + 1
        print("{},{}".format(counter, link.text.replace("\n", " ")), end=",")
    if link.get("title") == "Show source title details":
        print("{}".format(link.text.replace("\n", " ")))
    if counter > 1000:
        break
