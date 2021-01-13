import discord
import os
import time
import json
import random
import asyncio
import keep_alive
from discord.ext import commands

bot = commands.Bot(command_prefix="!")

def reverse(s): 
    str = "" 
    for i in s: 
        str = i + str
    return str

def convert(seconds):
   return time.strftime("%Hh %Mm %Ss", time.gmtime(seconds))

@bot.event
async def on_ready():
    print(f"Signed in as {bot.user}")

@bot.command(aliases=['s'])
async def start(ctx):
    with open('users.json', 'r') as f:
        users = json.load(f)
    
    users[str(ctx.author.id)] = {}
    user_dict = users[str(ctx.author.id)]
    user_dict['coins'] = 500
    user_dict['job'] = {}
    job = user_dict['job']
    job['name'] = ''
    job['salary'] = ''
    user_dict['items'] = []

    with open('users.json', 'w') as f:
        json.dump(users, f, indent=4)
    
    await ctx.send(':white_check_mark: **Success!** You are now entered!')

@bot.command(aliases=['bal', 'money', 'b'])
async def balance(ctx):
    with open('users.json', 'r') as f:
        users = json.load(f)
    
    coins = users[str(ctx.author.id)]['coins']
    await ctx.send(f"You have **{round(coins)}** coins, {ctx.author.mention}.")

@bot.command()
async def start_work(ctx, job):
    with open('users.json', 'r') as f:
        users = json.load(f)
    with open('jobs.json', 'r') as f:
        jobs = json.load(f)
    
    jobs_dict = users[str(ctx.author.id)]['job']

    if jobs_dict['name'] != '':
        await ctx.send("You already have a job.")
        return
    
    else:
        if job == 'YouTuber':
            job_name = jobs['jobs'][0]['name']
            salary = jobs['jobs'][0]['salary']

            users[str(ctx.author.id)]['job']['name'] += job_name
            users[str(ctx.author.id)]['job']['salary'] += str(salary)

            with open('users.json', 'w') as f:
                json.dump(users, f, indent=4)
            
            await ctx.send(f"You are now working as a **{job_name}** and your salary is **{salary}**!")
        else:
            await ctx.send(':x: That job does not exist yet!')
            return

@bot.command()
@commands.cooldown(1, 86400, commands.BucketType.user)
async def work_resign(ctx):
    with open('users.json', 'r') as f:
        users = json.load(f)

    job = users[str(ctx.author.id)]['job']['name']
    salary = users[str(ctx.author.id)]['job']['salary']

    if job == '':
        await ctx.send("You don't have a job. Do `!start_work YouTuber` to start your job.")
        return
    
    await ctx.send(f'You have resigned from your job as a **{job}** which had a salary of **{salary}**.')
    users[str(ctx.author.id)]['job']['name'] = ''
    users[str(ctx.author.id)]['job']['salary'] = ''

    with open('users.json', 'w') as f:
        json.dump(users, f, indent=4)

@bot.command()
@commands.cooldown(1, 3600, commands.BucketType.user)
async def work(ctx):
    with open('users.json', 'r') as f:
        users = json.load(f)
    
    salary = users[str(ctx.author.id)]['job']['salary']
    yt_words = open('yt_words.txt').read().split()
    random_word = random.choice(yt_words)
    print(reverse(random_word))
    def check(m):
        return m.author.id == ctx.author.id
    await ctx.send(f'Enter the following word in reverse.\n`{random_word}`')
    response = await bot.wait_for('message', check=check)
    if response.content != reverse(random_word):
        await ctx.send(f'You answered wrong, so you only get **{int(salary) / 2}** coins.')
        users[str(ctx.author.id)]['coins'] += int(salary) / 2
        
    else:
        await ctx.send(f"Good job! You got it right. You get {salary} coins.")
        users[str(ctx.author.id)]['coins'] += int(salary)
        
    with open('users.json', 'w') as f:
        json.dump(users, f, indent=4)

@bot.event
async def on_command_error(ctx, error):    
    if isinstance(error, commands.CommandOnCooldown):
        sec = round(error.retry_after)
        await ctx.send(f"You are on cooldown. Try again in **{convert(sec)}**. ")

keep_alive.keep_alive()
bot.run(os.environ.get("DISCORD_BOT_TOKEN"))