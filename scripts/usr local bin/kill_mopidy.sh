if [ "$(pgrep -f mopidy)" ]; then
	sudo kill "$(pgrep -f mopidy)"
fi