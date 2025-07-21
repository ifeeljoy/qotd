
# About
An automated user-submitted question of the day system. If you do not want to host the bot on your personal device and don't mind paying for a cheap alterative ($1.50/month), use [this guide](https://github.com/ifeeljoy/self-host-guide) for setup. 

# How it works
Server members can submit questions using `/submit` followed by their question. 

The bot will send the submission to the review channel specified in the `.env` file. Admins (or any member with the `MANAGE SERVER` permission) can approve or deny the submission by reacting with the corresponding emoji. 

[![IMG-5677.jpg](https://i.postimg.cc/pX3QzdGZ/IMG-5677.jpg)](https://postimg.cc/kBFtd7d6)

Once approved, submissions will be added to a queue and posted to the qotd channel specified in the `.env` file. The bot will automatically post questions from the queue every 24 hours after the last question until the queue is empty.

[![IMG-5678.jpg](https://i.postimg.cc/VNtCqyZb/IMG-5678.jpg)](https://postimg.cc/KKZjbW2Z)

[![IMG-5679.jpg](https://i.postimg.cc/BZTRhXPm/IMG-5679.jpg)](https://postimg.cc/JthT07qX)

The bot requires the `SEND MESSAGES`, `READ MESSAGES`, `READ MESSAGE HISTORY`, `ADD REACTIONS`, `USE APPLICATION COMMANDS`, and `MENTION @EVERYONE, @HERE, AND ALL ROLES` permissions.

# Dependencies

discord.py>=2.3.2

python-dotenv>=1.0.1

# Installation

Make sure you have Python 3.12+

Clone the repository.

```
git clone https://github.com/ifeeljoy/qotd.git
```

Install dependencies.

```
pip install discord.py python-dotenv
```

Rename `.env-example` to `.env` and add the necessary information.

```
# Your bot's token
DISCORD_TOKEN=here

# Your server ID
GUILD_ID=here

# Your Question of the Day channel. Approved questions will be posted here.
QOTD_CHANNEL_ID=here

# Your QotD review channel. Submissions will be sent here to be approved/denied.
REVIEW_CHANNEL_ID=here

# The role ID for the role you want the bot to ping in the QotD channel. It can be any role.
PING_ROLE_ID=here
```

Run the bot.

```
python main.py
```

# License

This project is licensed under the GNU Affero General Public License v3.0. See the LICENSE file for more details.

# Buy Me A Coffee
[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/mozzarella)
