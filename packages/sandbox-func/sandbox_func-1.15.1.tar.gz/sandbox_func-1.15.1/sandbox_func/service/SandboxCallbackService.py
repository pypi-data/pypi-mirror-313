import logging

from sandbox_func.request import SFResponse, SFRequest
from sandbox_func.common.lang.async_requests import AsyncRequests

# logger = AwLogger.getLogger(__name__)
logger = logging.getLogger(__name__)


class SandboxCallbackService:
    """异步任务回调处理，如果request里包含hook信息，则进行回调"""

    def __init__(self, request: SFRequest, response: SFResponse):
        self.req = request
        self.res = response

    @staticmethod
    async def callback(req: SFRequest, res: SFResponse):
        logger.info(f"req:{req}")
        hook = req.get('hook')
        if hook:
            client = AsyncRequests()
            callback_url = hook.get('url')  # type:str
            params = hook['params'].dict() if hook.get('params') else hook.get('params')  # 透传参数
            req_input = req['input'].dict() if req.get('input') else req.get('input')
            data = {"result": res.result, "input": req_input, "params": params,
                    "progress": res.job.job_progress, "success": res.job.job_success, "error": res.job.job_error}
            logger.info(f'异步请求回调， 回调地址：{callback_url}， 回调js参数：{data}')
            try:
                req = client.build_request('post', url=callback_url, json=data)
                res = await client.send(req)
                logger.info(f"回调成功，返回值:{res}")
            except Exception as e:
                logger.error(f"回调处理报错，回调地址：{callback_url}, 回调参数：{data}, 报错信息：{e}")
