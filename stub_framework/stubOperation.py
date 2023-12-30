import requests


class StubOperate:
    def __init__(self):
        self.port = 899

    def shutdown_stub(self):
        """http桩下线"""
        requests.post(url=f"http://127.0.0.1:{self.port}/shutdown", timeout=3)
