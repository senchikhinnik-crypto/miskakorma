import discord
from discord.ext import commands

# ====== ВСТАВЬ СВОИ ДАННЫЕ СЮДА ======
import os
TOKEN = os.getenv("TOKEN")
ID_SERVERA = 1500151026932650036
ID_KANALA_PRIVETSTVIE = 1500153239256043560
ID_ROLI_UCHASTNIK = 1500158358022258798

# ====== КОД БОТА (НЕ ТРОГАЙ) ======
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(ID_KANALA_PRIVETSTVIE)
    if channel:
        embed = discord.Embed(
            title=f"🎬 Добро пожаловать, {member.name}!",
            description="Ты попал на съёмочную площадку сервера **miskakorma** — здесь снимаются самые сочные лав-хиты!\n\n"
                        "✅ **Чтобы попасть в команду:** нажми на 🎮 под этим сообщением\n"
                        "📝 **Потом загляни в** #│знакомство — расскажи о себе\n"
                        "🎥 **Новые видео выходят здесь раньше, чем на YouTube!**",
            color=0xFF69B4
        )
        await channel.send(f"Привет, {member.mention}!", embed=embed)

@bot.event
async def on_raw_reaction_add(payload):
    if payload.user_id == bot.user.id:
        return
    if payload.channel_id == ID_KANALA_PRIVETSTVIE:
        if str(payload.emoji) == "🎮":
            guild = bot.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)
            role = guild.get_role(ID_ROLI_UCHASTNIK)
            if role:
                await member.add_roles(role)

@bot.tree.command(name="кастинг", description="Объявление о поиске актёра")
async def casting(interaction: discord.Interaction, роль: str, описание: str):
    embed = discord.Embed(title=f"🎬 КАСТИНГ: {роль}", description=описание, color=0xFF4500)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="видео", description="Анонс нового ролика")
async def video(interaction: discord.Interaction, название: str, ссылка: str):
    embed = discord.Embed(title=f"📹 НОВОЕ ВИДЕО: {название}", description=ссылка, color=0x00FF7F)
    await interaction.response.send_message(embed=embed)

@bot.event
async def on_ready():
    print(f"✅ Бот {bot.user} запущен!")
    await bot.tree.sync(guild=discord.Object(id=ID_SERVERA))
    print("✅ Команды /кастинг и /видео готовы!")

bot.run(TOKEN)