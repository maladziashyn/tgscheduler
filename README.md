# tgscheduler
DB of text and photos, and a scheduler to a Telegram chat.

## Create a systemd service

Create entry:
```
sudo vim /etc/systemd/system/tg_rcv.service
```

Add contents:

```
[Unit]
Description=TG receiver for cool photos
After=network.target

[Service]
Type=oneshot
ExecStart=/home/rsm/projects/tgscheduler/start_tg_receiver.sh
RemainAfterExit=yes
User=rsm

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

For this to work, ensure you have a virtual environment:

```
cd ~/projects/tgscheduler
python3.14 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Edit crontab:

```
crontab -e
```

Add as last line, to run at 16:00 and 17:00 local time from Monday to Friday:

```
0 16,17 * * 1-5 /home/rsm/projects/tgscheduler/sender.py
```

Ensure there's an empty line at the end.

