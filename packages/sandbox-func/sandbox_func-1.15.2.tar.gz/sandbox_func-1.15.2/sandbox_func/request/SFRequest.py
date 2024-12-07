from typing import Optional
from sandbox_func.common.lang.dictclass import DictClass


class SFRequest(DictClass):
    class_file: str
    method_name: str
    request_id: str
    job_id: Optional[str]
    hook: dict
    input: DictClass
