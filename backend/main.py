from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import uvicorn
from pydantic import BaseModel, Field
from langchain_ollama import ChatOllama
from langchain.callbacks import AsyncIteratorCallbackHandler
from langchain.schema import HumanMessage
from contextlib import asynccontextmanager

async def data_stream(content):
    callback = AsyncIteratorCallbackHandler()
    llm = app.state.model

    task = asyncio.create_task(
        llm.agenerate(messages=[[HumanMessage(content=content)]], callbacks=[callback])
    )

    try:
        async for token in callback.aiter():
            yield token
    except Exception as e:
        print(f"Caught exception: {e}")
    finally:
        await callback.done.wait()  # Ensure the task completes
        callback.done.set()
        await task  # Make sure the LLM process finishes

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan function for FastAPI: initializes and warms up the model.
    """
    print("Starting FastAPI application...")

    # Initialize LLM model
    model = ChatOllama(
        model="llama3.2:1b",
        temperature=0,
        streaming=True,
        verbose=True,
        base_url="http://ollama:11434",
    )

    model.invoke("Hello, I am a language model. How can I help you?")

    print("Warm-up completed successfully!")
    
    app.state.model = model

    yield  # FastAPI runs here

    print("Shutting down FastAPI application...")
    app.state.model = None  # Cleanup resources if necessary
  
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
    generator = data_stream(req.content)
    return StreamingResponse(generator, media_type="text/event-stream"
                        , headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})
