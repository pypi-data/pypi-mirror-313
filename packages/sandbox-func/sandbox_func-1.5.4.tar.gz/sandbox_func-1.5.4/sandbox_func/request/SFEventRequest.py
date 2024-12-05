from sandbox_func.request.SFExtRequest import SFExtRequest


class SFEventRequest(SFExtRequest):
    """Event类函数请求"""

    func_type: str = 'event'
