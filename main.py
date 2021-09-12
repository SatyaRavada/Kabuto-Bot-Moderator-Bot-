import discord
import os
from googleapiclient import discovery
from keep_alive import keep_alive
from discord.ext import commands

client=commands.Bot(command_prefix ='.')
tlimit={client:90}

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
@commands.has_permissions(manage_messages=True) 
async def on_message(message):
  if message.author==client.user:
    return
  msg=message.content
  try:
    value=perspective_api(msg)
  except:
    await client.process_commands(message)
  if value*100>tlimit[client]:
    await message.delete()
  await client.process_commands(message)

  if msg.startswith(("$who made you","$who built you")):
    await message.channel.send("Author : "+os.environ['author'])
    await client.process_commands(message)
  
  if msg.startswith("$set limit"):
    if int(msg.split("$set limit",1)[1]) in range(1,101):
      tlimit[client]=int(msg.split("$set limit",1)[1])
      await message.channel.send("limit set to {}".format(tlimit[client]))
      await client.process_commands(message)
      
    else:
      await message.channel.send("Sorry it's not an accepatable limit value.Try again between 1-100!")
      await client.process_commands(message)
      
  
  if msg.startswith("$get limit"):
    await message.channel.send("current toxic limit is {}".format(tlimit[client]))
    await client.process_commands(message)
  
@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx,amount=2):
  await ctx.channel.purge(limit=amount) 

@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx,member : discord.Member, *,reason=None):
  await member.kick(reason=reason)
  await ctx.send(f'Kicked {member.mention}')

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx,member : discord.Member, *,reason=None):
  await member.ban(reason=reason)
  await ctx.send(f'Banned {member.mention}')

@client.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx,*,member):
  banned_users= await ctx.guild.bans()
  member_name,member_discriminator=member.split('#')
  for banned_entry in banned_users:
    user=banned_entry.user
    if(user.name,user.discriminator)==(member_name,member_discriminator):
      await ctx.guild.unban(user)
      await ctx.send(member_name+" has been unbanned.")
      return
  await ctx.send(member+" was not found")
    
keep_alive()
client.run(os.environ['Token'])




