from discord.ext.commands import Bot
import random
import json

def orange_text(string):
    return "```fix\n" + string + "```"

dekubot = Bot(command_prefix="!")

@dekubot.event
async def on_ready():
    print(dekubot.user.name + " online!")

@dekubot.command(pass_context=True)
async def hello(ctx):
    """ A friendly greeting.
    Simply say: Hello <Caller>!.
    Get the caller's name by allowing the context to be passed through.
    From the context we can grab message -> author -> display_name.
    """
    caller = ctx.message.author.display_name
    return await dekubot.say(orange_text("Hello {}!".format(caller)))


@dekubot.command(pass_context=True)
async def roll(ctx):
    """ Rolls a random value from 1-100.
    Returns result in the format: <Caller> rolls <Number> (1-100)
    """
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
    return await dekubot.say("<https://streamable.com/s9at>\n"
                             "<https://streamable.com/e2az>\n"
                             ":rage:")

def is_me(m):
    return m.author == dekubot.user

@dekubot.command(pass_context=True)
async def clear(ctx):
    """Clears recent replies from DekuBot.
    Only checks within the last 100 messages.
    Also returns how many successful deletes there were.
    REQUIRES MANAGE MESSAGES PERMISSION.
    """
    deleted = await dekubot.purge_from(ctx.message.channel, limit=100, check=is_me)
    return await dekubot.say(orange_text("Deleted {} message(s)".format(len(deleted))))


f = open("credentials.json", "r")
s = f.read()
credentials = json.loads(s)["dekubot"]
token = credentials["token"]

dekubot.run(token)
