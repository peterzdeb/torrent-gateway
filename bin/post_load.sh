#!/usr/bin/env bash

PROD_ROOT=/home/transmission/torrent-gateway
export PROD_ROOT
exec `python3.4 $PROD_ROOT/src/python/bin/post_load.py 2>> /var/log/torrent_gw.log`
