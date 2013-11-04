#!/bin/bash

if [ -z "$(ls /mnt/raspbmc/02611632-508e-42a3-9d69-566bdca87be8/)" ]
then 
	sudo mount -a
fi