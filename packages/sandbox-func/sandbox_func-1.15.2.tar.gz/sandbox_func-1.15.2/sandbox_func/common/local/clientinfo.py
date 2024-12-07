import socket
from sys import platform

import psutil


class ClientInfo:
    @staticmethod
    def get_ip() -> str:
        """
        获取本机IP地址
        :return:
        """
        s = None
        if "linux" == platform:
            for k, v in psutil.net_if_addrs().items():
                if len(v) < 2:
                    continue
                if k.startswith("lo"):
                    continue
                else:
                    return v[0].address
        else:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(('8.8.8.8', 80))
                ip = s.getsockname()[0]
            finally:
                s.close()
            return ip
