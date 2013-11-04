#!/bin/bash

if [ -z $1 ]; then
    echo "Need Time"
    exit
fi
sleep $1
mpc idle
mpc stop
mpc clear
plug_off.sh
