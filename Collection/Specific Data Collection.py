from bs4 import BeautifulSoup
import requests


def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


sep = '|   |'
file = open('../Data/SE Questions Physics.txt', 'w+', encoding='utf-8')
file.write('link' + sep + 'title' + sep + 'votes' + sep + 'answers' + sep + 'views' + sep + 'time\n')

url = 'https://physics.stackexchange.com'

html_doc = requests.get(url + '/questions?pagesize=50').text
sub = BeautifulSoup(html_doc, "html.parser")
# number of pages
n = int(sub.body.find_all(class_='page-numbers')[-2].string)

for page in range(1, n):
    votes_list = []
    title_list = []
    url_list = []
    answers_list = []
    views_list = []
    time_list = []

    wiki = [0 for x in range(50)]

    html_doc = requests.get(url + '/questions?pagesize=50?sort=newest&page=' + str(page)).text
    sub = BeautifulSoup(html_doc, "html.parser")
    try:
        count = 0
        for i, a in enumerate(sub.body.find_all('div', class_='user-details')):
            if a.next_sibling is not None:
                if str(a.next_sibling).strip() != '':
                    count += 1
                    wiki[i - count] = 1
        for i, a in enumerate(sub.body.find_all('strong')):
            if i % 2 == 0 and RepresentsInt(a.string):
                votes_list.append(a.string)
        for a in sub.body.find_all('a', href=True):
            s = a['href']
            if s.startswith('/questions/') and '/tagged/' not in s and not s.endswith('/ask'):
                url_list.append(url + s)
        for a in sub.body.find_all('a', class_="question-hyperlink"):
            if a.string.count('\n') == 0:
                title_list.append(a.string.strip())
        for i, a in enumerate(sub.body.find_all('strong')):
            if i % 2 == 1 and RepresentsInt(a.string):
                answers_list.append(a.string)
        for a in sub.body.find_all('span', class_='relativetime'):
            time_list.append(a['title'][:-1])
        for a in sub.body.find_all('div', class_='views'):
            views_list.append(a['title'].replace(',', '')[:-6])

        # filling in posts with no date
        for k in range(50):
            if wiki[k] == 1:
                time_list.insert(k+1, '')
        print(page / n * 100, '%')
    except AttributeError:
        pass

    assert len(votes_list) == len(title_list) == len(url_list) == len(time_list), str(len(votes_list)) + ',' + str(
        len(title_list)) + ',' + str(len(url_list)) + ',' + str(len(time_list))
    # add to file
    for j in range(len(url_list)):
        file.write(
            url_list[j] + sep + title_list[j] + sep + votes_list[j] + sep + answers_list[j] + sep + views_list[
                j] + sep + time_list[j] + '\n')

file.close()
