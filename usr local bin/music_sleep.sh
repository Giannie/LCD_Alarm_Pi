#!/bin/bash

if [ -z $1 ]; then
    echo "Need Time"
    exit
fi
sleep $1
if [ "$(mpc | grep playing)"]
then
	mpc idle
fi
mpc stop
mpc clear
plug_off.sh
