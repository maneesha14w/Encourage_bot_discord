import discord
import os
import requests
import json
import random
from replit import db


client = discord.Client()

sad_words = ['sad', 'depressed', 'unhappy', 'angry', 'miserable', 'depressing']

starter_encouragements = ["Cheer up!", "Hang in there.",
 "You are a great person!" ]

def getQuote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return (quote)
  

def updateEncouragements(enouraging_msg):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(enouraging_msg)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [enouraging_msg]


def del_Encouragements(index):
  encouragements = db["enouragements"]
  if len(encouragements) > index:
    del encouragements[index]
  db["encouragements"] = encouragements
    


@client.event
async def on_ready():
  print('We have logged in as {0.user} '.format(client))

@client.event
async def on_message(message):
  if message.author == client.user: 
    return

  msg = message.content
  
  if msg.startswith('$hello'):
    await message.channel.send('Hello!')
  
  if msg.startswith('$inspire'):
    quote = getQuote()
    await message.channel.send(quote)

  options = starter_encouragements
  if "encouragements" in db.keys():
    options = options + db["encouragements"]

  if any(word in msg for word in sad_words):
    await message.channel.send(random.choice(options))
    

client.run(os.getenv('token'))


