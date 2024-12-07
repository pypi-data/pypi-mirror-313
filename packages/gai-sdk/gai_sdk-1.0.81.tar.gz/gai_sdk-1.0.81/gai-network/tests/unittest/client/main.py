import os
os.environ["LOG_LEVEL"]="INFO"

import asyncio
from gai.network.gainet_node import GaiNetNode

class GaiNetClient(GaiNetNode):

    def __init__(self, servers, node_name):
        super().__init__(servers,node_name)
        self.pong_inbox = self.nc.new_inbox()

    @staticmethod
    async def create(servers,node_name):
        node = GaiNetClient(servers=servers, node_name=node_name)
        await node.connect()
        return node

    async def subscribe(self):
        await self.nc.subscribe(self.pong_inbox, cb=self.pong_handler)

    async def ping(self):
        await self.nc.publish("system.ping", self.node_name.encode(), self.pong_inbox)
        await asyncio.sleep(5)
        print(f"Aggregated Responses: {self.messages}")

async def main():
    node = await GaiNetClient.create(servers="nats://localhost:4222",node_name="User")
    await node.subscribe()
    await node.ping()
    await node.listen()

if __name__ == "__main__":
    asyncio.run(main())

