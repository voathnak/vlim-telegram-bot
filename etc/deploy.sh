#!/usr/bin/env bash
git -C /home/vlim/projects/vlim-telegram-bot pull origin master && \
    sudo service vlim_bot stop && \
    sudo service vlim_bot start  && \
    sudo service vlim_bot status
