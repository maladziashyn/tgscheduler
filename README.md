# tgscheduler

This app solves the issue of scheduling more than 100 messages in a Telegram chat.

I've been posting screenshots of interesting research findings from ScienceDaily.com to my family's Telegram chat for quite a while. But as the amount of screenshots was growing I started to schedule the messages in TG. With time I hit the limit of 100 scheduled messages and needed a way to simplify the process of storing screenshots and scheduling them. Hence this app.

It's running on a home server, and it's purpose is twofold:

* `receiver.py`: allows to send screenshots to my Telegram bot at any time and in any quantities, and then saves them in SQLite database.
* `sender.py` plus `crontab`: send the screenshots at scheduled times to my family Telegram chat.

On the back-end the project uses SQLite database and SQLAlchemy.

## Virtual environment

After cloning, go to project's directory, and:

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## bootstrap.py

This scripts does some initial project setup, e.g. creates database file `bot_data.db` and creates its only table, makes a directory for images, and removes logs if any.

The project uses `.env` file that must contain these keys with your values:

* `bot_token` - your Telegram bot token
* `sender_chat_id` - this is the target chat for sending the screenshots, family chat in my case
* `receiver_chat_id` - chat with your bot, this is where you dump the screenshots

## Create a systemd service

To make sure `receiver.py` runs after the server reboots, follow these steps below.

Create entry:
```
sudo vim /etc/systemd/system/tg_rcv.service
```

Add contents:

```
[Unit]
Description=TG receiver for images and text
After=network-online.target
Wants=network-online.target

[Service]
ExecStart=/home/rsm/projects/tgscheduler/start_tg_receiver.sh

[Install]
WantedBy=multi-user.target
```

Add execute permissions:

```
sudo chmod u+x /home/rsm/projects/tgscheduler/start_tg_receiver.sh
```

Then:

```
sudo systemctl daemon-reload
sudo systemctl enable tg_rcv.service
sudo systemctl start tg_rcv.service
```

## Add a crontab entry

Add execute permissions:

```
cd ~/projects/tgscheduler
sudo chmod u+x sender.py receiver.py
```

Add shebang lines at the beginning to sender.py and receiver.py:

```
#!/home/rsm/projects/tgscheduler/venv/bin/python3
```

Edit crontab:

```
crontab -e
```

Add the below as last line, to run at 16:00 and 17:00 local time from Monday to Friday:

```
0 16,17 * * 1-5 /home/rsm/projects/tgscheduler/sender.py
```

Ensure there's an empty line at the end.

## bonus: tmux script to work on project

To quickly start working on this project, I use `kickstart.sh` script that starts a new tmux session with several windows, dedicated e.g. to:

* main: enable virtual environment and run scripts
* vim: window for vim editor
* git: window for git commands

Add execute permissions to the script:

```
cd ~/projects/tgscheduler
sudo chmod u+x kickstart.sh
```

And run the script. When running directly from project's directory, type:

```
./kickstart.sh
```

