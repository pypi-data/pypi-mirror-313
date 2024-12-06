import time
import json
import logging
from sandbox_func.common.config.BusinessURLConfig import BusinessURLConfig, DataTypeEnum
from sandbox_func.common.request.CybotronSyncClient import CybotronClient
from sandbox_func.repository.cybotron.model.metadataobj import GetRequest, CreateRequest, GetListRequest
from sandbox_func.repository.cybotron.service.data_accessor import DataAccessor
from sandbox_func.request.SFResponse import SFResponse
from sandbox_func.request.SFRequest import SFRequest

logger = logging.getLogger(__name__)


class SandboxAccessor:
    URL = BusinessURLConfig.get_url(DataTypeEnum.SANDBOX)

    @classmethod
    async def dispatch_sandbox(cls, request: SFRequest) -> SFResponse:
        """
        调用沙盒函数
        """
        client = CybotronClient()
        url = f"{cls.URL}/{request.app_id}/{request.func_id}"
        response = SFResponse()
        try:
            res = await client.send(url, 'POST', json=request.input)
            response.result = res['result']
            result_json = json.loads(res['result'])
            response.request_id = result_json["requestId"]
            return response
        except Exception as e:
            response.error = e
            return response

    @classmethod
    async def update_async_job(cls, job_id, status, progress, loading_message=None, success_message=None,
                               error_code=None, error_message=None):
        """更新异步任务"""
        data = {"jobId": job_id, "success": status, "progress": progress}
        if progress == 100 and not loading_message:
            data["loadingMessage"] = "执行结束"
        if success_message:
            data["successMessage"] = success_message
        elif error_message:
            data["errorMessage"], data["error_code"] = error_message, error_code
        elif loading_message:
            data["loadingMessage"] = loading_message
        try:
            logger.info(f"更新异步任务，请求参数：data:{data}")
            client = CybotronClient()
            result = await client.post("/cbn/api/v1/asyncJob/update", json=data)
            if result.get("success") is not True:
                logger.error(f"更新异步任务失败！{result}")
            logger.info(f"更新异步任务返回结果：{result}")
            return result
        except Exception as e:
            logger.error(f"发送更新异步任务请求失败！{str(e)}")

    @classmethod
    async def create_async_job(cls, app_id, job_id, status, progress):
        """
        创建异步任务
        """
        try:
            get_res = await cls.get_async_job(job_id)
            if get_res:  # 已存在，更新进度及状态
                update_res = await cls.update_async_job(job_id, status, progress)
                logger.info(f"更新异步任务进度及状态：{update_res}")
                return job_id
            else:
                data_accessor = DataAccessor()
                get_tenant_req = GetListRequest(
                    **{'filter': {'app_id': app_id}, "appCode": "metabase", "tableCode": "mb_tenant_app"})
                get_tenant_res = await data_accessor.get_list(get_tenant_req)
                app_version_code = get_tenant_res.data[0].get("tenant_id", "master")
                req = CreateRequest(
                    appCode="metabase",
                    tableCode="mb_async_job",
                    values={"progress": progress, "success": status, "id": job_id,
                            "create_time": round(time.time() * 1000),
                            "app_code": app_id, "app_version_code": app_version_code, "job_type": "AsyncCallSandbox"}
                )
                create_res = await data_accessor.create(req)
                logger.info(f"创建异步任务返回结果：{create_res}，请求参数：req:{req}")
                return create_res.lastId
        except Exception as e:
            logger.error(f"创建异步任务失败！{str(e)}")

    @classmethod
    async def get_async_job(cls, job_id):
        """
        确认异步任务执行进度
        """
        data_accessor = DataAccessor()
        get_req = GetRequest(
            appCode="metabase",
            tableCode="mb_async_job",
            id=job_id
        )
        try:
            get_res = await data_accessor.get(get_req)
            return get_res.data
        except Exception as e:
            logger.error(f"获取异步任务失败！{str(e)}")
