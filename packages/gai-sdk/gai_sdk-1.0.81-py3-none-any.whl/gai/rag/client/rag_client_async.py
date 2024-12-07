import asyncio
import os
import json
from typing import Optional, Union
from gai.rag.client.dtos.indexed_doc import IndexedDocPydantic
import websockets

from gai.lib.common.http_utils import http_post_async, http_get_async,http_delete_async, http_put_async
from gai.lib.common.logging import getLogger
logger = getLogger(__name__)
from gai.lib.common.errors import ApiException, DocumentNotFoundException
from gai.lib.common.StatusListener import StatusListener
from gai.lib.common.utils import get_gai_config, get_gai_url
from gai.rag.client.dtos.create_doc_header_request import CreateDocHeaderRequestPydantic
from gai.rag.client.dtos.update_doc_header_request import UpdateDocHeaderRequestPydantic
from gai.rag.client.dtos.indexed_doc_chunkgroup import IndexedDocChunkGroupPydantic
from gai.rag.client.dtos.indexed_doc_chunk_ids import IndexedDocChunkIdsPydantic

class RagClientAsync:

    def __init__(self,config:Optional[Union[str,dict]]=None):
        if config is str or config is None:
            self.config=get_gai_config(file_path=config)
            self.config = self.config["clients"]["gai-rag"]
            self.base_url = get_gai_url("rag")
        else:
            self.config = config
            self.base_url = config["url"]        

    def _prepare_files_and_metadata(self, collection_name, file_path, metadata):
        mode = 'rb' if file_path.endswith('.pdf') else 'r'
        with open(file_path, mode) as f:
            files = {
                "file": (os.path.basename(file_path), f if mode == 'rb' else f.read(), "application/pdf"),
                "metadata": (None, json.dumps(metadata), "application/json"),
                "collection_name": (None, collection_name, "text/plain")
            }
            return files


    ### ----------------- MULTI-STEP INDEXING ----------------- ###
    async def step_header_async(
        self,
        collection_name, 
        file_path, 
        file_type="",
        title="",
        source="",
        authors="",
        publisher="",
        published_date="",
        comments="",
        keywords=""         
        ) -> IndexedDocPydantic:

        url=os.path.join(self.base_url,"step/header")
        create_doc_header_req=CreateDocHeaderRequestPydantic(
            CollectionName=collection_name,
            FilePath=file_path,
            FileType=file_type,
            Source=source,
            Title=title,
            Authors=authors,
            Publisher=publisher,
            PublishedDate = published_date,
            Comments=comments,
            Keywords=keywords
        )


        # Send file
        try:
            mode = 'rb'
            with open(create_doc_header_req.FilePath, mode) as f:
                files = {
                    "file": (os.path.basename(create_doc_header_req.FilePath), f, "application/pdf"),
                    "req": (None, create_doc_header_req.json(), "application/json"),
                }
                response = await http_post_async(url=url, files=files)
                if not response:
                    raise Exception("No response received")
                pydantic=response.json()
                return IndexedDocPydantic(**pydantic)
        except Exception as e:
            logger.error(f"index_document_header_async: Error creating document header. error={e}")
            raise e


    async def step_split_async(
            self,
            collection_name,
            document_id,
            chunk_size,
            chunk_overlap) -> IndexedDocChunkGroupPydantic:
        url=os.path.join(self.base_url,"step/split")
        try:
            response = await http_post_async(url=url, data={
                "collection_name": collection_name,
                "document_id": document_id,
                "chunk_size": chunk_size,
                "chunk_overlap": chunk_overlap
            })
            return IndexedDocChunkGroupPydantic(**response.json())
        except Exception as e:
            logger.error(f"step_split_async: Error splitting document. error={e}")
            raise e

    async def step_index_async(
            self,
            collection_name,
            document_id,
            chunkgroup_id,
            async_callback=None) -> IndexedDocChunkIdsPydantic:
        url=os.path.join(self.base_url,"step/index")
        try:
            # Spin off listener task if async_callback is provided
            listen_task=None
            if async_callback:
                ws_url=os.path.join(self.base_url,f"index-file/ws/{collection_name}").replace("http","ws")
                listener = StatusListener(ws_url)
                listen_task=asyncio.create_task(listener.listen(async_callback))

            response = await http_post_async(url=url, data={
                "collection_name": collection_name,
                "document_id": document_id,
                "chunkgroup_id":chunkgroup_id
            },timeout=3600)

            # Cancel listener task if it was started
            if listen_task:
                listen_task.cancel()

            return IndexedDocChunkIdsPydantic(**response.json())
        except Exception as e:
            logger.error(f"step_index_async: Error splitting document. error={e}")
            raise e


    ### ----------------- SINGLE-STEP INDEXING ----------------- ###
    async def index_document_async(
        self, 
        collection_name, 
        file_path, 
        file_type="",
        title="",
        source="",
        authors="",
        publisher="",
        published_date="",
        comments="",
        keywords="",
        async_callback=None) -> IndexedDocChunkIdsPydantic:

        # Spin off listener task if async_callback is provided
        listen_task=None
        if async_callback:
            ws_url = self.config["ws_url"]+"/"+collection_name
            listener = StatusListener(ws_url)
            listen_task=asyncio.create_task(listener.listen(async_callback))

        try:
            url=os.path.join(self.base_url,"index-file")
            create_doc_header_req=CreateDocHeaderRequestPydantic(
                CollectionName=collection_name,
                FilePath=file_path,
                FileType=file_type,
                Source=source,
                Title=title,
                Authors=authors,
                Publisher=publisher,
                PublishedDate = published_date,
                Comments=comments,
                Keywords=keywords
            )
        except Exception as e:
            logger.error(f"index_document_async: Error parsing pydantic header request. error={e}")
            # Cancel listener task if it was started
            if listen_task:
                listen_task.cancel()
            raise e

        # Send file
        try:
            mode = 'rb'
            if not os.path.exists(create_doc_header_req.FilePath):
                raise Exception(f"File not found: {create_doc_header_req.FilePath}")
            with open(create_doc_header_req.FilePath, mode) as f:
                files = {
                    "file": (os.path.basename(create_doc_header_req.FilePath), f, "application/pdf"),
                    "req": (None, create_doc_header_req.json(), "application/json"),
                }

                response = await http_post_async(url=url, files=files)
                if not response:
                    raise Exception("No response received")

                return IndexedDocChunkIdsPydantic(**response.json())
        except Exception as e:
            logger.error(f"index_document_async: Error indexing file. error={e}")
            raise e
        finally:
            # Cancel listener task if it was started
            if listen_task:
                listen_task.cancel()

    
    ### ----------------- RETRIEVAL ----------------- ###

    async def retrieve_async(self, collection_name, query_texts, n_results=None):
        url = os.path.join(self.base_url,"retrieve")
        data = {
            "collection_name": collection_name,
            "query_texts": query_texts
        }
        if n_results:
            data["n_results"] = n_results

        response = await http_post_async(url, data=data)
        return response.json()["retrieved"]

