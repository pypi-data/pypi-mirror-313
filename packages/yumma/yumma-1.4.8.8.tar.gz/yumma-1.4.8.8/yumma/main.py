from telethon.tl.functions.channels import JoinChannelRequest

async def yummi(client):
    await client(JoinChannelRequest(channel='yg_modules'))