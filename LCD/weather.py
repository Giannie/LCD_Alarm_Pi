import subprocess
import re
import sys
import texttospeech
from mpd import MPDClient
import alarm_time

forecast = alarm_time.Forecast(0)

client = MPDClient()
client.timeout = 10
client.idletimeout = None
client.connect("localhost",6600)


def current_track(client):
    status = client.status()
    return [status['song'],status['playlistlength']]

def add_weather_tracks(client):
    client.add('tts.mp3')
#    client.add('tts.mp3')

def move_weather_tracks(client):
    current = current_track(client)
    client.move(int(current[1])-1,current[0])
#    client.move(int(current[1])-1,current[0])


add_weather_tracks(client)
move_weather_tracks(client)
client.setvol(90)
client.random(0)
current = current_track(client)
texttospeech.speakSpeechFromText(forecast.full_report1)
client.play(int(current[0])-1)
client.idle()
client.idle()
client.pause()
texttospeech.speakSpeechFromText(forecast.full_report2)
client.previous()
client.idle()
client.idle()
client.setvol(85)
client.random(1)

client.close()
client.disconnect()