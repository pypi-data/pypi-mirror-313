import logging

logger = logging.getLogger(__name__)


class ModuleUtil:
    @staticmethod
    def get_func(kls):
        try:
            parts = kls.split('.')
            module = ".".join(parts[:-1])
            m = __import__(module)
            for comp in parts[1:]:
                m = getattr(m, comp)
            return m
        except Exception as e:
            logger.warning("引入函数({})失败: {}".format(kls, e))
            return None
