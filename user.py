import requests
import os
from discord import File
from github import Github
from github.ContentFile import ContentFile
from github.GithubException import UnknownObjectException
from static import *

users = []


def authentic(email, password):
    github_user = Github(email, password).get_user()
    try:
        repos = [repo for repo in github_user.get_repos()]
        return True
    except:
        return False


def multi_contents_description(contents):
    description = '```\n'
    for content in contents:
        description += content.name + '\n'
    description += '```'
    return description


def remove_slash(string):
    chars = [char for char in string]
    if chars[0] == '/':
        del chars[0]
    return ''.join(chars)


class User:
    current_repo = ''
    current_location = ''

    def __init__(self, discord, github):
        self.discord = discord
        self.github = github
        self.github_user = github.get_user()
        self.directory = './' + str(discord.id)
        os.mkdir(self.directory)
        users.append(self)

    async def sign_out(self, channel):
        os.rmdir(self.directory)
        users.remove(self)
        await channel.send(signed_out_message)

    async def ls(self, channel):
        if not self.current_repo:
            repos_description = multi_contents_description(self.github_user.get_repos())
            return await channel.send(embed=Embed(title='Repositories',
                                                  description=repos_description,
                                                  url=self.github_user.html_url,
                                                  color=color))
        repo = self.github_user.get_repo(self.current_repo)
        repo_contents = repo.get_contents(self.current_location)
        if isinstance(repo_contents, ContentFile):
            contents_description = f'```\n{repo_contents.name}\n```'
        else:
            contents_description = multi_contents_description(repo_contents)
        return await channel.send(embed=Embed(title=f'{self.current_repo}/{self.current_location}',
                                              description=contents_description,
                                              url=repo.html_url,
                                              color=color))

    async def pwd(self, channel):
        return await channel.send(f'```\n~/{self.current_repo}/{self.current_location}\n```')

    async def cd__(self, channel):
        if self.current_repo or self.current_location:
            if self.current_location:
                location_path = self.current_location.split('/')
                del location_path[-1]
                location_path = [item for item in location_path if item]
                self.current_location = ''
                for item in location_path:
                    self.current_location += '/' + item
                return await self.pwd(channel)
            self.current_repo = ''
            return await self.pwd(channel)
        return await channel.send(too_far_back_message)

    async def cd(self, path, channel):
        try:
            if not self.current_repo:
                repo = self.github_user.get_repo(path.split('/')[0])
                self.current_repo = path.split('/')[0]
            if not self.current_location:
                content = self.github_user.get_repo(self.current_repo).get_contents(path.replace(self.current_repo, ''))
                self.current_location = path.replace(self.current_repo, '')
            else:
                content = self.github_user.get_repo(self.current_repo).get_contents(f'{self.current_location}/{path}')
                self.current_location += '/' + path
            await self.pwd(channel)
        except UnknownObjectException:
            await channel.send(non_existent_location_message)

    async def upload(self, file_name, channel):
        try:
            repo = self.github_user.get_repo(self.current_repo)
            download_url = repo.get_contents(f'{self.current_location}/{file_name}').download_url
            file_content = requests.get(download_url).content.decode()
            with open(f'{self.directory}/{file_name}', 'w') as file:
                file.write(file_content)
            await channel.send(file=File(f'{self.directory}/{file_name}'))
            os.remove(f'{self.directory}/{file_name}')
        except UnknownObjectException:
            await channel.send(non_existent_location_message)

    async def nano(self, file_name, message, channel):
        repo = self.github_user.get_repo(self.current_repo)
        try:
            file_content = await message.attachments[0].read()
            if file_name in [content.name for content in repo.get_contents(self.current_location)]:
                file = repo.get_contents(f'{self.current_location}/{file_name}')
                repo.update_file(file.path, updated_gitbot, file_content, file.sha)
            else:
                repo.create_file(remove_slash(f'{self.current_location}/{file_name}'), created_gitbot, file_content)
                file = repo.get_contents(f'{self.current_location}/{file_name}')
            await channel.send(file.html_url)
        except IndexError:
            await channel.send(file_not_attached_message)

    async def rm(self, file_name, channel):
        try:
            repo = self.github_user.get_repo(self.current_repo)
            file = repo.get_contents(f'{self.current_location}/{file_name}')
            repo.delete_file(file.path, deleted_gitbot, file.sha)
            await channel.send(f'I have deleted the file under the name, \"{file_name}.\"')
        except UnknownObjectException:
            await channel.send(non_existent_location_message)

    async def mkdir(self, dir_name, channel):
        repo = self.github_user.get_repo(self.current_repo)
        repo.create_file(remove_slash(f'{self.current_location}/{dir_name}/info.txt'), created_gitbot, f'About {dir_name}')
        await channel.send(f'I have create a directory under the name, \"{dir_name}.\"')

    async def rmdir(self, dir_name, channel, final):
        repo = self.github_user.get_repo(self.current_repo)
        try:
            for content in repo.get_contents(f'{self.current_location}/{dir_name}'):
                if content.type == 'file':
                    repo.delete_file(content.path, deleted_gitbot, content.sha)
                elif content.type == 'dir':
                    await self.rmdir(f'{dir_name}/{content.name}', channel, False)
            if final:
                await channel.send(f'I have deleted a directory under the name, \"{dir_name}.\"')
        except UnknownObjectException:
            await channel.send(non_existent_location_message)

    async def mkrepo(self, repo_name, channel):
        self.github_user.create_repo(repo_name)
        repo = self.github_user.get_repo(repo_name)
        repo.create_file(remove_slash(f'{self.current_location}/README.md'), created_gitbot, f'# {repo_name}')
        await channel.send(repo.html_url)

    async def rmrepo(self, repo_name, channel):
        try:
            repo = self.github_user.get_repo(repo_name)
            repo.delete()
            await channel.send(f'I have deleted a repository under the name, \"{repo_name}.\"')
        except UnknownObjectException:
            await channel.send(non_existent_location_message)
