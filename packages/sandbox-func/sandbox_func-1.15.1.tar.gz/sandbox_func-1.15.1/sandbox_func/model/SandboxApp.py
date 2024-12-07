from sandbox_func.common.lang.dictclass import DictClass
from sandbox_func.model.SandboxFunc import SandboxFunc


class SandboxApp(DictClass):
    id: str
    name: str
    code: str
    path: str  # 代码路径
    type: str
    region: str
    apigw_url: str
    funcs: list[SandboxFunc]
