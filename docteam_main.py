import time
import unittest
from BeautifulReport import BeautifulReport
import os
from stub_framework.stubServer import server_run
import threading
from stub_framework.stubOperation import StubOperate
from werkzeug.serving import make_server

ENVIRON = "Online"  # 线上 Online 测试环境 Offline
Dir = os.path.dirname(os.path.abspath(__file__))


def run(test_suite):
    # 定义输出的文件位置和名字
    filename = "report.html"
    result = BeautifulReport(test_suite)
    result.report(filename=filename, description='测试报告', report_dir='./')


def docteamApp_run():
    os.chdir(Dir + '/app')
    os.system('python docteamApp.py')


if __name__ == '__main__':
    # 启动桩
    print('@@')
    t = threading.Thread(target=server_run)
    t.start()
    # 启动被测服务
    t2 = threading.Thread(target=docteamApp_run)
    t2.start()
    time.sleep(5)

    pattern = 'stub'  # all: run all case,  smoking: run smoking case.
    if pattern == 'all':
        suite = unittest.TestLoader().discover(Dir + '/testCase', 'test_*')
    elif pattern == 'smoking':
        suite = unittest.TestLoader().discover(Dir + '/testCase', 'test_major*')
    elif pattern == 'stub':
        suite = unittest.TestLoader().discover(Dir + '/testCase', 'test_edit*')
    else:
        raise "pattern error"
    run(suite)

    StubOperate().shutdown_stub()
    # server stop
    os.chdir(Dir + '/app')
    os.system('python appStop.py')