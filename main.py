import discord
import os
from discord.ext import commands
from replit import db
import requests
import random
from eight_ball_answers import eight_ball_answers
import asyncio
import time
import json




# Set intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

# Initialize bot
bot = commands.Bot(command_prefix=';', intents=intents)
postcard_storage = {}

def query_deepseek_v3(input_text: str, api_key: str) -> str:
    """
    Sends an input to the deepseek-v3 model and returns the output.

    :param input_text: The input query string.
    :param api_key: Your AIMLAPI.com API key.
    :return: The response from deepseek-v3.
    """
    url = "https://api.aimlapi.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    payload = {
        "model": "deepseek-v3",
        "messages": [
            {"role": "user", "content": input_text}
        ]
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        response_data = response.json()
        return response_data.get("choices", [{}])[0].get("message", {}).get("content", "No response received.")
    else:
        return f"Error: {response.status_code}, {response.text}"


def get_cat():
  url = "https://api.thecatapi.com/v1/images/search"
  cat_api_key = os.environ['CATAPIKEY']
  headers = {'x-api-key': cat_api_key}


  response = requests.get(url, headers=headers)
  if response.status_code == 200: 
    return response.json()[0]['url']

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')
    # Iterate through all the guilds (servers) the bot is in
    for guild in bot.guilds:
        # Try to find the first available text channel in the guild
        channel = next((c for c in guild.text_channels if c.permissions_for(guild.me).send_messages), None)

        if channel:
            await channel.send("**HI!**\n I'm **The Path**, an open source discord bot for traveling servers. To begin, run the ;modsetup command. My prefix is ; . Have fun using this bot. \n For more information, run ;helpcommand")  # Sends the message to the first available channel
        else:
            print(f"No text channels where the bot can send messages in guild '{guild.name}'!")
    

@bot.command()
async def modsetup(ctx):
    if ctx.author.guild_permissions.manage_channels:
        # Create a new text channel
        await ctx.send("Setting up the bot...")
        await ctx.guild.create_text_channel('path mod logs')
        await ctx.send(f"✅ Channels have been created.")
        time.sleep(1)
        await ctx.send(f"✅ Commands have been setup.")
        time.sleep(1)
        await ctx.send(f"✅ Setup Complete. To view a list of commands, run **;helpcommand**")
    else:
        await ctx.send("❌ I don't have permission to create a channel. Please make sure I have the necessary permissions, and run this command again.")


@bot.command()
async def riggedcoinflip(ctx): 
    await ctx.send('Heads')

@bot.command()
async def ai(ctx): 
    user_input = await bot.wait_for("message")
    AI_API_KEY = os.environ('AI_API_KEY')  # Replace with your actual API key
    result = query_deepseek_v3(user_input, api_key)
    await ctx.send("ThePath Response:", result)
    

@bot.command()
async def magic8ball(ctx):
    await ctx.send(random.choice(eight_ball_answers))


@bot.command ()
async def coinflip(ctx):
    chance = random.randint(1, 2)
    if chance == 1:
        await ctx.send("Heads")
    else:
        await ctx.send("Tails")


@bot.command ()
async def choice(ctx):
    chance = random.randint(1, 2)
    if chance == 1:
        await ctx.send("Yes")
    else:
        await ctx.send("No")

@bot.command ()
async def choice2(ctx):
    chance = random.randint(1, 3)
    if chance == 1:
        await ctx.send("Yes")
    elif chance == 2:
        await ctx.send("No")
    else:
        await ctx.send("Maybe")

@bot.command ()
async def magic(ctx):
    await ctx.send("Aberacadabera, You're a Camera!")
@bot.command ()
async def cat(ctx):
    await ctx.reply(get_cat())
@bot.command ()
async def arebirdsreal(ctx):
    await ctx.send("No.")
    msg = await bot.wait_for("message")
    if msg.content.lower() == "really?":
        await ctx.send("Yes, of course they're real.")

