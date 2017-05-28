import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone

from dnc.exceptions import ArticleNotFound

KST = timezone(timedelta(hours=9), 'KST')


def get_aids(oid, date):
    aids = list()
    page = 1

    while True:
        g = requests.get('http://media.daum.net/cp/{}?page={}&regDate={}'.format(oid, page, date.strftime('%Y%m%d')))
        html = BeautifulSoup(g.text, 'html.parser')

        none = html.find('p', 'txt_none')
        if none is not None:
            break

        aids_in_page = [tit.a['href'].split('/')[-1] for tit in html.find_all('strong', 'tit_thumb')]
        aids.extend(aids_in_page)

        page += 1

    return aids


def read_page(aid):
    g = requests.get('http://v.media.daum.net/v/{}'.format(aid))
    html = BeautifulSoup(g.text, 'html.parser')

    error = html.find('p', 'desc_empty')
    if error is not None:
        raise ArticleNotFound

    if 'life' in g.url:
        title = html.find('div', 'tit_subject').get_text().strip()
        contents = html.find('div', id='dmcfContents')
    else:
        title = html.find('h3', 'tit_view').get_text().strip()
        contents = html.find('div', 'article_view')


    title = title.replace('\0', '')

    contents = ' '.join(list(filter(lambda x: x.strip() != '\n', contents.strings))).strip()
    contents = re.sub(' +', ' ', contents)
    contents = contents.replace('\0', '')
    contents = contents.replace('\n', '')


    timestamp = datetime.strptime(str(aid)[:14], '%Y%m%d%H%M%S')
    timestamp = timestamp.replace(tzinfo=KST)


    return {
        'aid': aid,
        'title': title,
        'time': timestamp,
        'contents': contents
    }
