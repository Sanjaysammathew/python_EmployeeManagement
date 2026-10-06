from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello():
    print("Hello")
    return {"message": "Hello"}