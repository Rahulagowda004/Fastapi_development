from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "hello hope you are doing great!"}

@app.get("/trail")
async def read_trail():
    return {"message": "This is the trail endpoint"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)