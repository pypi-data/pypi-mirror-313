from typing import TYPE_CHECKING
from sandbox_func.common.lang.dictclass import DictClass

if TYPE_CHECKING:
    from sandbox_func.request.SFResponseJob import SFResponseJob


class SFResponse(DictClass):
    result: any
    request_id: str
    error: any
    success: bool
    job: "SFResponseJob"
