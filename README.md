# DiscordRoleSheeter

DiscordRoleSheeter is a tool for efficient management of Discord server roles. It fetches roles and members from a Discord guild via a Discord bot, allows modifications in an Excel spreadsheet, and pushes changes back to Discord, simplifying the process and reducing errors.

## Motivation

Discord servers, especially larger ones, often have a complex structure of roles and members. Managing these roles manually can be a time-consuming and error-prone task. DiscordRoleSheeter was created to address this issue. It provides a user-friendly graphical interface that simplifies the process of managing roles. By leveraging the power of Excel for data manipulation, it allows administrators to pull role and member data from Discord, make changes in a familiar spreadsheet environment, and then push those changes back to Discord. This not only saves time but also reduces the likelihood of mistakes.

This is made to be a simple application for you to setup and run your own Discord bot so you have full ownership of the role managment. It's also supposed to emulate a github workflow by pushing and pulling changes from and to Discord for a more keen user experience.

## Features

- Fetch members and roles from a Discord guild
- Export members and roles to an Excel spreadsheet
- Make changes to roles in the Excel spreadsheet
- See changes in the in a small and nicely formatted scrollable view
- Push changes from the Excel spreadsheet back to Discord

## Installation

Either download from [releases](https://github.com/CaptainFallaway/DiscordRoleSheeter/releases).

Or:

1. Clone the repository: `git clone https://github.com/yourusername/DiscordRoleSheeter.git`
2. Navigate to the project directory: `cd DiscordRoleSheeter`
3. Create a virtual enviroment with python 3.12.
4. Install the required dependencies: `pip install -r requirements.txt`
5. Compile with the batch file `.\build.bat`

## Usage

1. Launch the application to generate the `config.toml` file. You'll be prompted to exit after the file is created.
2. Populate the `config.toml` file with your bot token and guild id (Discord server id), then save the file.
3. Reopen the application and you're all set.
4. The interface is straightforward with only three buttons and detailed information provided for errors, warnings, and other statuses.

## Discord Bot Guide

1. Go to [discord developers](https://discord.com/developers/applications) and create a new application.
2. Go to the bot section and press reset token (So you can copy it) and save it or put it in the `config.toml` file.
3. Go to the Oatuh2 -> Url Generator and select `Bot` in the gray `SCOPES` panel. After that you select `Manage Roles` in the `BOT PERMISSIONS` panel.
4. Copy the Discord link at the bottom of the page and it should look something like this `https://discord.com/api/oauth2/authorize?client_id=xxxxxxxxxxxxxxxxxxx&permissions=268435456&scope=bot`

## Todo

- [ ] Make a websocket connection run as a background task to update bot discord presence.
- [ ] Better errors from discord instead of raw ones from the request.
- [ ] Implement pagination for fetching guild members (only supports up to 1000 members at the moment...)

## License

This project is licensed under the `Unlicense` License - see the [LICENSE](LICENSE) file for details.
