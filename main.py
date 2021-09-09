import discord
import os
from googleapiclient import discovery
from keep_alive import keep_alive
from replit import db
client=discord.Client()
limit={client:90}
if "responding" not in db.keys():
  db["responding"]=True
def perspective_api(msg):
  client = discovery.build(
  "commentanalyzer",
  "v1alpha1",
  developerKey=os.environ['api_key1'],
  discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
  static_discovery=False,
  )

  analyze_request = {
  'comment': { 'text': msg },
  'requestedAttributes': {'TOXICITY': {}}
  }

  response = client.comments().analyze(body=analyze_request).execute()
  value=response['attributeScores']['TOXICITY']["summaryScore"]["value"]
  return value
@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))
@client.event
async def on_message(message):
  
  if message.author==client.user:
    return
  msg=message.content

  if msg.startswith(("$who made you","$who built you")):
    await message.channel.send("Author : "+os.environ['author'])
  if msg.startswith("$set limit"):
    if int(msg.split("$set limit",1)[1]) in range(1,101):
      limit[client]=int(msg.split("$set limit",1)[1])
      await message.channel.send("limit set to {}".format(limit[client]))
    else:
      await message.channel.send("Sorry it's not an accepatable limit value.Try again between 1-100!")
  if msg.startswith("$get limit"):
    await message.channel.send("current toxic limit is {}".format(limit[client]))

  value=perspective_api(msg)
  if db["responding"]:
    if value*100>limit[client]:
      await message.channel.send("the above message has toxicity value = {}%".format(value*100))
  if msg.startswith("$respondingk"):
    value=msg.split("$respondingk ",1)[1]
    if value.lower()=='true':
      db["responding"]=True
      await message.channel.send("Responding is on.")
    else:
      db["responding"]=False
      await message.channel.send("Responding is off.")

    
keep_alive()
client.run(os.environ['Token'])


