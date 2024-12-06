import logging

from sandbox_func.common.config.BusinessURLConfig import BusinessURLConfig
from sandbox_func.common.request.CybotronSyncClient import CybotronClient
from sandbox_func.common.util.data_transfer_util import json2obj, dict2obj
from sandbox_func.repository.cybotron.model.flowobj import FlowWebRequest

logger = logging.getLogger(__file__)


class ServiceFlow:

    @classmethod
    async def _run(cls, url, data=None):
        client = CybotronClient()
        if data is None:
            data = FlowWebRequest()
        elif isinstance(data, dict):
            data = dict2obj(data, FlowWebRequest)
        elif isinstance(data, str):
            data = json2obj(data, FlowWebRequest)
        else:
            raise Exception(f"输入数据类型异常：{type(data)}")

        res = await client.post(url, json=data.model_dump())
        logger.info(f"返回结果：{res}")
        return res

    @classmethod
    async def service(cls, app_code, flow_code, data=None):
        url = f"{BusinessURLConfig.get_flow_url()}/{app_code}/{flow_code}"
        return await cls._run(url, data)

    @classmethod
    async def service_call(cls, app_id, flow_id, data=None):
        url = f"{BusinessURLConfig.get_flow_url()}/{app_id}/{flow_id}/call"
        return await cls._run(url, data)
