#!/usr/bin/env bash


sudo cp init/vlim_bot.service /lib/systemd/system/
systemctl daemon-reload
systemctl enable vlim_bot.service