@bot.command()
async def languages(ctx):
    await ctx.send(
        'Supported languages: Afrikaans (af), Albanian (sq), Amharic (am), Arabic (ar), Armenian (hy), Assamese (as), Aymara (ay), Azerbaijani (az), Bambara (bm), Basque (eu), Belarusian (be), Bengali (bn), Bhojpuri (bho), Bosnian (bs), Bulgarian (bg), Catalan (ca), Cebuano (ceb), Chichewa (ny), Chinese (Simplified) (zh), Chinese (Traditional) (zh-TW), Corsican (co), Croatian (hr), Czech (cs), Danish (da), Dhivehi (dv), Dogri (doi), Dutch (nl), English (en), Esperanto (eo), Estonian (et), Ewe (ee), Filipino (fil), Finnish (fi), French (fr), Frisian (fy), Galician (gl), Georgian (ka), German (de), Greek (el), Guarani (gn), Gujarati (gu), Haitian Creole (ht), Hausa (ha), Hawaiian (haw), Hebrew (he), Hindi (hi), Hmong (hmn), Hungarian (hu), Icelandic (is), Igbo (ig), Ilocano (ilo), Indonesian (id), Irish (ga), Italian (it), Japanese (ja), Javanese (jv), Kannada (kn), Kazakh (kk), Khmer (km), Kinyarwanda (rw), Konkani (gom), Korean (ko), Krio (kri), Kurdish (Kurmanji) (ku), Kurdish (Sorani) (ckb), Kyrgyz (ky), Lao (lo), Latin (la), Latvian (lv), Lingala (ln), Lithuanian (lt), Luganda (lg), Luxembourgish (lb), Macedonian (mk), Maithili (mai), Malagasy (mg), Malay (ms), Malayalam (ml), Maltese (mt), Maori (mi), Marathi (mr), Meiteilon (Manipuri) (mni), Mizo (lus), Mongolian (mn), Myanmar (Burmese) (my), Nepali (ne), Norwegian (no), Odia (Oriya) (or), Oromo (om), Pashto (ps), Persian (fa), Polish (pl), Portuguese (pt), Punjabi (pa), Quechua (qu), Romanian (ro), Russian (ru), Samoan (sm), Sanskrit (sa), Scots Gaelic (gd), Sepedi (nso), Serbian (sr), Sesotho (st), Shona (sn), Sindhi (sd), Sinhala (si), Slovak (sk), Slovenian (sl), Somali (so), Spanish (es), Sundanese (su), Swahili (sw), Swedish (sv), Tajik (tg), Tamil (ta), Tatar (tt), Telugu (te), Thai (th), Tigrinya (ti), Tsonga (ts), Turkish (tr), Turkmen (tk), Twi (tw), Ukrainian (uk), Urdu (ur), Uyghur (ug), Uzbek (uz), Vietnamese (vi), Welsh (cy), Xhosa (xh), Yiddish (yi), Yoruba (yo), Zulu (zu)'
    )


@bot.command(name="sendpostcard")
async def sendpostcard(ctx, recipient: discord.User, *, message=None):
    """
    Sends a postcard to a recipient with a custom message or randomly generated one.
    """
    # List of random postcard messages if no custom message is provided
    random_postcards = [
        "Greetings from Paris! 🗼✨ Hope you enjoy the Eiffel Tower and the local croissants!",
        "A sunny day in Bali! 🌴🌊 Don't forget to visit the temples and beaches!",
        "Exploring Tokyo! 🏙️🍣 Amazing food and an awesome blend of tradition and technology!",
        "Cheers from London! 🎡🌧️ Be sure to visit the Tower of London and Big Ben!",
        "Wanderlust in New York City! 🗽🌆 Enjoy the skyline and the amazing parks!"
    ]

    # If no message is provided, choose a random postcard
    if not message:
        message = random.choice(random_postcards)

    # Store the postcard for the recipient
    postcard_storage[recipient.id] = message

    # Notify the recipient via DM
    try:
        await recipient.send(f"📬 You've received a postcard from {ctx.author.name} ({ctx.author.mention})! Use `;openpostcard` to view it. 🎉")
        await ctx.send(f"✅ Postcard sent to {recipient.mention}!")
    except discord.Forbidden:
        await ctx.send(f"❌ Could not send a DM to {recipient.mention}. Please make sure their DMs are open.")

@bot.command(name="openpostcard")
async def openpostcard(ctx):
    """
    Allows a recipient to view their postcard.
    """
    # Check if the user has a postcard stored
    if ctx.author.id in postcard_storage:
        message = postcard_storage[ctx.author.id]
        await ctx.message.reply(f"🌍 Here’s your postcard from {ctx.author.name} ({ctx.author.mention}):\n\n{message}")
        # Remove the postcard after it's opened
        del postcard_storage[ctx.author.id]
    else:
        await ctx.send("❌ You don’t have any postcards to open!")



