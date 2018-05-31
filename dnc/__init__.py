from dnc.tools import read_page, KST
from dnc.exceptions import ArticleNotFound

from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker

import time

from datetime import timedelta, datetime
from multiprocessing import Pool

from dnc.schema import Article, Base
from dnc.tools import get_aids, read_page


def crawl_organization_with_postgres(oid, start_date, end_date, db_path):
    engine = create_engine(db_path)
    Base.metadata.create_all(engine)

    Session = sessionmaker()
    Session.configure(bind=engine)

    session = Session()

    count = 0
    buf = list()

    date = start_date
    while date >= end_date:
        print('Date: {}'.format(date.strftime('%Y-%m-%d')))
        try:
            aids = get_aids(oid, date)
        except ArticleNotFound:
            break

        with Pool(5) as p:
            articles = p.map(read_page, aids)
        
        for a in articles:
            a['oid'] = oid
            session.merge(Article(**a))
            count += 1
        session.commit()
        date -= timedelta(days=1)

    session.close()
    return count
