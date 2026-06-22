from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
import chromadb
from chromadb.utils import embedding_functions
from pathlib import Path
import os

BASE_DIR = Path(__file__).parent
CHROMA_PATH = str(BASE_DIR / "chroma_db")


def answer_question(user_query, collection, top_k=3): 
    
    results = collection.query(
        query_texts=[user_query],
        n_results=top_k
    ) 
    chunks = results['documents'][0]
    sources = results['metadatas'][0]
    distances = results['distances'][0]
    
    context_parts = []
    for chunk, meta, dist in zip(chunks, sources, distances):
      
        context_parts.append(
            f"[ДЖЕРЕЛО: {meta['source']}, СТОРІНКА: {meta['page']}, РЕЛЕВАНТНІСТЬ: {1-dist:.2f}]\n{chunk}"
        )
    
    context = "\n\n---\n\n".join(context_parts)
    
    prompt = f""" 
            You are an assistant who responds ONLY based on the context provided.
        RULES:
        1. Answer ONLY based on the context below.
        2. If the information is NOT in the context, honestly say “I don't know” or “This information is not included in the provided documents.”
        3. DO NOT make up information that is not in the context.
        4. If you answer, cite your source.

        CONTEXT (taken from documents):
        {context}

        USER QUESTION:
        {user_query}

        ANSWER (based on the context):
    """
         
    # query for llama3.2 model
    try:
        import ollama 
        response = ollama.chat(
            model = 'llama3.2',
            
            messages=[
                {"role": "system", "content": "You are an assistant. Respond only based on the context provided. If you don't know, say 'I don't know.'"},
                {"role": "user", "content": prompt}
            ],
            options = {
                'temperature': 0.3, # To more accuracy answer
                'num_predict': 500  # To more better think, but longer
            }   
        )
        answer = response['message']['content']
    except:
        print(f"Ollama недоступний")
        answer = "[ПОТРІБНА LLM МОДЕЛЬ]"
     
    return {
        'answer': answer,
        'sources': sources,
        'chunks': chunks,
        'context': context,
        'prompt': prompt
    }
 

@asynccontextmanager
async def lifespan(app: FastAPI):

    print('Start work....')
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    app.state.collection = client.get_collection(
        name="my_docs",
        embedding_function=embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
    )
 
    print("Server loaded successfully")
    
    yield
    print("Stop loading model...") 
    
    
       
app = FastAPI(
    title="llama model API",
    description="Generate answer",
    version="1.0.0", 
    lifespan= lifespan,
)

@app.get('/')
def start_func():
    return {"Hello": "World"}


@app.post("/generate_answer")
async def generate_answer(user_question: str, request: Request):
    """
    generate answer for base on download docs
    """

    collection = request.app.state.collection
    result = answer_question(user_question, collection, top_k = 3)

    print(f"Questions: {user_question}")
 
    print("\nAnswer: ")
    print(result['answer'])
    
    print("\n" + "="*70)
    print("Source: ")
    for i, source in enumerate(result['sources'], 1):
        print(f"{i}. {source['source']} (стор. {source['page']})")

    
    return {
        "Questions": user_question,
        "answer": result['answer'],
        "sources":[
            {"file": s['source'], "page": s['page']}
        for s in result['sources']
        ]
    }
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host = "127.0.0.1", port=8000)
