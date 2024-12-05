import logging
import asyncio
from threading import Thread
import httpx
import json
import time

class FeiShuWebhookHandler(logging.Handler):
    """
    通过webhook将自定义服务的消息推送至飞书
    """
    connection = None

    def __init__(self, webhook_url,key_word="feishu"):
        logging.Handler.__init__(self)
        self.url = webhook_url
        self.key_word = key_word

    def mapLogRecord(self, record):
        """
        Default implementation of mapping the log record into a dict
        that is sent as the CGI data. Overwrite in your class.
        Contributed by Franz Glasner.
        """
        return record.__dict__

    def getConnection(self):
        """
        get a HTTP[S]Connection.

        Override when a custom connection is required, for example if
        there is a proxy.
        """
        if not FeiShuWebhookHandler.connection:
            FeiShuWebhookHandler.connection = httpx.AsyncClient(default_encoding="utf-8")
        
        return FeiShuWebhookHandler.connection
    
    # @staticmethod
    # async def post2(connection,url,payload_message):
    #     print("post2 start")
    #     res = await connection.post(url=url,json=payload_message)
    #     print("post2 end")
    @staticmethod
    async def post(connection,url,payload_message):
        print("start post")
        res = await FeiShuWebhookHandler.post2(connection,url,payload_message)
        print("end post")
        return res
        # await asyncio.sleep(2)

    @staticmethod
    def send(connection,url,payload_message):
        asyncio.run(FeiShuWebhookHandler.post(connection,url,payload_message))

    @staticmethod
    async def test(fut):
        print(1)
        await asyncio.sleep(2)
        print(2)
        fut.set_result("666")

    @staticmethod
    async def main():
        print(111)
        loop = asyncio.get_running_loop()
        fut = loop.create_future()
        loop.create_task(FeiShuWebhookHandler.test(fut))
        # await FeiShuWebhookHandler.test(fut)
        await fut
        print(222)


    def emit(self, record):
        """
        Emit a record.
        """
        try:
            timeArray = time.localtime(int(record.created))
            otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            payload_message = {
                "msg_type": "text",
                "content": {
                    # @ 单个用户 <at user_id="ou_xxx">名字</at>
                    "text": "[{}] [{}] ".format(otherStyleTime,self.key_word) + record.msg + "\r\n" + json.dumps(self.mapLogRecord(record),indent=1,ensure_ascii=False)
                    # @ 所有人 <at user_id="all">所有人</at>
                    # "text": content + "<at user_id=\"all\">test</at>"
                }
            }

            # connection = self.getConnection()
            # url = self.url

            asyncio.run(FeiShuWebhookHandler.main())


            print("end emit")
            


            

            # t1 = Thread(target=FeiShuWebhookHandler.send, args=(connection,url,payload_message,))
            # t1.start()
            # join() 等待线程终止，要不然一直挂起
            
        except Exception:
            self.handleError(record)

if __name__ == "__main__":
    record = {}
    asyncio.run(FeiShuWebhookHandler("").emit(record))
        
