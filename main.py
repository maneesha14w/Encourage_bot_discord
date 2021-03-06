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

if "responding" not in db.keys():
  db["responding"] = True

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
  encouragements = db["encouragements"]
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

  if db["responding"]:
    options = starter_encouragements
    if "encouragements" in db.keys():
      options = options + db["encouragements"]

    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(options))
    
  if msg.startswith("$new"):
    encouraging_message = msg.split("$new ", 1)[1]
    updateEncouragements(encouraging_message)
    await message.channel.send("New Message added!")

  if msg.startswith("$del"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split("$del",1)[1])
      del_Encouragements(index)
      encouragements = db['encouragements']
      await message.channel.send(encouragements)

  if msg.startswith("$list"):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  if msg.startswith("$responding"):
    value = msg.split("$responding ", 1)[1]

    if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("responding is on.")
    elif value.lower() == "false":
      db["responding"] = False
      await message.channel.send("responding is off.")
    else:
      await message.channel.send("Please say true or false")


client.run(os.getenv('token'))


