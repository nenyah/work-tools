from datetime import datetime

import pandas as pd
import pymongo

from config import (DAZHONG_COLLECTION, DAZHONG_DB, MONGODB_COLLECTION,
                    MONGODB_DB, MONGODB_HOST, MONGODB_POST)

client = pymongo.MongoClient(MONGODB_HOST, MONGODB_POST)
tianmao = client[MONGODB_DB]
dianping = client[DAZHONG_DB]
tianmao_yeevar = tianmao[MONGODB_COLLECTION]
dianping_yeevar = dianping[DAZHONG_COLLECTION]


def out_to_csv(date, file, collection):
    df = pd.DataFrame(collection.find())
    df = df[df['crawl_date'] == date]
    df.to_csv(file)


KEYWORD = '伊婉'
_path = r"E:\玻尿酸销售情况"
today = datetime.today().strftime('%Y-%m-%d')
for site in ['天猫', '点评']:
    file = f'{_path}/{today}{KEYWORD}{site}销售情况.csv'
    if site == '天猫':
        collection = tianmao_yeevar
    else:
        collection = dianping_yeevar
    out_to_csv(today, file, collection)
