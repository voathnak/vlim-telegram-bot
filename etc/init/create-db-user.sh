#!/usr/bin/env bash
createuser --createdb --username postgres --no-createrole --superuser --pwprompt vlim
createuser --createdb --username vlim -P --no-createrole --superuser --pwprompt vlimbot
createdb vlim_bot
#GRANT ALL PRIVILEGES ON vlimbot  TO vlimbot;