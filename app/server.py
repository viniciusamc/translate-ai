import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from langchain_openai import ChatOpenAI

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="A simple api server using Langchain's Runnable interfaces",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

class Message(BaseModel):
    message: str

@app.post("/translate")
async def root(item: Message):
    llm = ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"))
    result = llm.invoke("Translate the following sentence to Portuguese:" + item.message)

    response_message = {"message": item.message, "translated_message": result}
    json_compatible_item_data = jsonable_encoder(response_message)
    return JSONResponse(content=json_compatible_item_data)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
