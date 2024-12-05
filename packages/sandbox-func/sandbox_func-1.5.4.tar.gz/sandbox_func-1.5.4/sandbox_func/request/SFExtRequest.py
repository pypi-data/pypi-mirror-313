from sandbox_func.common.lang.dictclass import DictClass


class SFExtRequest(DictClass):
    app_id: str
    func_id: str
    func_type: str
    func_region: str
    request_id: str
    input: DictClass
