import unittest
import requests
from stub_framework.httpCommon import HttpCommon
import json
import time


class TestPro(unittest.TestCase):

    def testCase01(self):
        url = 'http://127.0.0.1:8530/edit'
        headers = {
            'Content-Type': 'application/json',
            'Cookie': 'user_id=2'
        }
        body = {
            'file_id': '125',
            'status': 'edit'
        }

        hc = HttpCommon()
        hc.thread_run_requests(method='POST', url=url, headers=headers, json=body)

        time.sleep(2)
        print(hc.status_code)
        print(hc.res_text)
