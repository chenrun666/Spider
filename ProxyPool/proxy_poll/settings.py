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
# DAILI66_COOKIE = "yd_cookie=70e5c339-7e77-4681687dcc5a696de1663dcb5f30079cee96; Hm_lvt_1761fabf3c988e7f04bec51acd4073f4=1544782139; _ydclearance=cc6ce2fcee7f697cfa15a34b-e777-44ad-b684-cdc2ac19008d-1544972611; Hm_lpvt_1761fabf3c988e7f04bec51acd4073f4=1544965415"
# 最大的代理数
POOL_UPPER_THRESHOLD = 50000

# 测试ip的相关配置
VALID_STATUS_CODES = [200]
TEST_URL = "http://www.baidu.com"
BATCH_TEST_SIZE = 10

# 检测周期
TESTER_CYCLE = 60

# 获取周期
GETTER_CYCLE = 300

API_HOST = "0.0.0.0"
API_PORT = 5555


# 开关
TESTER_ENABLED = True
GETTER_ENABLED = True
API_ENABLED = True