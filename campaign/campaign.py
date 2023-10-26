from random import choices

import discord
from redbot.core import commands
from redbot.core.bot import Red

PETRA_RACES = {
    'Human': 0.15,
    'Halfling': 0.13,
    'Dwarf': 0.11,
    'Half-Elf': 0.09,
    'Elf': 0.06,
    'Gnome': 0.055,
    'Half-Orc': 0.05,
    'Tiefling': 0.05,
    'Dragonborn': 0.04,
    'Vedalken': 0.03,
    'Firbolg': 0.0225,
    'Aarakocra': 0.02,
    'Centaur': 0.02,
    'Genasi': 0.02,
    'Lizardfolk': 0.02,
    'Minotaur': 0.02,
    'Tabaxi': 0.02,
    'Changeling': 0.015,
    'Kenku': 0.015,
    'Goliath': 0.01,
    'Loxodon': 0.01,
    'Satyr': 0.01,
    'Shifter': 0.01,
    'Kalashtar': 0.005,
    'Leonin': 0.005,
    'Other/Mixed': 0.005,
    'Tortle': 0.005,
    'Aasimar': 0.0025
}


class Campaign(commands.Cog):
    """
    Utility commands for our campaign.
    """

    async def red_get_data_for_user(self, *, user_id):
        return {}

    async def red_delete_data_for_user(self, *, requester, user_id):
        pass

    def __init__(self, bot: Red) -> None:
        self.bot = bot

    @commands.command()
    async def character(self, ctx: commands.Context) -> None:
        """Roll base ability scores for a new character.

        Find the minimal and maximal sums of six roll sets.
        - A roll set is 5d6.
        - The minimal sum is the sum of the lowest three values.
        - The maximal sum is the sum of the highest three values.

        Sort the sums from lowest to highest. 
        Keep only the values from the second and fourth quarters.

        If the sum of the kept values is not in the desired range of 68-74, repeat the process.
        """
        # Initialize a list of scores with zero so the first while condition passes.
        scores = [0]
        # Repeat process while scores are not in desired range.
        while sum(scores) < 68 or sum(scores) > 74:
            # Placeholder to store the minimal and maximal sums.
            results = []

            # Create six roll sets.
            for i in range(6):
                # Roll 5d6.
                rolls = choices(range(1, 7), k=5)
                rolls.sort()

                # Find the minimal and maximal sums.
                high = sum(rolls[2:5])
                low = sum(rolls[0:3])

                results.append(high)
                results.append(low)

                # Sort from lowest to highest.
                results.sort()

                # Keep values in second and fourth quarters.
                scores = results[3:6] + results[9:12]

        # Format embedded message.
        color = await self.bot.get_embed_color(ctx)
        title = 'Your scores are: ' + str(scores)
        desc = 'Your total is ' + str(
            sum(scores)) + '. The desired range is 68-74.'

        embed = discord.Embed(title=title, description=desc, color=color)

        await ctx.send(embed=embed)

    @commands.group()
    async def petra(self, ctx: commands.Context):
        """Utility commands specific to the Petra campaign."""
        pass

    @petra.command()
    async def charge(self, ctx: commands.Context, travel_pace: int,
                     hours_charged: int):
        """Calculate the number of miles traveled by a sand ship.
    
        <base travel pace> <number of hours charged>
        """
        miles = travel_pace * (24 + hours_charged)

        # Format embedded message.
        color = await self.bot.get_embed_color(ctx)
        title = 'Miles traveled: ' + str(miles)
        desc = str(travel_pace) + '*(24+' + str(hours_charged) + ')'

        embed = discord.Embed(title=title, description=desc, color=color)

        await ctx.send(embed=embed)

    @petra.command()
    async def race(self, ctx: commands.Context, n: int | None = 1):
        """Randomly generate character races for Petra.

        <optional, number>
        """
        # Select races by associated weights.
        races = choices(list(PETRA_RACES.keys()),
                        list(PETRA_RACES.values()),
                        k=n)

        # Format embedded message.
        color = await self.bot.get_embed_color(ctx)
        title = ', '.join(races)

        embed = discord.Embed(title=title, color=color)

        await ctx.send(embed=embed)
