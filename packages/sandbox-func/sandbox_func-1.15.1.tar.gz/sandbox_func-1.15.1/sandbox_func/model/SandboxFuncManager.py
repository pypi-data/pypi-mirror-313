import logging

from sandbox_func.common.lang.moduleutil import ModuleUtil
from sandbox_func.model.SandboxFunc import SandboxFunc


logger = logging.getLogger(__name__)


class SandboxFuncManager:
    func_mapping = {}  # type: {str: SandboxFunc}

    @classmethod
    def get_func(cls, class_file: str, method_name: str) -> SandboxFunc:
        entry = f"{class_file}.{method_name}"
        if entry not in cls.func_mapping:
            func = SandboxFunc(id=entry, class_file=class_file, method_name=method_name)
            func.run = ModuleUtil.get_func(entry)
            cls.func_mapping[entry] = func
        return cls.func_mapping[entry]

    @classmethod
    def clear(cls):
        cls.func_mapping.clear()
