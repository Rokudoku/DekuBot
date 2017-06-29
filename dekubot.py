from discord.ext.commands import Bot
import random
import json

dekubot = Bot(command_prefix="!")

def orange_text(string):
    return "```fix\n" + string + "```"

def is_me(m):
    return m.author == dekubot.user

@dekubot.event
async def on_ready():
    print(dekubot.user.name + " online!")

@dekubot.command(pass_context=True)
async def roll(ctx):
    """ Rolls a random value from 1-100.
    Returns result in the format: <Caller> rolls <Number> (1-100)
    Get the caller's name by allowing the context to be passed through.
    From the context we can grab message -> author -> display_name.
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

@dekubot.command(pass_context=True)
async def ask(ctx):
    """ Ask DekuBot a question.
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
async def clear(ctx):
    """Clears recent replies from DekuBot.
    Only checks within the last 100 messages.
    Also returns how many successful deletes there were.
    REQUIRES MANAGE MESSAGES PERMISSION.
    """
    deleted = await dekubot.purge_from(ctx.message.channel, limit=100, check=is_me)
    return await dekubot.say(orange_text("Deleted {} message(s)".format(len(deleted))))

@dekubot.event
async def on_message(message):
    # if i want to add any message to look out for
    # remember that bot should never talk to itself
    # to make sure the bot keeps looking for the other commands...
    await dekubot.process_commands(message)

f = open("credentials.json", "r")
s = f.read()
credentials = json.loads(s)["dekubot"]
token = credentials["token"]

dekubot.run(token)