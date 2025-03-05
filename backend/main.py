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
# from agno.agent import Agent, RunResponse
# from agno.models.ollama import Ollama
import asyncio 
# from typing import Iterator, AsyncIterator
        
# async def data_stream(content):
#     # callback = AsyncIteratorCallbackHandler()
#     llm = app.state.model

#     # task = asyncio.create_task(
#     #     llm.agenerate(messages=[[HumanMessage(content=content)]], callbacks=[callback])
#     # )
#     run_response: AsyncIterator[RunResponse] = llm.run(content, stream = True)
    
#     try:
#         for response in run_response:
#             if isinstance(response, RunResponse):
#                 # Extract the content from the RunResponse object
#                 response_content = response.content
                
#                 # Ensure it's a string (or bytes) that can be encoded
#                 if isinstance(response_content, str):
#                     yield response_content.encode()  # Convert to bytes
#                 else:
#                     # If the content is not a string, handle appropriately, e.g., if it's bytes
#                     yield response_content
#     except Exception as e:
#         print(f"Caught exception: {e}")
#     finally:
#         print("Stream success")
#         # await callback.done.wait()  # Ensure the task completes
#         # callback.done.set()
#         # await task  # Make sure the LLM process finishes

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting FastAPI application...")

    # Initialize LLM model
    # model = ChatOllama(
    #     model="llama3.2:1b",
    #     temperature=0,
    #     streaming=True,
    #     verbose=True,
    #     base_url="http://ollama:11434",
    # )

    # model.invoke("Hello, I am a language model. How can I help you?")
    
    # model = Agent(model=Ollama(id="llama3.2:1b", host = "http://ollama:11434"))
    # model.print_response("Hello world")

    # print("Warm-up completed successfully!")
    
    # app.state.model = model

    yield  # FastAPI runs here

    # print("Shutting down FastAPI application...")
    # app.state.model = None  # Cleanup resources if necessary
  
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
    random_uuid = uuid.uuid4()
    await send_stream_of_messages(req.content, random_uuid)
    generator = consume_tokens_from_kafka(str(random_uuid))
    # generator = data_stream(req.content)
    return StreamingResponse(generator, media_type="text/event-stream"
                        , headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)