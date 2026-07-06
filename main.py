from fastapi import FastAPI
from database import conn

app = FastAPI()

@app.get('/')
def greetings():
    return "Welcome to leetcode tracker!!!"
