import redis

from random import choice

from ProxyPool.proxy_poll.settings import *
from ProxyPool.proxy_poll.error import PoolEmptyError


class RedisClient(object):
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT):
        self.db = redis.Redis(host=host, port=port, decode_responses=True)

    def add(self, proxy, score=INITIAL_SORCE):
        """
        添加代理，设置分数为最高
        :param proxy: 代理
        :param score: 分数
        :return:
        """
        # 有序集合
        if not self.db.zscore(REDIS_KEY, proxy):
            return self.db.zadd(REDIS_KEY, {proxy: score})

    def random(self):
        """
        随机获取有效代理，首先尝试获取最高分数代理，如果最高分数不存在， 则按照排名获取，否则异常
        :return: 随机代理
        """
        result = self.db.zrevrange(REDIS_KEY, 0, 100)
        if len(result):
            return choice(result)

        else:
            raise PoolEmptyError

    def decrease(self, proxy):
        """
        代理值减1分，分校小于最小值，则从数据库中删除
        :param proxy: 代理
        :return: 修改后的代理分数
        """
        score = self.db.zscore(REDIS_KEY, proxy)
        if score and score > MIN_SORCE:
            print("代理", proxy, "当前分数", score, "减1")
            return self.db.zincrby(REDIS_KEY, -1, proxy)
        else:
            print("代理", proxy, "当前分数", score, "移除")
            return self.db.zrem(REDIS_KEY, proxy)

    def exists(self, proxy):
        """
        判断是否存在
        :param proxy: 代理
        :return: 是否存在
        """
        return not self.db.zscore(REDIS_KEY, proxy) == None

    def max(self, proxy):
        """
        将代理设置为MAX_SCORE
        :param proxy: 代理
        :return: 设置结束
        """
        print("代理", proxy, "可用, 设置为", MAX_SCORE)
        return self.db.zadd(REDIS_KEY, {proxy: MAX_SCORE})

    def count(self):
        """
        :return: 数量
        获取数量
        """
        return self.db.zcard(REDIS_KEY)

    def all(self):
        """
        获取全部代理
        :return: 全部代理列表
        """
        return self.db.zrangebyscore(REDIS_KEY, MIN_SORCE, MAX_SCORE)

    def batch(self, start, stop):
        """
        批量获取
        :param start: 开始索引
        :param stop: 结束索引
        :return: 代理列表
        """
        return self.db.zrevrange(REDIS_KEY, start, stop - 1)


if __name__ == '__main__':
    conn = RedisClient()
    result = conn.batch(0, 2)
    print(result)