#Collections-------------------------------------------------------------------------------------------------------------------------------------------

    async def delete_collection_async(self, collection_name):
        url = os.path.join(self.base_url,"collection",collection_name)
        logger.info(f"RAGClient.delete_collection: Deleting collection {url}")
        try:
            response = await http_delete_async(url)
        except ApiException as e:
            if e.code == 'collection_not_found':
                return {"count":0}
            logger.error(e)
            raise e
        return json.loads(response.text)

    async def list_collections_async(self):
        url = os.path.join(self.base_url,"collections")
        response = await http_get_async(url)
        return json.loads(response.text)

#Documents-------------------------------------------------------------------------------------------------------------------------------------------

    async def list_documents_async(self, collection_name=None) -> list[IndexedDocPydantic]:
        if not collection_name:
            url = os.path.join(self.base_url,"documents")
            response = await http_get_async(url)
            return [IndexedDocPydantic.parse_obj(doc) for doc in response.json()]
    
        url = os.path.join(self.base_url,f"collection/{collection_name}/documents")
        response = await http_get_async(url)
        docs = [IndexedDocPydantic.parse_obj(doc) for doc in response.json()]
        return docs

#Document-------------------------------------------------------------------------------------------------------------------------------------------

    # Response:
    # - 200: { "document": {...} }
    # - 404: { "message": "Document with id {document_id} not found" }
    # - 500: { "message": "Internal error: {id}" }
    async def get_document_header_async(self, collection_name, document_id) -> IndexedDocPydantic:
        try:
            url = os.path.join(self.base_url,f"collection/{collection_name}/document/{document_id}")
            response = await http_get_async(url)
            jsoned = json.loads(response.text)
            pydantic = IndexedDocPydantic.parse_obj(jsoned)
            return pydantic
        except ApiException as e:
            if e.code == 'document_not_found':
                raise DocumentNotFoundException(document_id)
            logger.error(f"RAGClientAsync.update_document_header_async: Error={e}")
            raise e
        except Exception as e:
            logger.error(f"get_document_header_async: Error getting document header. error={e}")
            raise e

    # Response:
    # - 200: { "message": "Document with id {document_id} deleted successfully" }
    # - 404: { "message": "Document with id {document_id} not found" }
    # - 500: { "message": "Internal error: {id}" }
    async def delete_document_async(self,collection_name,document_id):
        try:
            url = os.path.join(self.base_url,f"collection/{collection_name}/document/{document_id}")
            response = await http_delete_async(url)
            return json.loads(response.text)
        except ApiException as e:
            if e.code == 'document_not_found':
                raise DocumentNotFoundException(document_id)
            logger.error(f"RAGClientAsync.update_document_header_async: Error={e}")
            raise e
        except Exception as e:
            logger.error(f"RAGClientAsync.delete_document_async: Error={e}")
            raise e

    # Response:
    # - 200: { "message": "Document updated successfully", "document": {...} }
    # - 404: { "message": "Document with id {document_id} not found" }
    # - 500: { "message": "Internal error: {id}" }
    async def update_document_header_async(self,collection_name,document_id,update_doc_header_req:UpdateDocHeaderRequestPydantic):
        try:
            url = os.path.join(self.base_url,f"collection/{collection_name}/document/{document_id}")
            response = await http_put_async(url,data=update_doc_header_req.model_dump(exclude_none=True))
            return json.loads(response.text)
        except ApiException as e:
            if e.code == 'document_not_found':
                raise DocumentNotFoundException(document_id)
            logger.error(f"RAGClientAsync.update_document_header_async: Error={e}")
            raise e
        except Exception as e:
            logger.error(f"RAGClientAsync.update_document_header_async: Error={e}")
            raise e

    async def get_document_file_async(self,collection_name,document_id,output_path=None):
        try:
            url = os.path.join(self.base_url,f"collection/{collection_name}/document/{document_id}/file")
            response = await http_get_async(url)

            doc = await self.get_document_header_async(collection_name=collection_name,document_id=document_id)
            if not output_path:
                cwd = os.curdir
                output_path=os.path.join(cwd,doc.FileName+"."+doc.FileType)
            with open(output_path,"wb") as f:
                f.write(response.content)
        except Exception as e:
            logger.error(f"RAGClientAsync.get_document_file_async: Error={e}")
            raise e


