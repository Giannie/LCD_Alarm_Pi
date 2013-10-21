#!/bin/sh

python LCD_Alarm_Pi/playlist.py
tr '\r' '\n' < AlarmPlaylist.m3u > AlarmPlaylistTmp.m3u
mv AlarmPlaylistTmp.m3u AlarmPlaylist.m3u
sudo mv AlarmPlaylist.m3u /var/lib/mpd/playlists
sudo chown mpd /var/lib/mpd/playlists/AlarmPlaylist.m3u
sudo chgrp audio /var/lib/mpd/playlists/AlarmPlaylist.m3u