from sandbox_func.common.request.CybotronClient import CybotronClient
from sandbox_func.common.lang.sync import execute_async


class CybotronSyncClient:
    """
    赛博坦同步接口，方便命令行工具等没有异步条件的代码中使用
    """

    def __init__(self, throw_exception=True):
        self.throw_exception = throw_exception
        self.client = CybotronClient(throw_exception)

    def get(self, url, params=None):
        return self.send(url, method="get", params=params)

    def send(self, url, method, data=None, files=None, json=None, params=None):
        return execute_async(self.client.send, url, method, data=data, files=files, json=json, params=params)

    def post(self, url, data=None, files=None, json=None):
        return self.send(url, method="post", data=data, files=files, json=json)
