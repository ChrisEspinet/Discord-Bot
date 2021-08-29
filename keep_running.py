from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
  return "Hey, I'm currently running!"

def run():
  app.run(host = '0.0.0.0',port = 8000)

def keep_running():
  thread = Thread(target = run)
  thread.start()