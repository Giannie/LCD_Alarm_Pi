#!/usr/bin/python

import alarm_time
import texttospeech

forecast = alarm_time.Forecast(0)

texttospeech.speakSpeechFromText(forecast.full_report1)
texttospeech.speakSpeechFromText(forecast.full_report2)