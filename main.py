import os
import discord
import requests
import json
import random
import pandas_datareader as web
from replit import db
from keep_running import keep_running

client = discord.Client()

greetings = ["What's up JARVIS", "whats up jarvis", "what are you up to?", "what are you doing jarvis", "What are you doing JARVIS?"]

greetings_response = [
  "Just doing robot things",
  "Currently mining crypto",
  "I'm just downloading movies",
  "Trying to get superpowers by letting a radioactive spider bite me",
  "Currently looking through your search history :)",
  "I'm creating an army of Discord bots as we speak",
  "Currently listening to lofi hip hop radio - beats to relax/study to"
]

def get_joke():
  response = requests.get("https://official-joke-api.appspot.com/random_joke")
  json_data = json.loads(response.text)
  joke = json_data['setup'] + "\n\n" + json_data['punchline']
  return(joke)

def get_stock_price(ticker):
  stockData = web.DataReader(ticker, "yahoo")
  return stockData['Close'].iloc[-1]


#Creates a new response to any of the greetings prompts
def update_activity(activity_response):
  if "activity" in db.keys():
    activity = db["activity"]
    activity.append(activity_response)
    db["activity"] = activity
  else:
    db["activity"] = [activity_response]

#Deletes a response
def delete_activity(index):
  activity = db["activity"]
  if len(activity) > index:
    del activity[index]
    db["activity"] = activity

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  options = greetings_response

  #Combines usered-entered responses with pre-made responses
  if "activity" in db.keys():
    options.extend(db["activity"])
  #Responds to any of the greetings prompts
  if any(word in message.content for word in greetings):
    await message.channel.send(random.choice(options))

  if message.author == client.user:
    return
  if message.content.startswith('Hey JARVIS'):
    await message.channel.send('Hello!')

  #Reponds with a jandom joke
  if 'me a joke' in message.content:
    joke = get_joke()
    await message.channel.send(joke)

  #Responds with stock price
  if message.content.startswith("?stockprice"):
    if len(message.content.split(" ")) == 2:
      ticker = message.content.split(" ")[1]
      stockPrice = get_stock_price(ticker)
      formattedStockPrice = "{:.2f}".format(stockPrice)
      await message.channel.send(f"Stock price of {ticker} is {formattedStockPrice} USD.")

  #Adds new activity response to database  
  if message.content.startswith("!new"):
    activity_message = message.content.split("!new ", 1)[1]
    update_activity(activity_message)
    await message.channel.send("New response added, thanks!")

  #Deletes activity response from database
  if message.content.startswith("!del"):
    activity = []
    if "activity" in db.keys():
      index = int(message.content.split("!del",1)[1])
      delete_activity(index)
      activity = db["activity"]
    await message.channel.send(activity)

  #Shows user a list of activity responses to the greetings prompts  
  if message.content.startswith("?list"):
    activity = []
    if "activity" in db.keys():
      activity = db["activity"]
    await message.channel.send(activity)

keep_running()

client.run(os.getenv('TOKEN'))