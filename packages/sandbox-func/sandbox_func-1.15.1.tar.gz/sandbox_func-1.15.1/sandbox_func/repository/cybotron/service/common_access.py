# -*- coding: utf-8 -*-
import logging
from typing import Dict

from sandbox_func.common.request.CybotronSyncClient import CybotronClient
from sandbox_func.repository.cybotron.model.metadataobj import *

logger = logging.getLogger(__name__)


class CommonAccess:

    def __init__(self):
        self.URL = None
        self.client = CybotronClient()

    async def create(self, req: CreateRequest) -> CreateResponse:
        """
        单条创建接口
        """
        result = await self.get_response(req, "create")
        return CreateResponse(lastId=result["lastId"])

    async def update(self, req: UpdateRequest) -> UpdateResponse:
        """
        单条修改接口
        """
        result = await self.get_response(req, "update")
        return UpdateResponse(count=result["count"], lastId=result.get("lastId"))

    async def delete(self, req: DeleteRequest) -> DeleteResponse:
        """
        单条删除接口
        """
        result = await self.get_response(req, "delete")
        return DeleteResponse(count=result["count"])

    async def bulk_create(self, req: BulkCreateRequest) -> BulkCreateResponse:
        """
        批量创建接口
        """
        result = await self.get_response(req, "bulkCreate")
        return BulkCreateResponse(count=result["count"])

    async def bulk_update(self, req: BulkUpdateRequest) -> BulkUpdateResponse:
        """
        批量修改接口
        """
        result = await self.get_response(req, "bulkUpdate")
        return BulkUpdateResponse(count=result["count"])

    async def bulk_delete(self, req: BulkDeleteRequest) -> BulkDeleteResponse:
        """
        批量删除接口
        """
        result = await self.get_response(req=req, method="bulkDelete")
        return BulkDeleteResponse(count=result["count"])

    async def get_response(self, req, method: str = "", re_method: str = "post") -> Dict:
        """
        请求数据
        """
        app_code = req.appCode
        table_code = req.tableCode
        url = f"{self.URL}/{app_code}/{table_code}/{method}"
        logger.info(f"url:{url}, json:{req.dict()}")
        response = await self.client.send(url, re_method, json=req.dict())
        if not response.get("success"):
            raise Exception(response.get("message"))
        return response["result"]

    async def get_response_json(self, url: str = "", json: str = "", method: str = "", headers: Dict = None) -> str:
        """
        请求数据, 抽取公共使用
        """
        response = await self.client.send(url, method, json=json)
        return response
