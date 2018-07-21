#!/usr/bin/env bash

adduser vlim
usermod -aG sudo vlim
su - vlim
mkdir /projects
cd /projects/
git clone git@bitbucket.org:v-lim/vlim-telegram-bot.git
cd vlim-telegram-bot/
apt-get install virtualenv
virtualenv /projects/vlim-telegram-bot.env -p python3
virtualenv /projects/vlim-telegram-bot.env -p python3
python -V
which python
which python3
apt-get install python-pip
/projects/vlim-telegram-bot.env/bin/pip install -r /projects/vlim-telegram-bot/requirement.txt
cp etc/init/vlim_bot.service /lib/systemd/system/
systemctl daemon-reload
systemctl enable vlim_bot.service
ls -la /lib/systemd/system/
systemctl daemon-reload


ip addr show ens4 | grep inet | awk '{ print $2; }' | sed 's/\/.*$//'
createuser --createdb --username postgres -P --no-createrole --superuser --pwprompt vlimbot



cd /projects/vlim-telegram-bot && \
git reset --hard origin/master && \
git pull origin master && \
source /projects/vlim-telegram-bot.env/bin/activate && \
sudo service vlim_bot stop && sudo service vlim_bot start && tail -f /logs/vlim-bot.log
