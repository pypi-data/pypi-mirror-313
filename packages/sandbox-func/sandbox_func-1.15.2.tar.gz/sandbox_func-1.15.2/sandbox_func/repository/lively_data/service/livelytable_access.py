# -*- coding: utf-8 -*-
import logging
from typing import Dict
from sandbox_func.common.config.BusinessURLConfig import DataTypeEnum, BusinessURLConfig
from sandbox_func.common.request.CybotronClient import CybotronClient
from sandbox_func.repository.lively_data.model.metadataobj import *

logger = logging.getLogger(__name__)


class LivelyDataAccessor:

    def __init__(self):
        self.client = CybotronClient()

    async def get(self, req: LivelyDataGetRequest) -> LivelyDataGetResponse:
        """
        单条创建接口
        """
        result = await self.get_response(req, "get")
        data = {} if not result.get('data', "") else result['data']  # 查询结果为空, 返回空字典
        return LivelyDataGetResponse(data=data)

    async def get_list(self, req: LivelyDataGetListRequest) -> LivelyDataGetListResponse:
        """
        分页查询接口
        """
        result = await self.get_response(req, "getList")
        return LivelyDataGetListResponse(data=result["data"], total=result["total"])

    async def create(self, req: LivelyDataCreateRequest) -> LivelyDataCreateResponse:
        """
        单条创建接口
        """
        result = await self.get_response(req, "create")
        return LivelyDataCreateResponse(lastId=result["lastId"])

    async def update(self, req: LivelyDataUpdateRequest) -> LivelyDataUpdateResponse:
        """
        单条修改接口
        """
        result = await self.get_response(req, "update")
        return LivelyDataUpdateResponse(count=result["count"])

    async def delete(self, req: LivelyDataDeleteRequest) -> LivelyDataDeleteResponse:
        """
        单条删除接口
        """
        result = await self.get_response(req, "delete")
        return LivelyDataDeleteResponse(count=result["count"])

    async def bulk_create(self, req: LivelyDataBulkCreateRequest) -> LivelyDataBulkCreateResponse:
        """
        批量创建接口
        """
        result = await self.get_response(req, "bulkCreate")
        return LivelyDataBulkCreateResponse(count=result["count"])

    async def bulk_update(self, req: LivelyDataBulkUpdateRequest) -> LivelyDataBulkUpdateResponse:
        """
        批量修改接口
        """
        result = await self.get_response(req, "bulkUpdate")
        return LivelyDataBulkUpdateResponse(count=result["count"])

    async def bulk_delete(self, req: LivelyDataBulkDeleteRequest) -> LivelyDataBulkDeleteResponse:
        """
        批量删除接口
        """
        result = await self.get_response(req=req, method="bulkDelete")
        return LivelyDataBulkDeleteResponse(count=result["count"])

    async def get_response(self, req, method: str = "", re_method: str = "post") -> Dict:
        """
        请求数据
        """
        app_code = req.appCode
        table_id = req.tableId
        url = f"{BusinessURLConfig.get_url(DataTypeEnum.LIVELYDATA)}/{app_code}/{table_id}/{method}"
        logger.info(f"json:{req.model_dump()}")
        response = await self.client.post(url, json=req.model_dump())
        if not response.get("success"):
            raise Exception(response.get("message"))
        return response["result"]
