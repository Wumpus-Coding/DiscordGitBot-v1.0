from discord import Embed

color = 0x505050
token = 'YOUR_DISCORD_BOT_TOKEN_HERE'

sign_in_split = '>'
command_prefix = 'gb.'
sign_in_instructions_command = command_prefix + 'sign in'
sign_out_command = command_prefix + 'sign out'
status_command = command_prefix + 'status'
ls_command = 'ls'
pwd_command = 'pwd'
cd_command = 'cd '
cd__command = 'cd ..'
upload_command = 'upload '
nano_command = 'nano '
rm_command = 'rm '
mkdir_command = 'mkdir '
rmdir_command = 'rmdir '
mkrepo_command = 'mkrepo '
rmrepo_command = 'rmrepo '
help_command = command_prefix + 'help'
help_basic_command = help_command + ' basic'
help_file_command = help_command + ' file'
help_directory_command = help_command + ' directory'
help_repo_command = help_command + ' repo'

sign_in_instructions_sent_message = 'Check your DMs for instructions on how to sign in with GitBot.'
sign_in_success_message = 'Hooray!  You have successfully signed into GitBot.'
sign_in_failure_message = 'Uh oh.  Looks like the credentials you gave me were invalid.'
signed_out_message = 'You have been signed out of GitBot.'
signed_in_message = 'You are signed in as '
not_signed_in_message = f'You are not signed in with GitBot.  For instructions on how to sign in, type `{sign_in_instructions_command}`.'
too_far_back_message = 'You cannot go back any further.'
non_existent_location_message = 'Sorry, but I could not find the item from the location you requested.'
file_not_attached_message = 'Error!  Please attach a file to your message.'
created_gitbot = 'Created By GitBot'
updated_gitbot = 'Updated By GitBot'
deleted_gitbot = 'Deleted By GitBot'

sign_in_instructions_message = Embed(
    title='Sign In With GitBot',
    description=f'To sign in with GitBot, type {sign_in_split} and then your token.',
    color=color
)
sign_in_instructions_message.add_field(name='Example', value=f'{sign_in_split}bc20fae37b2923a75836fd206068b7402e7e79f1', inline=False)
sign_in_instructions_message.add_field(name='Note', value='It is recommended to sign in through a private dm, rather than on a server.', inline=False)

help_message = Embed(
    title='Help',
    description='Use the commands below for detailed help on a specific topic.',
    color=color
)
help_message.add_field(name=sign_in_instructions_command, value='Instructions on how to sign in.')
help_message.add_field(name=sign_out_command, value='Signs out a user.')
help_message.add_field(name=status_command, value='Returns current status.')
help_message.add_field(name=help_basic_command, value='Basic GitBot commands.')
help_message.add_field(name=help_file_command, value='GitBot file Commands')
help_message.add_field(name=help_directory_command, value='GitBot directory commands.')
help_message.add_field(name=help_repo_command, value='GitBot repository commands.')

help_basic_message = Embed(
    title='Help Basic',
    description='Here are some basic GitBot commands.',
    color=color
)
help_basic_message.add_field(name=ls_command, value='Lists items in current directory.', inline=False)
help_basic_message.add_field(name=pwd_command, value='Returns present working directory.', inline=False)
help_basic_message.add_field(name=cd_command + '<directory_name>', value='Moves to a new directory.', inline=False)
help_basic_message.add_field(name=cd__command, value='Moves one directory back.', inline=False)

help_file_message = Embed(
    title='Help File',
    description='Here are some GitBot file commands.',
    color=color
)
help_file_message.add_field(name=nano_command + '<file_name>', value='Creates or edits a file.', inline=False)
help_file_message.add_field(name=rm_command + '<file_name>', value='Removes a file from GitHub.', inline=False)
help_file_message.add_field(name=upload_command + '<file_name>', value='Uploads a file from GitHub.', inline=False)

help_directory_message = Embed(
    title='Help Directory',
    description='Here are some GitBot directory commands.',
    color=color
)
help_directory_message.add_field(name=mkdir_command + ' <directory_name>', value='Makes a new directory.', inline=False)
help_directory_message.add_field(name=rmdir_command + ' <directory_name>', value='Removes a directory.', inline=False)

help_repo_message = Embed(
    title='Help Repo',
    description='Here are some GitBot repository commands.',
    color=color
)
help_repo_message.add_field(name=mkrepo_command + '<repo_name>', value='Makes a new repository.', inline=False)
help_repo_message.add_field(name=rmrepo_command + '<repo_name>', value='Removes a repository.', inline=False)

helps = {
    help_command: help_message,
    help_basic_command: help_basic_message,
    help_file_command: help_file_message,
    help_directory_command: help_directory_message,
    help_repo_command: help_repo_message
}
