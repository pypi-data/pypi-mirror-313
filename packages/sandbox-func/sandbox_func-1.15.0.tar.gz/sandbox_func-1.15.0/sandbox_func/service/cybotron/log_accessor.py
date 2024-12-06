from sandbox_func.common.config.BusinessURLConfig import BusinessURLConfig, DataTypeEnum
from sandbox_func.common.config.LogConfig import LOG_APP_CODE, LOG_TABLE_CODE
from sandbox_func.common.request.CybotronSyncClient import CybotronSyncClient


class LogAccessor:

    @staticmethod
    def send_log(log_message: dict) -> bool:
        business_url = f"{BusinessURLConfig.get_url(DataTypeEnum.DATA)}/{LOG_APP_CODE}/{LOG_TABLE_CODE}/create"
        req = {
            "values": log_message,
            "options": {
                "conflictToUpdate": False
            }
        }

        client = CybotronSyncClient()
        res = client.post(business_url, json=req)
        if res.is_success:
            return True
        else:
            return False
