#!/bin/bash

if [ -z "$(ifconfig wlan0 | grep "inet addr")" ]
then
	ifup —-force wlan0
fi
