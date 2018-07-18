#!/usr/bin/env bash
cd /projects/vlim-telegram-bot
git pull origin master
sudo service vlim_bot stop
sudo service vlim_bot start
sudo service vlim_bot status