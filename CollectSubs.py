from bs4 import BeautifulSoup
import requests

url = "https://stackexchange.com/sites#"
html_doc = requests.get(url).text
StackExchange = BeautifulSoup(html_doc, "html.parser")

links = []  # list of all stackexchange links

for a in StackExchange.body.find_all('a', href=True):
    s = a['href']
    if s.startswith('https://') and s not in links and s.count('/') == 2 and s.endswith('.com') and s.count('?') == 0:
        links.append(a['href'])

file = open('SE.txt','a+')
for i in links:
    file.write(i + '\n')
file.close()