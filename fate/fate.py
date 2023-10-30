from random import choices

import discord
from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.config import Config

import contextlib
from typing import Union


async def try_delete(message):
    with contextlib.suppress(discord.HTTPException):
        await message.delete()


class FateRoller(commands.Cog):
    """
    A dice roller for the FATE system.
    """

    async def red_get_data_for_user(self, *, user_id):
        return {}

    async def red_delete_data_for_user(self, *, requester, user_id):
        pass

    def __init__(self, bot: Red) -> None:
        self.bot = bot

    @commands.command(aliases=['f'])
    async def fate(self,
                   ctx: commands.Context,
                   modifier: Union[int, None] = None) -> None:
        """Rolls 4dF and optionally adds a modifier.

        Fate/fudge dice (dF) are dice with values of -1, 0, and +1.
        """
        # Roll 4dF.
        str_rolls = choices(['`-1`', '`0`', '`+1`'], k=4)
        num_rolls = [int(i.replace('`', '')) for i in str_rolls]

        # Format message.
        header = f'{ctx.author.mention}  :game_die:\n'

        # Show result and total with optional modifier.
        if modifier is not None:
            result = ('**Result:** 4dF (' + ', '.join(str_rolls) + ') + ' +
                      str(modifier) + '\n')
            total = '**Total:** ' + str(sum(num_rolls, modifier)) + '\n'
        else:
            result = ('**Result:** 4dF (' + ', '.join(str_rolls) + ')\n')
            total = '**Total:** ' + str(sum(num_rolls)) + '\n'

        out = header + result + total

        await try_delete(ctx.message)
        await ctx.send(
            out, allowed_mentions=discord.AllowedMentions(users=[ctx.author]))
