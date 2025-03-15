from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
# import asyncio
import uvicorn
from pydantic import BaseModel, Field
# from langchain_ollama import ChatOllama
# from langchain.callbacks import AsyncIteratorCallbackHandler
# from langchain.schema import HumanMessage
from contextlib import asynccontextmanager
from kafka_producer import send_stream_of_messages
# from kafka_delete import delete_all_kafka_topics
from kafka_consumer import consume_tokens_from_kafka
import uuid
# from elasticsearch import Elasticsearch
from agno.agent import Agent, RunResponse
from agno.models.ollama import OllamaChat
import asyncio 
from typing import Iterator, AsyncIterator
from textwrap import dedent
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer
import asyncio
# from agno.tools.duckduckgo import DuckDuckGoTools
# from agno.knowledge.pdf import PDFKnowledgeBase
# from agno.vectordb.pgvector import PgVector
# from agno.embedder.ollama import OllamaEmbedder
# from agno.document.base import Document
# from agno.knowledge.document import DocumentKnowledgeBase
import json
from agno.workflow import RunEvent, RunResponse, Workflow

model = OllamaChat(id="llama3.2:1b", host="http://localhost:11434")
# embed_model = SentenceTransformer('all-mpnet-base-v2')

# def get_rag_info(content):
#     # rag_info = ''
#     es = Elasticsearch(
#     "http://localhost:9200",
# )
#     if es.ping():
#         print('Connected to ES!')
#     else:
#         print('Could not connect to ES!')
#         exit(1)
#     max_candi = es.count(index="rag")["count"]
#     if max_candi > 0:
#         query = {
#         "field" : "SummaryVector",
#         "query_vector" : embed_model.encode(content),
#         "k" : 5,
#         "num_candidates" : max_candi , 
#     }
#         res = es.knn_search(index="rag", knn=query , source=["Type","Session","Content","Summary"])
#         results = []

#         for hit in res['hits']['hits']:
#             source_data = hit['_source']
#             results.append({
#                 "Type": source_data.get("Type"),
#                 "Session": source_data.get("Session"),
#                 "Content": source_data.get("Content"),
#                 "Summary": source_data.get("Summary")
#             })
        
#         return json.dumps(results, indent=2)

async def data_stream(content):
    llm = Agent(model=model, 
                # context = {"rag":get_rag_info(content) },
                instructions=dedent("""\
                You are VERON, an IC design assistant.
                Your task is to provide assistance in IC design. If the answer includes code, return the answer in properly formatted code blocks.

                You will answer based on the following context:
                    {rag}\
                """),   
                # knowledge = knowledge_base,
                # tools=[DuckDuckGoTools()],
                # show_tool_calls = True,
                markdown=True,
                # add_references= True
                )



    run_response: AsyncIterator[RunResponse] = await llm.arun(content, stream = True)
    try:
        async for response in run_response:
            if isinstance(response, RunResponse):
                # Extract the content from the RunResponse object
                response_content = response.content
                yield response_content
    except Exception as e:
        print(f"Caught exception: {e}")
    finally:
        print("Stream success")

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting FastAPI application...")
    yield  # FastAPI runs here

  
app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class Item(BaseModel):
    content: str = Field(...)

@app.post("/api/chat")
async def ask(req: Item):
    # random_uuid = uuid.uuid4()
    # await send_stream_of_messages(req.content, random_uuid)
    # generator = consume_tokens_from_kafka(str(random_uuid))
    generator = data_stream(req.content)
    return StreamingResponse(generator, media_type="text/event-stream"
                        # , headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"}
                        )

if __name__ == "__main__":
    # db_url = "postgresql+psycopg://ai:ai@localhost:5555/ai"
    
    # fun_facts = """
    # - Earth is the third planet from the Sun and the only known astronomical object to support life.
    # - Approximately 71% of Earth's surface is covered by water, with the Pacific Ocean being the largest.
    # - The Earth's atmosphere is composed mainly of nitrogen (78%) and oxygen (21%), with traces of other gases.
    # - Earth rotates on its axis once every 24 hours, leading to the cycle of day and night.
    # - The planet has one natural satellite, the Moon, which influences tides and stabilizes Earth's axial tilt.
    # - Earth's tectonic plates are constantly shifting, leading to geological activities like earthquakes and volcanic eruptions.
    # - The highest point on Earth is Mount Everest, standing at 8,848 meters (29,029 feet) above sea level.
    # - The deepest part of the ocean is the Mariana Trench, reaching depths of over 11,000 meters (36,000 feet).
    # - Earth has a diverse range of ecosystems, from rainforests and deserts to coral reefs and tundras.
    # - The planet's magnetic field protects life by deflecting harmful solar radiation and cosmic rays.
    # """

    # # Load documents from the data/docs directory
    # documents = [Document(content=fun_facts)]

    # # Database connection URL
    # db_url = "postgresql+psycopg://ai:ai@localhost:5555/ai"

    # # Create a knowledge base with the loaded documents
    # knowledge_base = DocumentKnowledgeBase(
    #     table_name="documents",
    #     db_url=db_url,
    #     embedder=OllamaEmbedder(id="llama3.2:1b")
    # ),

    # knowledge_base.load(recreate=False)
    uvicorn.run(app, host="0.0.0.0", port=8000)