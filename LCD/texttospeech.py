#!/usr/bin/python

import urllib, pycurl, os

def downloadFile(url, fileName):
    fp = open(fileName, "wb")
    curl = pycurl.Curl()
    curl.setopt(pycurl.URL, url)
    curl.setopt(pycurl.WRITEDATA, fp)
    curl.perform()
    curl.close()
    fp.close()

def getGoogleSpeechURL(phrase):
    googleTranslateURL = "http://translate.google.com/translate_tts?tl=en&"
    parameters = {'q': phrase}
    data = urllib.urlencode(parameters)
    googleTranslateURL = "%s%s" % (googleTranslateURL,data)
    return googleTranslateURL

def speakSpeechFromText(phrase):
    googleSpeechURL = getGoogleSpeechURL(phrase)
    downloadFile(googleSpeechURL,"/tmp/tts.mp3")
   
def play_file(phrase):
    speakSpeechFromText(phrase)
    os.system("mplayer /tmp/tts.mp3 -nocache 2>&1")