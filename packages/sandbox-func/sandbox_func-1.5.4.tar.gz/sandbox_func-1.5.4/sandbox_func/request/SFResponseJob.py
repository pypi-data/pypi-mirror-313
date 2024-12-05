import logging
import json

from sandbox_func.repository.cybotron.service.sandbox_accessor import SandboxAccessor

logger = logging.getLogger(__name__)


class SFResponseJob:

    def __init__(self):
        self.job_error: str = ''
        self.job_success: str = ''
        self.job_progress: int = 0
        self.request_id: str = ''
        self.job_id: str = ''

    async def progress(self, progress: int):
        self.job_progress = progress
        try:
            await self.send_progress_request()
        except Exception as e:
            logger.exception(e)

    def success(self, success: str):
        self.job_success = success

    def error(self, error: str):
        self.job_error = error

    def set_request_id(self, request_id: str):
        self.request_id = request_id

    def set_job_id(self, job_id: str):
        self.job_id = job_id

    def __str__(self):
        return json.dumps({"progress": self.job_progress, "success": self.job_success, "error": self.job_error,
                           "request_id": self.request_id, "job_id": self.job_id, "type": "job_response"})

    def __repr__(self):
        return self.__str__()

    async def send_progress_request(self):
        return await SandboxAccessor.update_async_job(self.job_id, "PROCESSING", self.job_progress)
