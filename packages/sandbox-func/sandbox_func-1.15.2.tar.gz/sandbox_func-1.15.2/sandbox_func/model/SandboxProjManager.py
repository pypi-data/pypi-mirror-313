import logging
import os.path

from sandbox_func.model.SandboxFuncManager import SandboxFuncManager

logger = logging.getLogger(__name__)
DEFAULT_PROJ_ROOT_DIR = '/mnt/scf'


class SandboxProjManager:

    def __init__(self, proj_root_dir: str = DEFAULT_PROJ_ROOT_DIR):
        self.proj_root_dir = proj_root_dir

    def walk_json(self):

        root_dir = self.proj_root_dir
        if not os.path.exists(root_dir):
            root_dir = DEFAULT_PROJ_ROOT_DIR

        if not os.path.exists(root_dir):
            raise SystemError(f'系统找不到沙盒函数目录{root_dir}')

        code_version = os.getenv('code_version')
        if root_dir == DEFAULT_PROJ_ROOT_DIR and code_version:
            # 查看索引文件是否存在
            index_file_dir = os.path.join(root_dir, 'func_index', os.getenv('env'), code_version + '_func.csv')
            if not os.path.exists(index_file_dir):
                raise FileNotFoundError(f'未找到沙盒函数索引文件：{index_file_dir}')
            logger.info(f'线上模式，将从索引文件中加载所有沙盒函数：{index_file_dir}')
            SandboxFuncManager.read_repo_by_index(root_dir, index_file_dir)
        else:
            logger.info(f'本地模式，将从{root_dir}加载所有沙盒函数')
            for proj_name in os.listdir(root_dir):
                proj_dir = os.path.join(root_dir, proj_name)
                if os.path.isdir(proj_dir):
                    logger.info(f'加载{proj_dir}沙盒函数项目')
                    SandboxFuncManager.read_repo_path(proj_dir)
