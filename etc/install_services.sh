#!/usr/bin/env bash
apt-get install virtualenv && \
virtualenv /projects/vlim-telegram-bot.env && \
source /projects/vlim-telegram-bot.env/bin/activate && \
/projects/vlim-telegram-bot.env/bin/pip install -r /projects/vlim-telegram-bot/requirement.txt && \
cd /projects/vlim-telegram-bot
cp etc/init/vlim_bot.service /lib/systemd/system/
systemctl daemon-reload
systemctl enable vlim_bot.service