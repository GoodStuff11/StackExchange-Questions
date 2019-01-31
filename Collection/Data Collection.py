from bs4 import BeautifulSoup
import requests


def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

sep = '|   |'
file = open('../Data/SE Questions.txt', 'w+', encoding='utf-8')
file.write('SE'+sep+'link'+sep+'title'+sep+'votes\n')
with open('../Data/SE.txt', 'r') as SEfile:
    links = SEfile.readlines()


for n, url in enumerate(links[:20]):
    votes_list = []
    title_list = []
    url_list = []

    url = url[:-1]
    html_doc = requests.get(url).text
    sub = BeautifulSoup(html_doc, "html.parser")
    title = sub.title.string

    for page in range(1,100):
        print(n, page)
        html_doc = requests.get(url + '/questions?sort=newest&page=' + str(page)).text
        sub = BeautifulSoup(html_doc, "html.parser")
        try:
            for i, a in enumerate(sub.body.find_all('strong')):
                if i % 2 == 0 and RepresentsInt(a.string):
                    votes_list.append(a.string)
            for a in sub.body.find_all('a', href=True):
                s = a['href']
                if s.startswith('/questions/') and '/tagged/' not in s and not s.endswith('/ask'):
                    url_list.append(url + s)
            for a in sub.body.find_all('a', class_="question-hyperlink"):
                if a.string == a.string.strip():
                    title_list.append(a.string)
        except AttributeError:
            pass

        assert len(votes_list) == len(title_list) == len(url_list), str(len(votes_list)) + ',' + str(
            len(title_list)) + ',' + str(len(url_list))
    # add to file
    for j in range(len(url_list)):
        file.write(title + sep + url_list[j] + sep + title_list[j] + sep + votes_list[j] + '\n')

file.close()
