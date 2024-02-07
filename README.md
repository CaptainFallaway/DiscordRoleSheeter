# DiscordRoleSheeter

DiscordRoleSheeter is a GUI application designed to manage user roles in a Discord server. It fetches members and roles from a specified Discord guild in a `config.toml` file and exports the data into an Excel spreadsheet in the same folder. You can then make changes to the Excel sheet and push those changes back to Discord.

## Motivation

Discord servers, especially larger ones, often have a complex structure of roles and members. Managing these roles manually can be a time-consuming and error-prone task. DiscordRoleSheeter was created to address this issue. It provides a user-friendly graphical interface that simplifies the process of managing roles. By leveraging the power of Excel for data manipulation, it allows administrators to pull role and member data from Discord, make changes in a familiar spreadsheet environment, and then push those changes back to Discord. This not only saves time but also reduces the likelihood of mistakes.

## Features

- Fetch members and roles from a Discord guild
- Export members and roles to an Excel spreadsheet
- Make changes to roles in the Excel spreadsheet
- See changes in the in a small and nicely formatted scrollable view
- Push changes from the Excel spreadsheet back to Discord

## Installation

Either download from [releases](https://github.com/CaptainFallaway/DiscordRoleSheeter/releases).

##### Or:

1. Clone the repository: `git clone https://github.com/yourusername/DiscordRoleSheeter.git`
2. Navigate to the project directory: `cd DiscordRoleSheeter`
3. Create a virtual enviroment with python 3.12.
4. Install the required dependencies: `pip install -r requirements.txt`
5. Compile with the batch file `.\build.bat`

## Usage

1. Run the application to create the `config.toml` file, you'll be propmted to exit after file creation.
2. Fill in the `config.toml` file with your bot token and guild id (Discord server id), save the file after.
3. Open the app again and your good to go.
4. The user experience should be friendly if you've read the context above and there is only three buttons and alot of information that will be provided about errors, warning and other statuses.

## Discord Bot Guide

1. Go to [discord developers](https://discord.com/developers/applications) and create a new application.
2. Go to the bot section and press reset token (So you can copy it) and save it or put it in the `config.toml` file.
3. Go to the Oatuh2 -> Url Generator and select `Bot` in the gray `SCOPES` panel. After that you select `Manage Roles` in the `BOT PERMISSIONS` panel.
4. Copy the Discord link at the bottom of the page and it should look something like this `https://discord.com/api/oauth2/authorize?client_id=xxxxxxxxxxxxxxxxxxx&permissions=268435456&scope=bot`

## License

This project is licensed under the `Unlicense` License - see the [LICENSE](LICENSE) file for details.