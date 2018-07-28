# encoding: utf-8

import requests
import pandas as pd
from bs4 import BeautifulSoup
from collections import Counter
import re

title_regexp = re.compile(r'title = {(.*)},')
author_regexp = re.compile(r'author = {(.*)}')

with open('skip_words.txt') as f:
    skip_words = set([_.strip() for _ in f])

cnt = Counter()
url = 'http://openaccess.thecvf.com/CVPR2018.py'
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
paper_bib_text_list = soup.find_all('div', class_='bibref')
print 'Total number of papers: ', len(paper_bib_text_list)
for paper_bib_text in paper_bib_text_list:
    text = paper_bib_text.get_text()
    title = title_regexp.search(text).group(1)
    words = title.lower().split()
    for word in words:
        word = re.sub(r'\W+', '', word)
        if word and word not in skip_words:
            cnt[word] += 1

d = list()
for word, freq in cnt.most_common():
    d.append(
        {
            'keyword': word,
            'frequency': freq
        }
    )

pd.DataFrame(d).to_csv('output_keywords.csv', header=True, columns=['keyword', 'frequency'], index=False,
                       encoding='utf-8')
