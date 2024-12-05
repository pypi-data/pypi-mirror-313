import logging
import sys,os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

LOG_FORMAT = "%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.WARNING, format=LOG_FORMAT, encoding='utf-8')

from feishu_logging.handler import FeiShuWebhookHandler
log_feishu = logging.getLogger("feishu")
url = os.environ["feishu_url"]
http_handler = FeiShuWebhookHandler(url,"toll_server",cache_time=60,filter_key=["funcName","message","levelname","args","pathname","lineno","threadName","stack_info"],simple_log_levelno=logging.ERROR,simple_format = LOG_FORMAT,At=["all"])
http_handler.setLevel(logging.DEBUG)
log_feishu.addHandler(http_handler)

import time

class FF():
    def __init__(self) -> None:
        pass

    def zero(self):
        f = 1/0

for a in range(1):
    
    try:
        f= FF()
        f.zero()
    except Exception as e:
        _, _, tb = sys.exc_info()
        # log_feishu.error(e)
        log_feishu.error(e)

    # log_feishu.error("错误测试")
    time.sleep(10)

