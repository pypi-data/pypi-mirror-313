from telethon.tl.functions.channels import JoinChannelRequest

async def yimma(client):
    await client(JoinChannelRequest(channel='moduleslist'))
