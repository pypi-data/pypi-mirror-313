
import asyncio
import nats
from nats.aio.msg import Msg
from abc import ABC, abstractmethod
from gai.lib.common.logging import getLogger
logger = getLogger(__name__)

class GaiNetNodeMessage:
    # def __init__(self, subject_type:str=None, subject_params:str=None, message:str=None):
        # self.subject_type=subject_type
        # self.subject_params=subject_params
        # self.message=message

    def __init__(self,msg: Msg):
        self.subject_type=msg.subject.split(":")[0]
        self.subject_params=msg.subject.split(":")[1].split(".")
        self.message=msg.data.decode('utf-8')        

class GaiNetNode(ABC):
    
    def __init__(self, servers, node_name):
        self.servers = servers
        self.node_name = node_name
        self.nc = None

    async def connect(self):
        try:
            self.nc = await nats.connect(servers=self.servers)
            logger.info("GaiNetNode.connect: Ready.")
        except Exception as e:
            logger.error(f"GaiNetNode.connect: Failed to connect to gai network. {e}")

    async def send_raw(self, subject, msg):
        payload = msg.encode("utf-8")
        await self.nc.publish(subject,payload)

    async def pong(self,recipient):
        subject_type = "system.pong"
        await self.send_raw(f"{subject_type}:{self.node_name}.{recipient}", "PONG")
        logger.info(f"GaiNetNode.pong: pong ({recipient})")

    async def ping(self,recipient=None):
        subject_type = "system.ping"
        if not recipient:
            recipient = ">"
            logger.info(f"GaiNetNode.ping: ping (ALL)")
        else:
            logger.info(f"GaiNetNode.ping: ping ({recipient})")
        await self.send_raw(f"{subject_type}:{self.node_name}.{recipient}", "PING")

    async def route(self,msg):
        
        if len(msg.subject.split(":")) < 2:
            em = f"GaiNetNode.route: Invalid subject {msg.subject}"
            logger.error(em)
            raise ValueError(em)

        # gainet_msg = GaiNetNodeMessage(
        #     subject_type=msg.subject.split(":")[0],
        #     subject_params=msg.subject.split(":")[1].split("."),
        #     message=msg.data.decode('utf-8')
        # )
        gainet_msg = GaiNetNodeMessage(msg)
        
        if gainet_msg.subject_type == "system.ping":
            sender = gainet_msg.subject_params[0]
            recipient = gainet_msg.subject_params[1]

            # ignore message from self
            if sender == self.node_name:
                return
            
            # Process message to self
            if recipient == self.node_name or recipient == ">":
                logger.info(f"GaiNetNode.route: ping ({sender})")
                await self.pong(sender)
            return        

        if gainet_msg.subject_type == "system.pong":
            sender = gainet_msg.subject_params[0]
            recipient = gainet_msg.subject_params[1]

            # ignore message from self
            if sender == self.node_name:
                return

            # Process message to self
            if recipient == self.node_name or recipient == ">":
                logger.info(f"GaiNetNode.route: pong ({sender})")
            return

        return gainet_msg        

    async def close(self):
        await self.nc.close()
