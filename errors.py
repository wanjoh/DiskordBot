from main import *

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(s_nemaDjidanja)

@pusti.error
async def resi_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(s_staPustiti)


@resi.error
async def resi_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(s_kogaResiti)