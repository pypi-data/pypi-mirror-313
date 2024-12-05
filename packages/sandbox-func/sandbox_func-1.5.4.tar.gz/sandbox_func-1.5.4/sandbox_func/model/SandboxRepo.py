from sandbox_func.common.lang.dictclass import DictClass
from sandbox_func.model.SandboxApp import SandboxApp


class SandboxRepo(DictClass):
    path: str  # 代码路径
    apps: list[SandboxApp]
