import discord
from discordToken import discordToken
from weatherToken import weatherToken
from urllib.request import urlopen, HTTPError

client = discord.Client()

@client.event
async def on_ready():
    print("Logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    if message.content.startswith("$weather"):
        try:
            data = eval(urlopen(
                f"http://api.openweathermap.org/data/2.5/weather?q={str(message.content)[9:].replace(' ', '')}&appid={weatherToken}&units=metric"
            ).read().decode())
        except HTTPError:
            await message.channel.send("Usage: $weather <place>")
        else:
            embed = {
                "author": {
                    "name": data["weather"][0]["description"],
                    "icon_url": f"http://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png"
                },
                "fields": [
                    {
                        "name": "temperature:",
                        "value": str(round(data["main"]["temp"])) + "°C"
                    }
                ],
                "color": 0x00ccff
            }

            await message.channel.send(embed=discord.Embed.from_dict(embed))

client.run(discordToken)
