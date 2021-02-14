import discord
from user import *
from static import *

client = discord.Client()


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=help_command))


@client.event
async def on_message(message):
    if not message.author.bot:
        if message.content == sign_in_instructions_command:
            await message.author.send(embed=sign_in_instructions_message)
            await message.channel.send(sign_in_instructions_sent_message)

        elif message.content == status_command:
            user = [user for user in users if user.discord == message.author]
            if user:
                await message.channel.send(signed_in_message + user[0].github_user.name + '.')
            else:
                await message.channel.send(not_signed_in_message)

        elif message.content.find(sign_in_split) != -1 and len(message.content) == 41:
            token = message.content[1:]
            if authentic(token):
                User(message.author, Github(token))
                await message.channel.send(sign_in_success_message)
            else:
                await message.channel.send(sign_in_failure_message)
            if message.guild:
                await message.delete()

        elif message.content.find(help_command) != -1:
            try:
                await message.channel.send(embed=helps[message.content])
            except KeyError:pass

        elif message.author in [user.discord for user in users]:
            user = [user for user in users if user.discord == message.author][0]
            if message.content == sign_out_command:
                await user.sign_out(message.channel)

            elif message.content == ls_command:
                await user.ls(message.channel)

            elif message.content == pwd_command:
                await user.pwd(message.channel)

            elif message.content == cd__command:
                await user.cd__(message.channel)

            elif message.content.find(cd_command) != -1 and message.content.replace(cd_command, ''):
                await user.cd(message.content.replace(cd_command, ''), message.channel)

            elif message.content.find(upload_command) != -1 and message.content.replace(upload_command, ''):
                await user.upload(message.content.replace(upload_command, ''), message.channel)

            elif message.content.find(nano_command) != -1 and message.content.replace(nano_command, ''):
                await user.nano(message.content.replace(nano_command, ''), message, message.channel)

            elif message.content.find(rm_command) != -1 and message.content.replace(rm_command, ''):
                await user.rm(message.content.replace(rm_command, ''), message.channel)

            elif message.content.find(mkdir_command) != -1 and message.content.replace(mkdir_command, ''):
                await user.mkdir(message.content.replace(mkdir_command, ''), message.channel)

            elif message.content.find(rmdir_command) != -1 and message.content.replace(rmdir_command, ''):
                await user.rmdir(message.content.replace(rmdir_command, ''), message.channel, True)

            elif message.content.find(mkrepo_command) != -1 and message.content.replace(mkrepo_command, ''):
                await user.mkrepo(message.content.replace(mkrepo_command, ''), message.channel)

            elif message.content.find(rmrepo_command) != -1 and message.content.replace(rmrepo_command, ''):
                await user.rmrepo(message.content.replace(rmrepo_command, ''), message.channel)


client.run(token)
