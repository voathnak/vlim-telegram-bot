#!/usr/bin/env bash
createuser --createdb --username vlim --no-createrole --superuser --pwprompt vlimbot
createdb vlim_bot