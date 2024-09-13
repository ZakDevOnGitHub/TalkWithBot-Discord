#Discord
import discord, random
from discord import app_commands
import tracemalloc

# Intents, Guild, Client, Tree
intents = discord.Intents.default()
intents.message_content = True
guild_id = "YOUR_SERVER_ID" # Replace this ID with the ServerID you're going to control the bot in
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    tracemalloc.start()
    await tree.sync(guild=discord.Object(id=guild_id))
    print(f"{client.user} is ready to go!")

@client.event
async def on_message(Message: discord.Message):
    if not Message.author.bot and Message.channel == client.get_channel(ControlChannelID):
        await SessionChannel.send(Message.content)

@tree.command(name="start_session", description="Starts a session with the Discord Bot", guild=discord.Object(id=guild_id))
async def Start_Session(Interaction: discord.Interaction, channel_id: str):
    global Session
    global SessionChannel
    global ControlChannelID
    ControlChannelID = None
    SessionChannel = None
    Session = False
    if Session == False:
        if client.get_channel(int(channel_id)):
            Channel = client.get_channel(int(channel_id))
            if not Channel.permissions_for(client.get_guild(Channel.guild.id).me).send_messages:
                await Interaction.response.send_message("❌ **I'm sorry, but I have insufficent permissions to send messages in this channel! Please choose a different channel for me to use!**", ephemeral=True)
            else:
                await Interaction.response.send_message(f"✅ **Your session has started for `{Channel.name}`! As you send messages here, the bot will send the same message in that channel! if you wish to end your session, please run the `/end_session` command!**", ephemeral=True)
                Session = True
                SessionChannel = Channel
                ControlChannelID = Interaction.channel.id
        else:
            await Interaction.response.send_message("❌ **I'm sorry, but I could NOT find the channel with that ID! Please make sure this is a Channel ID and NOT a Server ID! If this is a valid Channel ID, please make sure I am in that server with the channel of that ID!**", ephemeral=True)
    else:
        await Interaction.response.send_message(f"❌ **{Interaction.user} A session is already active! Please end this session by running `/end_session` if you wish to start a new one!**", ephemeral=True)


@tree.command(name="end_session", description="Ends a session with the Discord Bot!", guild=discord.Object(id=guild_id))
async def end_session(Interaction: discord.Interaction):
    global SessionChannel
    if SessionChannel != None:
        await Interaction.response.send_message(f"✅ **Your session has ended for `{SessionChannel.name}`! the bot will no longer send messages you send here! If you wish to start a new session, please run the `/start_session` command!**", ephemeral=True)
        SessionChannel = None
    else:
        await Interaction.response.send_message(f"❌ **{Interaction.user} no session is currently acitve Please run `/start_session` if you wish to start a new one!**", ephemeral=True)

@tree.command(name="reply", description="Reply to a message in the channel the bot is sending messages in!", guild=discord.Object(id=guild_id))
async def reply(Interaction: discord.Interaction, message_id: str, message: str):
    if Session:
        try:
            await SessionChannel.get_partial_message(int(message_id)).reply(content=message)
            await Interaction.response.send_message("✅ **Message replied!**")
        except:
            await Interaction.response.send_message("❌ **I could NOT find the message with that ID in that channel! Please make sure you have entered a message ID**")
    else:
        Interaction.response.send_message("❌ **No session is currently active! Please run `/start_session` if you wish to start a new one!**")
client.run('YOUR_DISCORD_BOT_TOKEN')