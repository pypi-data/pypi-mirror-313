import logging
# import asyncio
from threading import Thread
import httpx
import json
import time
from cachetools import LRUCache, TTLCache
import base64
import traceback

class FeiShuWebhookHandler(logging.Handler):
    """
    通过webhook将自定义服务的消息推送至飞书
    """
    connection = None
    cache = TTLCache(maxsize=1024,ttl=60)

    def __init__(self,webhook_url,key_word="feishu",cache_time=0,filter_key=[],simple_log_levelno=logging.ERROR,simple_format = "",At=None):
        """_summary_

        Args:
            webhook_url (_type_): _description_
            key_word (str, optional): 机器人关键词（配合机器人过滤用） Defaults to "feishu".
            cache_time (int, optional): 多少秒不再输出同一个错误，避免同一个错误频繁抛出造成机器人卡死（0为不限制） Defaults to 0.
            filter_key (list, optional): 全量输出时，过滤出哪些key Defaults to [].
            simple_log_levelno (int, optional): 异常等级超过多少则全量输出内容，否则简化输出 Defaults to 40.
            simple_format (str, optional): 类似这样的格式： %(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s - %(message)s
            At (list, optional): https://open.feishu.cn/document/client-docs/bot-v3/add-custom-bot?lang=zh-CN#756b882f // @ 单个用户 <at user_id="ou_userid">名字</at>   // @ 所有人 <at user_id="all">所有人</at>
        """
        logging.Handler.__init__(self)
        self.url = webhook_url
        self.key_word = key_word
        self.cache_time = cache_time
        if cache_time>0:
            self.cache = TTLCache(maxsize=1024,ttl=cache_time)
        self.filter_key = filter_key
        self.simple_log_levelno = simple_log_levelno
        self.simple_format = simple_format
        self.At = At

    def mapLogRecord(self, record):
        """
        Default implementation of mapping the log record into a dict
        that is sent as the CGI data. Overwrite in your class.
        Contributed by Franz Glasner.
        """
        if self.filter_key:
            result = {}
            for key in self.filter_key:
                if key in record.__dict__:
                    if type(record.__dict__[key]) != str:
                        result[key] = str(record.__dict__[key])
                    else:
                        result[key] = record.__dict__[key]
            return result
        else:
            return record.__dict__

    def getText(self,record):
        stack_info = ""
        timeArray = time.localtime(int(record.created))
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        if "stack_info" in self.filter_key:
            # if not record.stack_info:
            #     record.stack_info = "请看最后面详情"
            stack_info = traceback.format_exc()
        
        record.asctime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(record.created)))
        record.message = record.getMessage()
        self.msecs = int((record.created - int(record.created)) * 1000) + 0.0

        text = ""
        if record and hasattr(record,"levelno") and record.levelno<self.simple_log_levelno and self.simple_format: #部分输出 简化输出
            values = record.__dict__
            text = f"[{self.key_word}] - "+self.simple_format%values
            return text
        else:
            text = f"[{self.key_word}] [{otherStyleTime}] \r\n" + json.dumps(self.mapLogRecord(record),indent=1,ensure_ascii=False) + "\r\n" + stack_info
            return text


    @classmethod
    def getConnection(cls):
        """
        get a HTTP[S]Connection.

        Override when a custom connection is required, for example if
        there is a proxy.
        """
        if not cls.connection:
            cls.connection = httpx.Client(default_encoding="utf-8")
        
        return cls.connection

    @staticmethod
    def post(connection:httpx.Client,url,payload_message):
        try:
            res = connection.post(url=url,json=payload_message)
            if res.status_code!=200:
                print("feishu logging handler error : {}".format(res.text))
        except Exception as e:
            print("feishu logging handler error : {}".format(e))
    
    @staticmethod
    def send(connection,url,payload_message):
        # asyncio.run(FeiShuWebhookHandler.post(connection,url,payload_message))
        FeiShuWebhookHandler.post(connection,url,payload_message)

    def emit(self, record):
        """
        Emit a record.
        """
        try:
            text = self.getText(record)

            if record.levelno>=40 and self.At and type(self.At)==list:
                at_text = ""
                for userid in self.At:
                    if userid=="all":
                        at_text = at_text + " <at user_id=\"all\">所有人</at>"
                    else:
                        at_text = at_text + f" <at user_id=\"ou_{userid}\">userid</at>"

                if at_text:
                    text = text + at_text

            payload_message = {
                "msg_type": "text",
                "content": {
                    # @ 单个用户 <at user_id="ou_xxx">名字</at>
                    "text": text
                    # @ 所有人 <at user_id="all">所有人</at>
                    # "text": content + "<at user_id=\"all\">test</at>"
                }
            }

            # 判断是否要推送
            if self.cache_time!=0:
                b = base64.b64encode(bytes(str(record.msg), 'utf-8')) # bytes
                base64_str = b.decode('utf-8') # convert bytes to string
                value = self.cache.get(base64_str)
                if value:
                    # print("feishu logger 命中缓存略过本条消息")
                    return
                else:
                    self.cache[base64_str] = base64_str

            connection = self.getConnection()
            url = self.url

            # asyncio.run(FeiShuWebhookHandler.post(connection,url,payload_message))
            # print("end 这里应该是最先出现的")

            t1 = Thread(target=FeiShuWebhookHandler.send, args=(connection,url,payload_message,))
            t1.start()
            # join() 等待线程终止，要不然一直挂起
            
        except Exception:
            self.handleError(record)
        
