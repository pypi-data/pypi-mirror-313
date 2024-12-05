from typing import Union, Optional

from pydantic import BaseModel


class LivelyDataBaseRequest(BaseModel):
    appCode: str  # app 名称
    tableId: str  # 表名


class LivelyDataGetOptions(BaseModel):
    select: str = ""
    idToName: bool = False
    fetchSubTable: bool = False
    fetchTotal: bool = True


class LivelyDataGetRequest(LivelyDataBaseRequest):
    id: str  # 主键值
    parameters: dict = {}
    options: LivelyDataGetOptions = LivelyDataGetOptions()  # 查询配置


class LivelyDataGetListRequest(LivelyDataBaseRequest):
    query: str = None  # 查询条件
    filter: Union[dict, None] = {}
    sort: str = None
    select: Union[str, None] = []
    pageSize: int = 10
    pageNum: int = 1
    options: LivelyDataGetOptions = LivelyDataGetOptions()  # 查询配置

class LivelyDataCreateRequest(LivelyDataBaseRequest):
    values: dict = {}  # 主键值


class BulkCreateOptions(BaseModel):
    conflictToUpdate: bool = False


class LivelyDataBulkCreateRequest(LivelyDataBaseRequest):
    values: Optional[list[dict]] = None  # 主键值
    options: BulkCreateOptions = BulkCreateOptions()  # 查询配置


class LivelyDataUpdateRequest(LivelyDataBaseRequest):
    id: str  # 主键值
    values: dict = {}


class LivelyDataBulkUpdateRequest(LivelyDataBaseRequest):
    ids: list  # 主键值
    values: dict = {}


class LivelyDataDeleteOptions(BaseModel):
    cascaded: bool = True


class LivelyDataDeleteRequest(LivelyDataBaseRequest):
    id: str  # 主键值
    options: LivelyDataDeleteOptions = LivelyDataDeleteOptions()


class LivelyDataBulkDeleteRequest(LivelyDataBaseRequest):
    ids: list  # 主键值


class LivelyDataGeneralResponse(BaseModel):
    code: str = None
    message: str = None
    args: Optional[list[dict]] = None
    success: bool or None


class LivelyDataGetResponse(BaseModel):
    data: dict


class LivelyDataGetListResponse(BaseModel):
    data: Optional[list[dict]]
    total: int


class LivelyDataCreateResponse(BaseModel):
    lastId: str


class LivelyDataUpdateResponse(BaseModel):
    count: int


class LivelyDataDeleteResponse(BaseModel):
    count: int


class LivelyDataBulkCreateResponse(BaseModel):
    count: int


class LivelyDataBulkUpdateResponse(BaseModel):
    count: int


class LivelyDataBulkDeleteResponse(BaseModel):
    count: int
