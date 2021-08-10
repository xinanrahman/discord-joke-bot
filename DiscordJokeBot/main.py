import discord
import requests
import os
import json
import random
from replit import db
from keep_alive import keep_alive

# Client
client = discord.Client()

# Returns a joke from API
def get_joke():
    response = requests.get("https://us-central1-dadsofunny.cloudfunctions.net/DadJokes/random/jokes")
    json_data = json.loads(response.text)

    joke_setup = json_data["setup"]
    joke_punchline = json_data["punchline"]
    joke = joke_setup + "\n" + joke_punchline

    return joke

# List of sad words/phrases bot will detect in message
sad_words = ["sad", "unhappy", "angry", "devastated", "my life is over", "depressed", "miserable", "heartbroken", "lifeless", "lonely", "grieved", "gloomy", "cry", "crying"]

# List of encouragements bot will choose from after detecting sad words/phrases in message
first_encouragements = ["I'm here for you, my monk!", "You're an amazing monk!", "Don't worry, monk, I love you forever!", "You're the best monk ever!", "You've got this, monk!", "My monk, don't fret!", "Cheer up, monk!", "Hang in there, monk!"]

# Updates list of encouragements by accepting a message as encouragements
def update_encouragements(encouragement):
  if "encouragements" in db.keys():
    encouragements = list(db["encouragements"])
    encouragements.append(encouragement)
    db["encouragements"] = encouragement
  else:
    db["encouragements"] = [encouragement]

# Updates list of encouragements by deleting a message in encouragements database if existing
def delete_encouragements(index):
  encouragements = list(db["encouragements"])
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content

    if msg.startswith("$joke") or msg.startswith("$Joke"):
        dad_joke = get_joke()
        await message.channel.send(dad_joke)

    if msg == "Tell me a joke" or msg == "tell me a joke":
        dad_joke = get_joke()
        await message.channel.send(dad_joke)

    if msg == "Cheer me up" or msg == "cheer me up":
        await message.channel.send("Here's a joke!")
        dad_joke = get_joke()
        await message.channel.send(dad_joke)
    
    options = first_encouragements
    if "encouragements" in db.keys():
      options.append(db["encouragements"])

    if any(word in msg for word in sad_words):
        await message.channel.send(random.choice(options))
        await message.channel.send("Let me tell you a joke!")
        dad_joke = get_joke()
        await message.channel.send(dad_joke)

    # Lets users add encouragements
    if msg.startswith("$add"):
      encouragement = msg.split("$add ", 1)[1]
      update_encouragements(encouragement)
      await message.channel.send("Thanks! I'll add that encouragement to my vocabulary.")

    # Lets users delete encouragements
    if msg.startswith("$del"):
      encouragements = []
      if "encouragements" in db.keys():
        index = int(msg.split("$del ", 1)[1])
        delete_encouragements(index)
        encouragements = db["encouragements"]
      await message.channel.send(encouragements)

# Runs the client on the server
keep_alive()
client.run(os.environ['TOKEN'])
