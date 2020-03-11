#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pymongo

MONGO_URL = 'localhost'
MONGO_TAOBAO = 'taobao'
MONGO_MEITUAN = 'meituan'
MONGO_COLLECTION = 'products'
client = pymongo.MongoClient(MONGO_URL)
