#!/usr/bin/env bash

cd /home/vlim/projects/vlim-telegram-bot
sudo cp etc/init/vlim_bot.service /lib/systemd/system/
systemctl daemon-reload
systemctl enable vlim_bot.service