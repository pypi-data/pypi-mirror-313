from typing import Union, Optional

from pydantic import BaseModel


class BaseRequest(BaseModel):
    appCode: str  # app 名称
    tableCode: str  # 表名


class GetOptions(BaseModel):
    select: str = ""
    idToName: bool = False
    fetchSubTable: bool = False
    fetchTotal: bool = True


class GetMetaOptions(GetOptions):
    fetchRelatedApp: bool = False


class GetRequest(BaseRequest):
    id: str  # 主键值
    parameters: dict = {}
    options: GetOptions = GetOptions()  # 查询配置


class GetMetaRequest(GetRequest):
    metadataAppId: str = ""  # 应用id
    options: GetMetaOptions = GetMetaOptions()  # 查询配置


class GetListRequest(BaseRequest):
    query: str = None  # 查询条件
    filter: Union[dict, None] = {}
    sort: str = None
    select: Union[str, None] = []
    pageSize: int = 10
    pageNum: int = 1
    options: GetOptions = GetOptions()  # 查询配置


class GetMetaListRequest(GetListRequest):
    metadataAppId: str = ""  # 应用id
    options: GetMetaOptions = GetMetaOptions()  # 查询配置


class CreateOptions(BaseModel):
    conflictToUpdate: bool = False


class CreateRequest(BaseRequest):
    values: dict = {}  # 主键值
    options: CreateOptions = CreateOptions()  # 查询配置


class ExportAppRequest(BaseModel):
    appId: str
    appVersionId: str


class BulkCreateOptions(BaseModel):
    conflictToUpdate: bool = False


class BulkCreateRequest(BaseRequest):
    values: Optional[list[dict]] = None  # 主键值
    options: BulkCreateOptions = BulkCreateOptions()  # 查询配置


class UpdateRequest(BaseRequest):
    id: str  # 主键值
    values: dict = {}
    metadataVersionId: Optional[str] = None


class BulkUpdateRequest(BaseRequest):
    ids: list  # 主键值
    values: dict = {}


class DeleteOptions(BaseModel):
    cascaded: bool = True


class DeleteRequest(BaseRequest):
    id: str  # 主键值
    options: DeleteOptions = DeleteOptions()


class BulkDeleteRequest(BaseRequest):
    ids: list  # 主键值


class GeneralResponse(BaseModel):
    code: str = None
    message: str = None
    args: Optional[list[dict]] = None
    success: bool or None


class GetResponse(BaseModel):
    data: dict


class GetListResponse(BaseModel):
    data: Optional[list[dict]]
    total: int


class CreateResponse(BaseModel):
    lastId: str


class UpdateResponse(BaseModel):
    count: int
    lastId: Optional[str]


class DeleteResponse(BaseModel):
    count: int


class BulkCreateResponse(BaseModel):
    count: int


class BulkUpdateResponse(BaseModel):
    count: int


class BulkDeleteResponse(BaseModel):
    count: int
