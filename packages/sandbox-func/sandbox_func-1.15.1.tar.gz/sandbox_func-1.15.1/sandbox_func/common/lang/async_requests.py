import logging
import typing

import httpx
from httpx import Response, Request
from httpx._client import UseClientDefault, USE_CLIENT_DEFAULT
from httpx._types import URLTypes, RequestContent, RequestData, RequestFiles, QueryParamTypes, HeaderTypes, CookieTypes, \
    TimeoutTypes, RequestExtensions, ProxiesTypes, VerifyTypes

logger = logging.getLogger(__name__)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)


class AsyncRequests:
    def __init__(self, base_url=None, proxies: typing.Optional[ProxiesTypes] = None, verify: VerifyTypes = False):
        self.base_url = base_url
        self.proxies = proxies
        self.verify = verify

    async def send(self, request: Request, retry=1) -> Response:
        for retry_count in range(retry):
            try:
                async with httpx.AsyncClient(base_url=self.base_url, proxies=self.proxies,
                                             verify=self.verify) as client:
                    return await client.send(request)
            except Exception as e:
                logger.error(f'{str(request.url)}请求接口失败，尝试第{retry_count + 1}次')
                # logger.error(f"请求参数：{str(request.json)}")
                if retry_count == retry - 1:
                    raise e
                else:
                    logger.error(e)

    async def request(self, url, data, retry=1) -> Response:
        for retry_count in range(retry):
            try:
                async with httpx.AsyncClient(base_url=self.base_url, proxies=self.proxies,
                                             verify=self.verify, timeout=None) as client:
                    return await client.request('POST', url, data=data)
            except Exception as e:
                logger.error(e)
                logger.error(f'{url}请求接口失败，尝试第{retry_count + 1}次')
                logger.error(f"请求参数：{str(data)}")
                if retry_count == retry - 1:
                    raise e
                else:
                    logger.error(e)

    def build_request(self,
                      method: str,
                      url: URLTypes,
                      *,
                      content: typing.Optional[RequestContent] = None,
                      data: typing.Optional[RequestData] = None,
                      files: typing.Optional[RequestFiles] = None,
                      json: typing.Optional[typing.Any] = None,
                      params: typing.Optional[QueryParamTypes] = None,
                      headers: typing.Optional[HeaderTypes] = None,
                      cookies: typing.Optional[CookieTypes] = None,
                      timeout: typing.Union[TimeoutTypes, UseClientDefault] = USE_CLIENT_DEFAULT,
                      extensions: typing.Optional[RequestExtensions] = None):
        timeout = float(timeout) if isinstance(timeout, int) else timeout
        return httpx.AsyncClient(base_url=self.base_url, proxies=self.proxies, verify=self.verify).build_request(
            method, url, content=content, data=data, files=files, json=json, params=params, headers=headers,
            cookies=cookies,
            timeout=timeout, extensions=extensions)
