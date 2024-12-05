import logging
import contextvars

from sandbox_func.common.lang.async_requests import AsyncRequests
from sandbox_func.common.config.LoginConfig import DefaultLoginConfig
from sandbox_func.common.config.BaseURLConfig import DefaultURLConfig

logger = logging.getLogger(__name__)
ENV = DefaultLoginConfig.get_env()
TENANT_ID = contextvars.ContextVar('Id of tenant')
TRACE_ID = contextvars.ContextVar('Trace id')


class CybotronClient:

    def __init__(self, throw_exception: bool = True):
        self.throw_exception = throw_exception
        self.client = AsyncRequests(base_url=self.get_base_url())

    @staticmethod
    def get_base_url() -> str:
        if DefaultLoginConfig.unit_test:
            return DefaultURLConfig.get_api_base_url(ENV)
        else:
            return 'http://localhost:{}'.format(9000 if DefaultLoginConfig.is_online else 8081)  # 区分沙盒边车和CLI边车端口

    @staticmethod
    def __get_headers(method, url) -> dict:
        # 单元测试时从配置文件中获取
        if DefaultLoginConfig.unit_test:
            headers = {
                'X-API-KEY': DefaultLoginConfig.get_api_key(),
                'X-TENANT-ID': DefaultLoginConfig.get_tenant_id()
            }
        else:
            headers = {
                'X-TENANT-ID': TENANT_ID.get(),
                'Original-Request': '{}__{}'.format(method, url),
                'traceId': TRACE_ID.get()
            }
        return headers

    async def get(self, url, params=None):
        return await self.send(url, method="get", params=params)

    async def send(self, url, method, data=None, files=None, json=None, params=None):
        headers = CybotronClient.__get_headers(method, url)
        # 除单元测试外，全部进行转发
        if not DefaultLoginConfig.unit_test:
            method, url = 'post', '/forward-request'
        logging.info('发送业务请求: method({}), url({})'.format(method, self.client.base_url + url))
        request = self.client.build_request(method=method, url=url, data=data, json=json, files=files,
                                            params=params, headers=headers)
        response = await self.client.send(request)
        response_json = response.json()

        if self.throw_exception and response_json.get("errorMessage"):
            raise Exception(response_json.get("errorMessage"))

        return response_json

    async def post(self, url, data=None, files=None, json=None):
        return await self.send(url, method="post", data=data, files=files, json=json)
