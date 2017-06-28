from discord.ext.commands import Bot
import random
import json

def orange_text(string):
    return '```fix\n' + string + '```'

dekubot = Bot(command_prefix="!")

@dekubot.event
async def on_ready():
    print(dekubot.user.name + ' online!')

@dekubot.command(pass_context=True)
async def hello(ctx):
    """
    Simply say: Hello <Caller>!.
    Get the caller's name by allowing the context to be passed through.
    From the context we can grab message -> author -> display_name.
    """
    caller = ctx.message.author.display_name
    return await dekubot.say(orange_text('Hello {}!'.format(caller)))


@dekubot.command(pass_context=True)
async def roll(ctx):
    """ Rolls a random value from 1-100.
    Returns result in the format: <Caller> rolls <Number> (1-100)
    """
    caller = ctx.message.author.display_name
    number = random.randrange(1,101)
    return await dekubot.say(orange_text('{} rolls {} (1-100)'.format(caller, number)))

@dekubot.command()
async def coinflip():
    """
    50/50 chance of getting Heads/Tails.
    """
    n = random.randrange(0,2)
    result = 'Heads.'
    if n == 0:
        result = 'Tails.'
    return await dekubot.say(orange_text(result))

f = open('credentials.json', 'r')
s = f.read()
credentials = json.loads(s)['dekubot']
token = credentials['token']

dekubot.run(token)
