import discord
from discord import app_commands
from discord.ext import commands
import json
import os

# ---- Environment Variables ----
TOKEN = os.getenv("TOKEN")  # Discord Bot Token
GUILD_ID = int(os.getenv("GUILD_ID"))  # Discord Server ID
ADMIN_ROLE_ID = int(os.getenv("ADMIN_ROLE_ID"))  # Admin Role ID
DATA_FILE = "tags.json"
# --------------------------------

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

# Slash Commands für Guild sofort synchronisieren
@bot.event
async def on_ready():
    print(f"Bot ist online als {bot.user}")
    guild = discord.Object(id=GUILD_ID)
    try:
        await bot.tree.sync(guild=guild)
        print(f"Slash Commands für Guild {GUILD_ID} synchronisiert")
    except Exception as e:
        print("Fehler beim Sync:", e)

# /givetag
@bot.tree.command(name="givetag", description="Setzt einen Roblox Tag", guild=discord.Object(id=GUILD_ID))
@app_commands.describe(roblox_id="Roblox UserId", tag="Tag zum Setzen")
async def givetag(interaction: discord.Interaction, roblox_id: str, tag: str):
    if ADMIN_ROLE_ID not in [role.id for role in interaction.user.roles]:
        await interaction.response.send_message("❌ Keine Berechtigung!", ephemeral=True)
        return

    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
    else:
        data = {}

    data[roblox_id] = tag
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

    await interaction.response.send_message(f"✅ Tag '{tag}' für Roblox-ID {roblox_id} gesetzt!")

# /gettag
@bot.tree.command(name="gettag", description="Zeigt einen Roblox Tag", guild=discord.Object(id=GUILD_ID))
@app_commands.describe(roblox_id="Roblox UserId")
async def gettag(interaction: discord.Interaction, roblox_id: str):
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
        tag = data.get(roblox_id, "")
        if tag:
            await interaction.response.send_message(f"Tag für {roblox_id}: {tag}")
        else:
            await interaction.response.send_message("Kein Tag gesetzt.")
    else:
        await interaction.response.send_message("Keine Tags gefunden.")

bot.run(TOKEN)
