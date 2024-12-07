import sys
import uvicorn
import logging

from sandbox_func.web import sandbox_app

logger = logging.getLogger(__name__)


if __name__ == '__main__':
    work_path, port = sys.argv[1:]
    logger.info(f"添加业务代码工作目录：{work_path}")
    uvicorn.run(sandbox_app.app, host="0.0.0.0", port=int(port), log_level="info", app_dir=work_path)
