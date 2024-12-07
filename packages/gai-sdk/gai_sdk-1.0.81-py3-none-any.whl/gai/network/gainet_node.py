import asyncio
from nats.aio.msg import Msg
from nats.aio.client import Client as NATS
from abc import ABC
from gai.lib.common.logging import getLogger
logger = getLogger(__name__)

class GaiNetNode(ABC):
    
    def __init__(self, servers, node_name):
        self.servers = servers
        self.node_name = node_name
        self.nc = NATS()
        self.messages = []

    async def connect(self):
        try:
            await self.nc.connect(servers=self.servers)
            logger.info("GaiNetNode.connect: Ready.")
        except Exception as e:
            logger.error(f"GaiNetNode.connect: Failed to connect to gai network. {e}")

    async def send_raw(self, subject, msg):
        payload = msg.encode("utf-8")
        await self.nc.publish(subject,payload)

    async def ping_handler(self,msg):
        subject=msg.subject
        data = msg.data.decode()
        reply = msg.reply
        self.messages.append({
            "subject":subject,
            "data":data
            })
        logger.info(f"system.ping: {data}")

        # Responding back to the requester
        if reply:
            await self.send_raw(reply,self.node_name)

    async def pong_handler(self,msg):
        subject=msg.subject
        data = msg.data.decode()
        self.messages.append({
            "subject":subject,
            "data":data
            })
        logger.info(f"system.pong: {data}")     


    async def listen(self):
        # Keep the subscriber running
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            pass
        finally:
            # Close the connection
            await self.nc.drain()

    async def flush(self):
        await self.nc.flush(timeout=1)

    async def close(self):
        await self.nc.close()