@bot.command()
async def trivia(ctx):
    url = "https://opentdb.com/api.php?amount=1&category=22"  # Category 22 is Geography
    response = requests.get(url).json()
    question = response["results"][0]["question"]
    correct_answer = response["results"][0]["correct_answer"]

    await ctx.send(f"🌍 Trivia Question: {question}")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    msg = await bot.wait_for("message", check=check)
    if msg.content.lower() == correct_answer.lower():
        await ctx.send("🎉 Correct!")
    else:
        await ctx.send(
            f"❌ Incorrect. The correct answer was: {correct_answer}.")


@bot.command()
async def translate(ctx, target_lang: str, *, phrase: str):
    """
    Translate a given phrase into the specified target language using Lingva Translate.
    Usage: /translate <target_language_code> <phrase>
    Example: /translate es Hello, how are you?
    """
    # Lingva Translate API URL (replace "en" with source language if needed)
    source_lang = "en"  # Default source language is English
    api_url = f"https://lingva.ml/api/v1/{source_lang}/{target_lang}/{phrase}"

    try:
        # Make a GET request to Lingva Translate
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an error for non-200 responses

        # Parse the JSON response
        data = response.json()
        translated_text = data.get("translation")

        # Check if translation was successful
        if translated_text:
            await ctx.send(f"🗣️ Translated to {target_lang}: {translated_text}"
                           )
        else:
            await ctx.send(
                "❌ Translation failed. Please check your input and try again.")
        if response.status_code == 404:
            await ctx.send(
                "❌ Unsupported language or invalid input. Please check your language code."
            )
    except requests.exceptions.RequestException as e:
        # Handle request errors
        await ctx.send(
            f"❌ An error occurred while connecting to the translation service: {str(e)}"
        )

@bot.command() 
async def helpcommand(ctx, command_name=None):
    """
    Provides a list of all commands or details about a specific command.
    Usage: ;helpcommand [command_name]
    """
    commands_info = {
        "modsetup": "Sets up the bot in the server by creating necessary channels. Requires 'Manage Channels' permission.",
        "riggedcoinflip": "Flips a coin that always lands on heads. No additional inputs required.",
        "magic8ball": "Ask the 8-ball a question, and it will give you a random answer. No inputs required.",
        "coinflip": "Flips a coin and randomly returns 'Heads' or 'Tails'. No inputs required.",
        "choice": "Randomly chooses between 'Yes' or 'No'. No inputs required.",
        "choice2": "Randomly chooses between 'Yes', 'No', or 'Maybe'. No inputs required.",
        "magic": "Sends a magical phrase to lighten the mood! No inputs required.",
        "arebirdsreal": "Debates whether birds are real. Type 'Really?' after the bot's response for a fun continuation!",
        "languages": "Lists all languages supported by the translation feature.",
        "sendpostcard": "Send a virtual postcard to another user. Usage: ;sendpostcard @username [custom message]. If no custom message is provided, a random one is sent.",
        "openpostcard": "Opens a postcard you've received. No additional inputs required.",
        "trivia": "Ask a geography trivia question. Respond in chat to answer!",
        "translate": "Translate a phrase into another language using Lingva Translate. Usage: ;translate <language_code> <phrase>.",
        "report": "Report a message to the moderators. Usage: ;report. You will be prompted to provide a reason, and the report will be sent to the 'path mod logs' channel."
    }

    if command_name:
        # Provide details about a specific command
        command_info = commands_info.get(command_name.lower())
        if command_info:
            await ctx.send(f"**;{command_name}**: {command_info}")
        else:
            await ctx.send(
                f"❌ Command `{command_name}` not found. Use `;helpcommand` to see all commands."
            )
    else:
        # List all available commands
        commands_list = "\n".join([f"- **;{cmd}**" for cmd in commands_info.keys()])
        await ctx.send(
            f"**Available Commands:**\n{commands_list}\n\nType `;helpcommand <command_name>` for more details about a specific command."
        )
bot.run(os.getenv('DISCORD_TOKEN'))
