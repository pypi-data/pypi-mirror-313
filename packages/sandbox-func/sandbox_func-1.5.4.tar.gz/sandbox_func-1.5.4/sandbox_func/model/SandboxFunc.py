from sandbox_func.common.lang.dictclass import DictClass


class SandboxFunc(DictClass):
    id: str
    class_file: str
    method_name: str
    run: callable       # 执行方法
