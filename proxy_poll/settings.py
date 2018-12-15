######################分数设置，以及redis设置##################
MAX_SCORE = 100
MIN_SORCE = 0
INITIAL_SORCE = 10
REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
REDIS_PASSWORD = None
REDIS_KEY = "proxies"

######################请求设置#################################
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"
DAILI66_COOKIE = "yd_cookie=70e5c339-7e77-4681687dcc5a696de1663dcb5f30079cee96; Hm_lvt_1761fabf3c988e7f04bec51acd4073f4=1544782139; _ydclearance=942e78d6d6cef8b80e6832cc-6d50-4b12-8a05-4a7787c05e29-1544847645; Hm_lpvt_1761fabf3c988e7f04bec51acd4073f4=1544840454"

# 最大的代理数
POOL_UPPER_THRESHOLD = 1000

# 测试ip的相关配置
VALID_STATUS_CODES = [200]
TEST_URL = "http://www.baidu.com"
BATCH_TEST_SIZE = 100
