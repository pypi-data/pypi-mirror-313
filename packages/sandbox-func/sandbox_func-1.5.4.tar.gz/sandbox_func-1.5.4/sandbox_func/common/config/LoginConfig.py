import logging
import os
from configparser import ConfigParser
from pathlib import Path

from sandbox_func.common.config.ConfigModel import ConfigModel
from sandbox_func.common.lang.dictclass import DictClass

CONFIG_PATH = Path.home().joinpath(".autowork/config.ini")
logger = logging.getLogger(__file__)


def set_config_file_path(path):
    global CONFIG_PATH
    CONFIG_PATH = path


def get_config_file_path():
    global CONFIG_PATH
    return CONFIG_PATH


class LoginConfig(ConfigModel):
    unit_test: bool = False

    def __init__(self, config_path=None):
        if config_path is None:
            config_path = get_config_file_path()
            if not config_path.exists() and self.get_env():  # 用户目录不存在config.ini且配置了env环境变量，在项目目录下提取config.ini
                set_config_file_path(Path(__file__).parent.joinpath("config.ini"))
                config_path = get_config_file_path()
            logger.info(f"config_path:{str(config_path)}")

        self.config_path = config_path
        self.config = LoginConfig.init_config(config_path)
        self.data = dict()
        for section in self.config.sections():
            d = dict()
            for k, v in self.config.items(section):
                d[k] = v
            self.data[section] = DictClass(d)

    @staticmethod
    def init_config(config_path):
        # allow_no_value设置为True以支持配置文件中添加注释
        config = ConfigParser(allow_no_value=True)
        # 配置文件内容区分大小写
        config.optionxform = lambda option: option
        config.read(config_path, encoding='utf-8')
        return config

    def __getattr__(self, item):
        if item in ["config", "data", "config_path"]:
            return object.__getattribute__(self, item)
        if item not in self.data:
            self.data[item] = DictClass()
        return self.data[item]

    def get(self, item) -> any:
        return self.__getattr__(item)

    def save(self, path=None):
        if path is None:
            path = self.config_path

        config = ConfigParser(allow_no_value=True)
        config.optionxform = lambda option: option
        for k in self.data:
            config[k] = self.data[k]

        dir_path = Path(path).parent.resolve()
        Path(dir_path).mkdir(parents=True, exist_ok=True)

        with open(path, 'w') as configfile:
            config.write(configfile)

    def set_env(self, env):
        self.get_global_config().ENV = env
        os.environ["env"] = env

    def get_env(self):
        return os.getenv('env').upper() if isinstance(os.getenv('env'), str) else self.get_global_config().ENV

    def set_debug(self, debug):
        self.get_global_config().DEBUG = debug

    def get_debug(self):
        return True if self.get_global_config().get("DEBUG") in {'True', True} else False

    def get_global_config(self) -> DictClass:
        if "GLOBAL_CONFIG" not in self.data:
            self.data["GLOBAL_CONFIG"] = DictClass()
        return self.data["GLOBAL_CONFIG"]

    def get_dev_apps(self):
        return self.get_global_config().get("DEV_APPS")

    def set_dev_apps(self, dev_apps):
        self.get_global_config().DEV_APPS = dev_apps

    def set_api_key(self, api_key):
        product_env = self.get_product_env_str()
        if product_env not in self.data:
            self.data[product_env] = DictClass()
        self.data[product_env]['API_KEY'] = api_key

    def get_api_key(self):
        product_env = self.get_product_env_str()
        if product_env not in self.data:
            self.data[product_env] = DictClass()
        api_key = self.data[product_env].get('API_KEY')
        return api_key

    def set_product(self, product_name):
        self.get_global_config().PRODUCT = product_name

    def get_product(self):
        return os.getenv('product') or self.get_global_config().get("PRODUCT", 'CYBOTRON')

    def set_tenant_id(self, tenant_id):
        self.get_global_config().TENANT_ID = tenant_id

    def get_tenant_id(self):
        return self.get_global_config().get("TENANT_ID")

    def get_product_env_str(self):
        product = self.get_product()
        env = self.get_env()
        return f"{product}-{env}"

    @property
    def is_online(self):
        return True if os.getenv('BUSINESS_KEY') else False

    def __str__(self):
        return str(self.data)

    def __repr__(self):
        return self.__str__()


DefaultLoginConfig = LoginConfig()
