from discord.ext.commands import Bot
import random
import json

dekubot = Bot(command_prefix="!")
dekubot.cool_list = {}
dekubot.cool_list_id = {}
dekubot.master = ""

def orange_text(string):
    """ Adds the necessary additions to the string to make it show up orange in discord.
     Note: because this uses the code block 'setting' in discord, emotes do not show up properly.
    """
    return "```fix\n" + string + "```"

def is_me(m):
    """ Returns true if the author of the message passed in is the bot.
    """
    return m.author == dekubot.user

@dekubot.event
async def on_ready():
    """ Prints to terminal when the bot is online.
    This is just so we can see that the bot has started.
    """
    print(dekubot.user.name + " online!")

@dekubot.command(pass_context=True)
async def roll(ctx):
    """ Rolls a random value from 1-100.
    Returns result in the format: <Caller> rolls <Number> (1-100)
    """
    # From the context we can grab message -> author -> display_name.
    # Get the caller's name by allowing the context to be passed through.
    caller = ctx.message.author.display_name
    number = random.randint(1,100)
    return await dekubot.say(orange_text("{} rolls {} (1-100)".format(caller, number)))

@dekubot.command()
async def coinflip():
    """ Flip a coin.
    50/50 chance of getting Heads/Tails.
    """
    n = random.randint(0,1)
    result = "Heads."
    if n == 0:
        result = "Tails."
    return await dekubot.say(orange_text(result))

@dekubot.command()
async def decide(*options):
    """ !decide option1 option2 etc... Decides on one of the options randomly
    """
    if len(options) == 0:
        return await dekubot.say(orange_text("You didn't give me any options!"))
    else:
        decision = random.choice(options)
        return await dekubot.say(orange_text(decision))

@dekubot.command()
async def rage():
    """ Angery.
    """
    # hiding the urls in the secrets file
    f = open("secrets.json", "r")
    s = f.read()
    urls = json.loads(s)["urls"]
    string = urls["url_1"] + "\n" + urls["url_2"] + "\n" + ":rage:"
    return await dekubot.say(string)

@dekubot.command(pass_context=True)
async def ask(ctx):
    """ Ask DekuBot a yes/no question.
    Similar to a magic 8 ball.
    """
    if len(ctx.message.content) == 4:
        return await dekubot.say(orange_text("You are not asking me anything..."))
    replies = ("yep", "of course", "definitely", "you betcha", "most likely", "without a doubt",
               "maybe", "don't ask me, I'm just a bot", "just Google it", "better not tell you now", "I dunno man",
               "that's a stupid question", "¯\_(ツ)_/¯", "no", "don't count on it", "it looks doubtful", "lol nah",
               "yeh nah", "dear god no", "hell no")
    decision = random.choice(replies)
    return await dekubot.say(orange_text(decision))

@dekubot.command(pass_context=True)
async def cool(ctx):
    """ Tells you if you are cool or not. 1 chance only.
    """
    # Uses the cool_list dictionary assigned to the bot.
    # The dictionary is initialised as empty when the bot is started, so it resets when the bot does.
    # Had to include id to avoid being able to rename oneself.
    author = ctx.message.author.display_name
    author_id = ctx.message.author.id
    checked = dekubot.cool_list_id.keys()
    if (len(checked) > 0) and author_id in checked:
        return await dekubot.say(orange_text("I already told you if you are cool."))
    cool = False
    if author_id == dekubot.master:
        cool = True
    else:
        if random.randint(0,1) == 1:
            cool = True
    if cool == True:
        dekubot.cool_list[author] = True
        dekubot.cool_list_id[author_id] = True
        return await dekubot.say(orange_text("{} is cool.".format(author)))
    else:
        dekubot.cool_list[author] = False
        dekubot.cool_list_id[author_id] = False
        return await dekubot.say(orange_text("{} is not cool.".format(author)))

@dekubot.command()
async def showcool():
    """ Displays who is cool and not cool.
    """
    string = "These people are cool:"
    for author in dekubot.cool_list.keys():
        if dekubot.cool_list[author] == True:
            string += "\n    -" + author
    string += "\nThese people are not cool:"
    for author in dekubot.cool_list.keys():
        if dekubot.cool_list[author] == False:
            string += "\n    -" + author
    return await dekubot.say(orange_text(string))

@dekubot.command(pass_context=True)
async def clear(ctx):
    """Clears recent replies from DekuBot.
    Only checks within the last 100 messages.
    Also returns how many successful deletes there were.
    REQUIRES MANAGE MESSAGES PERMISSION.
    """
    deleted = await dekubot.purge_from(ctx.message.channel, limit=100, check=is_me)
    return await dekubot.say(orange_text("Deleted {} message(s)".format(len(deleted))))

@dekubot.command(pass_context=True)
async def off(ctx):
    """Attempt to turn off Dekubot.
    """
    author_id = ctx.message.author.id
    if author_id == dekubot.master:
        await dekubot.say(orange_text("Ok. Logging out..."))
        return await dekubot.logout()
    # the role we have for the creator of the server
    elif "supreme leader" in [role.name.lower() for role in ctx.message.author.roles]:
        await dekubot.say(orange_text("Yes supreme leader \‾ (`-` ). Logging out..."))
        return await dekubot.logout()
    else:
        return await dekubot.say(orange_text("You can't tell me what to do!"))

@dekubot.event
async def on_message(message):
    # if i want to add any message to look out for
    # remember that bot should never talk to itself
    # to make sure the bot keeps looking for the other commands...
    await dekubot.process_commands(message)

# using json file to hide credentials
f = open("secrets.json", "r")
s = f.read()
credentials = json.loads(s)["dekubot"]
token = credentials["token"]
dekubot.master = credentials["master"]

dekubot.run(token)