#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @File    :   mongo_utils.py
# @Time    :   2022/3/1 14:04
# @Author  :   Jianbin Li
# @Version :   1.0
# @Contact :   jianbin0410@gmail.com
# @Desc    :

# here put the import lib
import pymongo


class Mongo(object):

    def __init__(self, uri, db_name='research'):
        self.db_name = db_name
        self.client = pymongo.MongoClient(
            uri, connect=False, appname='research')
        self.db = self.client[db_name]

    def __del__(self):
        self.client.close()


class MongoContext(object):

    def __init__(self, uri, col, db='research'):
        self.uri = uri
        self.col = col
        self.db = db

    def __enter__(self):
        self.client = pymongo.MongoClient(
            self.uri, connect=False, appname=self.col)
        return self.client[self.db][self.col]

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()
