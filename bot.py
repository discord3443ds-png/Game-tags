import discord
from discord import app_commands
from discord.ext import commands
import json
import os

# Discord Bot Token und IDs aus Environment Variables
TOKEN = os.getenv("TOKEN")  # Deinen Discord-Bot Token eintragen
GUILD_ID = int(os.getenv("GUILD_ID"))  # Deine Server ID
ADMIN_ROLE_ID = 1410993496902467710  # Admin Role ID
DATA_FILE = "tags.json"

# Bot ohne Voice/Audio
bot = commands.Bot(command_prefix="/", intents=discord.Intents.default())

@bot.event
async def on_ready():
    print(f"Bot online als {bot.user}")
    await bot.tree.sync(guild=discord.Object(id=GUILD_ID))
    print("Slash Commands synchronisiert!")

# Command um Tag zu setzen
@bot.tree.command(name="givetag", description="Setzt Roblox Tag", guild=discord.Object(id=GUILD_ID))
@app_commands.describe(roblox_id="Roblox UserId", tag="Tag")
async def givetag(interaction: discord.Interaction, roblox_id: str, tag: str):
    # Admin-Prüfung
    if ADMIN_ROLE_ID not in [role.id for role in interaction.user.roles]:
        await interaction.response.send_message("❌ Keine Berechtigung!", ephemeral=True)
        return
    # Tags laden oder neues Dict erstellen
    data = {}
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
    data[roblox_id] = tag
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)
    await interaction.response.send_message(f"✅ Tag '{tag}' gesetzt!")

# Optional: Command um Tag abzurufen
@bot.tree.command(name="gettag", description="Zeigt Roblox Tag", guild=discord.Object(id=GUILD_ID))
@app_commands.describe(roblox_id="Roblox UserId")
async def gettag(interaction: discord.Interaction, roblox_id: str):
    data = {}
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
    tag = data.get(roblox_id, "")
    if tag:
        await interaction.response.send_message(f"Tag für {roblox_id}: {tag}")
    else:
        await interaction.response.send_message("Kein Tag gesetzt.")

bot.run(TOKEN)
