import os
print("TOKEN LENGTH:", len(os.getenv("DISCORD_TOKEN") or ""))

import os
from flask import Flask
from threading import Thread
import discord
from discord.ext import commands

# -------- BOT INTENTS --------
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)


# -------- ROLE NAMES --------
NEW_MEMBER_ROLE = "New-Member"
MEMBER_ROLE = "[Member]"

# -------- VERIFY BUTTON --------
class VerifyView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Verify",
        style=discord.ButtonStyle.green,
        custom_id="verify_button"
    )
    async def verify(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        member = interaction.user

        new_member_role = discord.utils.get(guild.roles, name=NEW_MEMBER_ROLE)
        member_role = discord.utils.get(guild.roles, name=MEMBER_ROLE)

        if not new_member_role or not member_role:
            await interaction.response.send_message(
                "❌ Roles not found. Contact an admin.",
                ephemeral=True
            )
            return

        await member.add_roles(member_role)
        await member.remove_roles(new_member_role)

        await interaction.response.send_message(
            "✅ You are now verified!",
            ephemeral=True
        )

# -------- BOT READY --------
@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")
    bot.add_view(VerifyView())

# -------- SEND VERIFY MESSAGE --------
@bot.command()
@commands.has_permissions(administrator=True)
async def send_verify(ctx):
    embed = discord.Embed(
        title="Server Verification",
        description="Click the button below to verify and gain access.",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed, view=VerifyView())

# -------- RUN BOT --------
@bot.command()
async def test(ctx):
    await ctx.send("Bot commands are working!")

import os

app = Flask("")

@app.route("/")
def home():
    return "Bot is alive!"

def run_web():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    Thread(target=run_web).start()
    
import os

bot.run(os.getenv("DISCORD_TOKEN"))






