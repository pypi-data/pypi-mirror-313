import asyncio,json
from gai.lib.common.logging import getLogger
logger = getLogger(__name__)
logger.setLevel("DEBUG")

config_type = "local"
from gai.lib.common.utils import this_dir
from gai.rag.client.rag_client_async import RagClientAsync
here=this_dir(__file__)
rag = RagClientAsync({
    "type":"rag",
    "url":"http://localhost:12036/gen/v1/rag"
})

async def main():
    try:
        result = await rag.list_collections_async()
        logger.info("COLLECTIONS:")
        logger.info(json.dumps(result))

        result = await rag.list_documents_async()
        logger.info("DOCUMENTS:")
        logger.info(json.dumps(result))

        result = await rag.list_documents_async("demo")
        logger.info("DOCUMENTS BY COLLECTION:")
        logger.info(json.dumps(result))

        result = await rag.get_document_header_async("demo","PwR6VmXqAfwjn84ZM6dePsLWTldPv8cNS5dESYlsY2U")
        logger.info("DOCUMENT:")
        logger.info(json.dumps(result))

        result = await rag.list_document_chunks_async("demo","PwR6VmXqAfwjn84ZM6dePsLWTldPv8cNS5dESYlsY2U")
        logger.info("CHUNKS:")
        logger.info(json.dumps(result))

        chunk_id = result[-1]
        result = await rag.get_chunk_async("demo",chunk_id)
        logger.info("CHUNK:")
        logger.info(json.dumps(result))


    except Exception as e:
        logger.error(e)

asyncio.run(main())