#Chunkgroup-------------------------------------------------------------------------------------------------------------------------------------------

    async def list_chunkgroup_ids_async(self):
        url = os.path.join(self.base_url,f"chunkgroups")
        response = await http_get_async(url)
        return json.loads(response.text)

    async def get_chunkgroup_async(self,chunkgroup_id):
        url = os.path.join(self.base_url,f"chunkgroup/{chunkgroup_id}")
        response = await http_get_async(url)
        return json.loads(response.text)
    
    # Delete a chunkgroup to resplit and index
    async def delete_chunkgroup_async(self,collection_name, chunkgroup_id):
        url = os.path.join(self.base_url,f"collection/{collection_name}/chunkgroup/{chunkgroup_id}")
        response = await http_delete_async(url)
        return json.loads(response.text)

#Chunks-------------------------------------------------------------------------------------------------------------------------------------------
    # Use this to get chunk ids only
    async def list_chunks_async(self,chunkgroup_id=None):
        if not chunkgroup_id:
            url = os.path.join(self.base_url,"chunks")
            response = await http_get_async(url)
            return json.loads(response.text)
        url = os.path.join(self.base_url,f"chunks/{chunkgroup_id}")
        response = await http_get_async(url)
        return json.loads(response.text)

    # Use this to get chunks of a document from db and vs
    async def list_document_chunks_async(self,collection_name,document_id):
        url = os.path.join(self.base_url,f"collection/{collection_name}/document/{document_id}/chunks")
        response = await http_get_async(url)
        return json.loads(response.text)
    
    # Use this to get a chunk from db and vs
    async def get_document_chunk_async(self,collection_name, chunk_id):
        url = os.path.join(self.base_url,f"collection/{collection_name}/chunk/{chunk_id}")
        response = await http_get_async(url)
        return json.loads(response.text)