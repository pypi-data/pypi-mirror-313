import uvicorn

from sandbox_func.web import sandbox_app


class SandboxFuncServer:
    @classmethod
    def start(cls, port: int, reload: bool = False):
        """
        服务启动入口，提供给业务代码使用
        :param port: 端口号
        :param reload:
        :return:
        """
        uvicorn.run(sandbox_app.app, host="0.0.0.0", port=port, log_level="info", reload=reload)
