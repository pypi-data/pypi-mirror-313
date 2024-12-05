import logging

from sandbox_func.common.lang.singleton import SingletonMeta
from sandbox_func.model.SandboxFuncManager import SandboxFuncManager

from sandbox_func.repository.cybotron.service.sandbox_accessor import SandboxAccessor
from sandbox_func.request.SFRequest import SFRequest
from sandbox_func.request.SFResponse import SFResponse
from sandbox_func.request.SFResponseJob import SFResponseJob

logger = logging.getLogger(__name__)


class SandboxFuncService(metaclass=SingletonMeta):
    def __init__(self):
        pass

    @staticmethod
    async def create_async_job(app_id, request_id, status, progress) -> str:
        return await SandboxAccessor.create_async_job(app_id, request_id, status, progress)

    @staticmethod
    async def update_async_job(request_id, status, progress, loading_message=None, success_message=None,
                               error_code=None, error_message=None):
        return await SandboxAccessor.update_async_job(request_id, status, progress, loading_message,
                                                      success_message, error_code, error_message)

    @staticmethod
    async def call(request: SFRequest) -> SFResponse:
        response = SFResponse()
        job = SFResponseJob()
        job.set_request_id(request.request_id)
        job.set_job_id(request.job_id)
        response.request_id = request.request_id
        response.job = job
        try:
            func = SandboxFuncManager.get_func(request.class_file, request.method_name)
            if not func or not func.run:
                logger.error(f'沙盒函数缓存里找不到class_file={request.class_file}, method_name={request.method_name}')
                raise Exception(f"class_file={request.class_file}, method_name={request.method_name} not found")
            result = await func.run(request, response)
            if result:
                response.result = result
            return response
        except Exception as e:
            logger.exception(e)
            response.error = str(e)
            return response
