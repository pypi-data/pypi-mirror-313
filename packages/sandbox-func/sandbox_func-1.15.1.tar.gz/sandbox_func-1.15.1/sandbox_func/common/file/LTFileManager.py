# -*- coding:utf-8 -*-
from sandbox_func.common.request.CybotronClient import CybotronClient


class LTFileManager:
    """
    多维表文件相关接口
    """

    def __init__(self, app_code, table_code):
        self.app_code = app_code
        self.table_code = table_code
        self.client = CybotronClient()

    async def __send_request(self, url: str, data=None, files=None, json=None):
        """
        :param url: 接口地址
        :param data:
        :param files:
        :param json:
        :return: 接口返回的result
        """
        api_url = '/cbn/api/v1/file2/{}/{}/{}'.format(self.app_code, self.table_code, url)
        response = await self.client.post(url=api_url, data=data, files=files, json=json)
        if not response.get("success"):
            raise Exception(response.get("message"))
        return response["result"]

    async def upload_file(self, data_id: str, column_code: str, file_path: str) -> dict:
        """
        上传文件
        :param data_id: 数据id
        :param column_code: 列编码
        :param file_path: 文件路径
        :return:
        """
        # 读取文件内容
        with open(file_path, 'rb') as f:
            files = {"file": f}
            data = {
                "dataId": data_id,
                "columnCode": column_code
            }
            result = await self.__send_request('upload', data=data, files=files)
            return result

    async def delete_file(self, data_id: str, column_code: str, file_id: str) -> dict:
        """
        删除文件
        :param data_id: 数据id
        :param column_code: 列编码
        :param file_id: 文件id
        :return:
        """
        params_data = {
            "fileId": file_id,
            "dataId": data_id,
            "columnCode": column_code
        }
        result = await self.__send_request('delete', json=params_data)
        return result
