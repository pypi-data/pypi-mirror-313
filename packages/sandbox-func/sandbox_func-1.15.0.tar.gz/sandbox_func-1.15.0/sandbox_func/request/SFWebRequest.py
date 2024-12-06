from sandbox_func.request.SFExtRequest import SFExtRequest


class SFWebRequest(SFExtRequest):
    """Web函数请求"""

    func_type: str = 'web'
    apigw_url: str
    func_path: str
    http_method: str
