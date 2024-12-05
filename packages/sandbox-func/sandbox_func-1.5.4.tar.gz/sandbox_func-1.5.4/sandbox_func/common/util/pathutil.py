import os
import sys
import re
from sandbox_func.common.config.LogConfig import DEFAULT_LOG_FILE

DEFAULT_PROJ_ROOT_DIR = '/mnt/scf'


def get_project_path() -> str:
    common_path = os.path.dirname(os.path.dirname(__file__))
    sandbox_func_path = os.path.dirname(common_path)  # noqa
    return os.path.dirname(sandbox_func_path)


def get_test_path():
    project_path = get_project_path()
    test_path = os.path.join(project_path, "tests")
    return test_path


def get_log_file_path():
    project_path = get_project_path()
    log_file_path = os.path.join(project_path, DEFAULT_LOG_FILE)
    return log_file_path


def get_tmp_path():
    if os.getenv("env") in ["dev", "test", "prod"]:
        return "/tmp"  # 云函数环境
    return os.path.join(get_project_path(), "tmp")


def get_lib_package_path():
    result_dict, lib_pkg_path = {}, None
    toml_path = os.path.join(sys.path[0], "pyproject.toml")
    pattern = r'({})\s*=\s*"([^"]+)"'.format('|'.join(['pylib', 'pylib_version']))

    with open(toml_path, 'r') as file:
        file_content = file.read()

    # 使用正则表达式查找所有匹配的键值对
    matches = re.findall(pattern, file_content)
    if matches:
        # 遍历匹配结果，填充字典
        for key, value in matches:
            result_dict[key] = value
        # 打印结果字典
        lib_pkg_path = os.path.join(DEFAULT_PROJ_ROOT_DIR, 'pylib',
                                    result_dict['pylib'], result_dict['pylib_version'], 'site-packages')
    return lib_pkg_path
