import os
os.environ["LOG_LEVEL"]="INFO"
import asyncio
from gai.network.gainet_node import GaiNetNode

class GaiNetClient(GaiNetNode):

    def __init__(self, servers, node_name):
        super().__init__(servers,node_name)

    @staticmethod
    async def create(servers,node_name):
        node = GaiNetClient(servers=servers, node_name=node_name)
        await node.connect()
        return node

    async def subscribe(self):
        await self.nc.subscribe(">", cb=self.route)

    async def listen(self):
        # Keep the server running indefinitely
        await asyncio.Event().wait()


async def main():
    node = await GaiNetClient.create(servers="nats://localhost:4222",node_name="User")
    await node.subscribe()
    await node.ping()
    await node.listen()

if __name__ == "__main__":
    asyncio.run(main())