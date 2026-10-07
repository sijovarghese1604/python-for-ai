from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Hello from FastAPI"}


@app.get("/greet/{name}")
def greet(name: str, excited: bool = False):
    text = f"Hello, {name}"
    return {"greeting": text + ("!!!" if excited else ".")}