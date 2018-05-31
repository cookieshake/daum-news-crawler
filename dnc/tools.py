import re
import requests
from requests_futures.sessions import FuturesSession
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone

from dnc.exceptions import ArticleNotFound

KST = timezone(timedelta(hours=9), 'KST')
session = FuturesSession(max_workers=10)

def get_aids(oid, date):
    aids = list()
    offset = 1

    while True:

        results = [
            session.get('http://media.daum.net/cp/{}?page={}&regDate={}'.format(oid, page, date.strftime('%Y%m%d')))
            for page in range(offset, offset + 10)
        ]

        for g in results:
            g = g.result()
            html = BeautifulSoup(g.text, 'html.parser')
            none = html.find('p', 'txt_none')
            if none is not None:
                return aids

            aids_in_page = [tit.a['href'].split('/')[-1] for tit in html.find_all('strong', 'tit_thumb')]
            aids.extend(aids_in_page)
  
        offset += 10


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

    regDate = html.find('meta',  property='og:regDate')['content']
    timestamp = datetime.strptime(regDate[:14], '%Y%m%d%H%M%S')
    timestamp = timestamp.replace(tzinfo=KST)


    return {
        'aid': aid,
        'title': title,
        'time': timestamp,
        'contents': contents
    }
