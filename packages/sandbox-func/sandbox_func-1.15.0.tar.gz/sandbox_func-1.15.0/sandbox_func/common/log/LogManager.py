from sandbox_func.common.config.LoginConfig import DefaultLoginConfig


class LogManager:

    @staticmethod
    def enable_debug():
        DefaultLoginConfig.set_debug(True)
        DefaultLoginConfig.save()

    @staticmethod
    def disable_debug():
        DefaultLoginConfig.set_debug(False)
        DefaultLoginConfig.save()

    @staticmethod
    def debug_status():
        return DefaultLoginConfig.get_debug()
