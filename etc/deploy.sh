#!/usr/bin/env bash
source /projects/vlim-telegram-bot.env/bin/activate && \
/projects/vlim-telegram-bot.env/bin/pip install -r /projects/vlim-telegram-bot/requirement.txt && \
git -C /projects/vlim-telegram-bot pull origin master && \
sudo service vlim_bot stop && \
sudo service vlim_bot start  && \
sudo service vlim_bot status
