import os
os.environ["LOG_LEVEL"]="INFO"

import asyncio
from gai.network.gainet_node import GaiNetNode

class GaiNetServer(GaiNetNode):

    def __init__(self, servers, node_name):
        super().__init__(servers,node_name)

    @staticmethod
    async def create(servers,node_name):
        node = GaiNetServer(servers=servers, node_name=node_name)
        await node.connect()
        return node

    async def serve(self):
        await self.nc.subscribe("system.ping", cb=self.ping_handler)
        await self.listen()

async def main():
    node = await GaiNetServer.create(servers="nats://localhost:4222",node_name="Sara")
    await node.serve()

if __name__ == "__main__":
    asyncio.run(main())
