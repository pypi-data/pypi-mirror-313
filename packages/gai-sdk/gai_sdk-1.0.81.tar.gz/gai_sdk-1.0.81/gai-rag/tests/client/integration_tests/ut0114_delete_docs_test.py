import asyncio,json
from gai.lib.common.errors import ApiException
from gai.lib.common.logging import getLogger
logger = getLogger(__name__)


config_type = "local"
from gai.lib.common.utils import this_dir
from gai.rag.client.rag_client_async import RagClientAsync
here=this_dir(__file__)
rag = RagClientAsync({
    "type":"rag",
    "url":"http://localhost:12036/gen/v1/rag"
})

try:
    result = asyncio.run(rag.delete_document_async("demo","PwR6VmXqAfwjn84ZM6dePsLWTldPv8cNS5dESYlsY2U"))
    print(json.dumps(result))
except ApiException as e:
    if e.code == "document_not_found":
        logger.info("document not found.")
except Exception as e:
    logger.error(e)

