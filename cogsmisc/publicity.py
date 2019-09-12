"""
Created on Dec 29, 2016

@author: andrew
"""
import asyncio
import logging

import aiohttp
from discord.ext import commands

import credentials

log = logging.getLogger(__name__)

DBL_API = "https://discordbots.org/api/bots/"


class Publicity(commands.Cog):
    """
    Sends updates to bot repos.
    """

    def __init__(self, bot):
        self.bot = bot
        self.bot.loop.create_task(self.background_update())

    async def update_server_count(self):
        if self.bot.testing or not credentials.dbl_token:
            return
        payload = {"server_count": len(self.bot.guilds)}
        async with aiohttp.ClientSession() as aioclient:
            try:
                await aioclient.post(f"{DBL_API}{self.bot.user.id}/stats", data=payload,
                                     headers={"Authorization": credentials.dbl_token})
            except Exception as e:
                log.error(f"Error posting server count: {e}")

    async def background_update(self):
        try:
            await self.bot.wait_until_ready()
            while not self.bot.is_closed():
                await self.update_server_count()
                await asyncio.sleep(3600)  # every hour
        except asyncio.CancelledError:
            pass

    @commands.Cog.listener()
    async def on_guild_join(self, server):
        log.info('Joined server {}: {}, {} members ({} bot)'.format(server, server.id, len(server.members),
                                                                    sum(1 for m in server.members if m.bot)))

    @commands.Cog.listener()
    async def on_guild_remove(self, server):
        log.info('Left server {}: {}, {} members ({} bot)'.format(server, server.id, len(server.members),
                                                                  sum(1 for m in server.members if m.bot)))


def setup(bot):
    bot.add_cog(Publicity(bot))
