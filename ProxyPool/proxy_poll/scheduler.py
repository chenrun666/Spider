import time

from multiprocessing import Process
from ProxyPool.proxy_poll.api import app
from ProxyPool.proxy_poll.getter import Getter
from ProxyPool.proxy_poll.tester import Tester
from ProxyPool.proxy_poll.settings import *


class Scheduler():
    def schedule_tester(self, cycle=TESTER_CYCLE):
        tester = Tester()
        while True:
            print("测试器开始")
            tester.run()
            time.sleep(cycle)

    def schedule_getter(self, cycle=GETTER_CYCLE):
        getter = Getter()
        while True:
            print("开始抓取代理")
            getter.run()
            time.sleep(cycle)

    def schedule_api(self):
        app.run(API_HOST, API_PORT)

    def run(self):
        print("代理池开始运行")

        if TESTER_ENABLED:
            tester_process = Process(target=self.schedule_tester)
            tester_process.start()

        if GETTER_ENABLED:
            getter_process = Process(target=self.schedule_getter)
            getter_process.start()

        if API_ENABLED:
            api_process = Process(target=self.schedule_api)
            api_process.start()


if __name__ == '__main__':
    scheduler = Scheduler()
    scheduler.run()
