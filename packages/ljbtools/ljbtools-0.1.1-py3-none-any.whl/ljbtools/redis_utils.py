#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @File    :   redis_utils.py
# @Time    :   2023/1/5 16:41
# @Author  :   Jianbin Li
# @Version :   1.0
# @Contact :   jianbin0410@gmail.com
# @Desc    :

# here put the import lib
import json
import redis
import umsgpack


class RedisCli(object):

    def __init__(self, config) -> None:
        password = config.get('password', None)
        if config.get('cluster_nodes') is None:
            pool = redis.ConnectionPool(host=config['host'], port=config['port'], password=password,
                                        db=config['db'], max_connections=config.get('max_connections', 50))
            self.redis = redis.Redis(connection_pool=pool)
        else:
            from rediscluster import RedisCluster
            startup_nodes = config["cluster_nodes"]
            self.redis = RedisCluster(host=startup_nodes[0]['host'], port=startup_nodes[0]['port'], password=password,
                                      skip_full_coverage_check=True, max_connections=config.get('max_connections', 50))

    @staticmethod
    def _check_data(data):
        return data.decode('utf-8') if data is not None else None

    def get(self, key):
        return self._check_data(self.redis.get(key))

    def setex(self, key, value, ex):
        self.redis.setex(key, ex, value)

    def set(self, key, value):
        self.redis.set(key, value)

    def hset(self, key, field, value):
        self.redis.hset(key, field, value)

    def hget(self, key, field):
        return self._check_data(self.redis.hget(key, field))

    def hkeys(self, key):
        return self.redis.hkeys(key)

    def qsize(self, key):
        return self.redis.llen(key)

    def lpop(self, key, pack=False):
        if pack:
            ret = self.redis.lpop(key)
            if ret is None:
                return ret
            return umsgpack.unpackb(ret)
        return self._check_data(self.redis.lpop(key))

    def expire(self, key, time):
        self.redis.expire(key, time)

    def process_delete_key(self, key):
        # key 不存在则不处理
        if self.exists(key) == 0:
            return
        # 先修改key名称
        tar_key = f'{key}_del'
        self.redis.rename(key, tar_key)
        self.expire(tar_key, 1800)

    def rpop(self, key, pack=False):
        if pack:
            ret = self.redis.rpop(key)
            if ret is None:
                return ret
            return umsgpack.unpackb(ret)
        return self._check_data(self.redis.rpop(key))

    def push(self, key, data, pack=False, high_priority=False):
        """
        根据优先级决定是左边插入还是右边插入
        :param key:
        :param data:
        :param pack:
        :param high_priority:
        :return:
        """
        if pack:
            data = umsgpack.packb(data)
        elif isinstance(data, (dict, list)):
            data = json.dumps(data, ensure_ascii=False)
        if high_priority:
            self.redis.lpush(key, data)
        else:
            self.redis.rpush(key, data)

    def rpush(self, key, data, pack=False):
        if pack:
            data = umsgpack.packb(data)
        elif isinstance(data, (dict, list)):
            data = json.dumps(data, ensure_ascii=False)
        self.redis.rpush(key, data)

    def batch_rpush(self, key, data, pack=False):
        if pack:
            data = [umsgpack.packb(x) for x in data]
        else:
            data = [json.dumps(x, ensure_ascii=False)
                    if isinstance(x, dict) else x for x in data]
        self.redis.rpush(key, *data)

    def lpush(self, key, data, pack=False):
        if pack:
            data = umsgpack.packb(data)
        elif isinstance(data, (dict, list)):
            data = json.dumps(data, ensure_ascii=False)
        self.redis.lpush(key, data)

    def sadd(self, key, data):
        if isinstance(data, dict):
            data = json.dumps(data, ensure_ascii=False)
        return self.redis.sadd(key, data)

    def spop(self, key):
        return self._check_data(self.redis.spop(key))

    def srem(self, key, value):
        return self.redis.srem(key, value)

    def srandmember(self, key):
        return self._check_data(self.redis.srandmember(key))

    def scard(self, key):
        return self.redis.scard(key)

    def sismember(self, key, data):
        return self.redis.sismember(key, data)

    def clear(self, key):
        self.redis.delete(key)

    def ping(self):
        return self.redis.ping()

    def exists(self, key):
        return self.redis.exists(key)

    def scan_key(self, pattern, count=10):
        return [key for key in self.redis.scan_iter(pattern, count=count)]
