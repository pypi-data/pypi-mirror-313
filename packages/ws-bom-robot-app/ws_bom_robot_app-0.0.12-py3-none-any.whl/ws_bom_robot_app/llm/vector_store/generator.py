import os, shutil, traceback
import asyncio
from fastapi import HTTPException
from fastapi.responses import StreamingResponse
from langchain_core.documents import Document
from ws_bom_robot_app.llm.vector_store.loader.base import Loader
from ws_bom_robot_app.llm.models.api import RulesRequest, KbRequest, VectorDbResponse
from ws_bom_robot_app.llm.vector_store.integration.manager import IntegrationManager
from ws_bom_robot_app.llm.utils.faiss_helper import FaissHelper
from ws_bom_robot_app.util import timer

#@timer
async def rules(rq: RulesRequest) -> VectorDbResponse:
  api_key = rq.api_key()
  _config = rq.config()
  db_name = rq.out_name()
  store_path = os.path.join(_config.robot_data_folder, _config.robot_data_db_folder, _config.robot_data_db_folder_store, db_name)
  try:
    await FaissHelper.create([Document(page_content=rule, metadata={"source": "rules"}) for rule in rq.rules], store_path, api_key) #type: ignore
    #FAISS.from_texts([json.dumps({"rule": rule}) for rule in rq.rules], OpenAIEmbeddings(api_key=api_key)).save_local(store_path) #type: ignore
    db_file_path = shutil.make_archive(os.path.join(_config.robot_data_folder, _config.robot_data_db_folder, _config.robot_data_db_folder_out, db_name), "zip", store_path)
    return VectorDbResponse(file = os.path.basename(db_file_path))
  except Exception as e:
    if os.path.exists(store_path):
      shutil.rmtree(store_path)
    return VectorDbResponse(success = False, error = str(e))

#@atimer
async def kb(rq: KbRequest) -> VectorDbResponse:
  import aiofiles
  import aiofiles.os
  os.environ['MPLCONFIGDIR'] = './tmp/.matplotlib'
  from ws_bom_robot_app.llm.models.kb import load_endpoints
  from ws_bom_robot_app.llm.utils.download import download_files
  api_key = rq.api_key()
  _config = rq.config()
  db_name = rq.out_name()
  src_path = os.path.join(_config.robot_data_folder, _config.robot_data_db_folder, _config.robot_data_db_folder_src)
  working_path = os.path.join(src_path, db_name)

  if all([not rq.files,not rq.endpoints,not rq.integrations]):
    return VectorDbResponse(success = False, error = "No files, endpoints or integrations provided")
  else:
    await aiofiles.os.makedirs(src_path, exist_ok=True)
    await aiofiles.os.makedirs(working_path, exist_ok=True)

  loaders = Loader(working_path)
  filter_file_extensions = loaders.managed_file_extensions()

  # Download/copy all files
  if rq.files:
    try:
      files_to_download = [file for file in rq.files if not os.path.exists(os.path.join(src_path, os.path.basename(file)))]
      if files_to_download:
        await download_files(
          [f"{_config.robot_cms_host}/{_config.robot_cms_kb_folder}/{os.path.basename(file)}" for file in files_to_download if any([file.endswith(ext) for ext in filter_file_extensions])],
          src_path, authorization=_config.robot_cms_auth)
      # copy files to working tmp folder
      for file in rq.files:
        async with aiofiles.open(os.path.join(src_path, os.path.basename(file)), 'rb') as src_file:
          async with aiofiles.open(os.path.join(working_path, os.path.basename(file)), 'wb') as dest_file:
            await dest_file.write(await src_file.read())
    except Exception as e:
      return VectorDbResponse(success = False, error = f"Failed to download file {e}")

  documents: list[Document] = []

  if rq.endpoints:
    try:
      documents.extend(await load_endpoints(rq.endpoints, working_path))
    except Exception as e:
      tb = traceback.format_exc()
      return VectorDbResponse(success = False, error = f"Endpoint failure: {e} | {tb}")

  if rq.integrations:
    tasks = []
    for integration in rq.integrations:
      tasks.append(
        IntegrationManager
        .get_strategy(integration.type.lower(), working_path, integration.__pydantic_extra__) #type: ignore
        .load()
      )
    try:
      integration_documents = await asyncio.gather(*tasks)
      for docs in integration_documents:
        documents.extend(docs)
    except Exception as e:
      tb = traceback.format_exc()
      return VectorDbResponse(success=False, error=f"Integration failure: {e} | {tb}")

  try:
    documents.extend(await loaders.load())
  except Exception as e:
    tb = traceback.format_exc()
    return VectorDbResponse(success = False, error = f"Failed to load files {e} | {tb}")
  finally:
    await aiofiles.os.wrap(shutil.rmtree)(working_path)

  if documents and len(documents) > 0:
    try:
      store_path = os.path.join(_config.robot_data_folder, _config.robot_data_db_folder, _config.robot_data_db_folder_store, db_name)
      # create db
      await FaissHelper.create(documents,store_path,api_key) #type: ignore
      # zip db
      db_file_path = await aiofiles.os.wrap(shutil.make_archive)(os.path.join(_config.robot_data_folder, _config.robot_data_db_folder, _config.robot_data_db_folder_out, db_name), "zip", store_path)
      return VectorDbResponse(file = os.path.basename(db_file_path))
    except Exception as e:
      return VectorDbResponse(success = False, error = str(e))
  else:
    return VectorDbResponse(success = False, error = "No documents found in the knowledgebase folder")

async def kb_stream_file(filename: str):
    from ws_bom_robot_app.config import config

    file_path = os.path.join(config.robot_data_folder, config.robot_data_db_folder, config.robot_data_db_folder_out, filename)
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    def iter_file():
        with open(file_path, mode="rb") as file:
            while chunk := file.read(1024*8):
                yield chunk
    return StreamingResponse(iter_file(), media_type="application/octet-stream", headers={"Content-Disposition": f"attachment; filename={filename}"})
