#!/usr/bin/python3
import subprocess
import time

import pyttsx3


def read_track_or_playlist(track=True):
    status = subprocess.check_output('qdbus --system org.bluez  ' + player + ' org.bluez.MediaPlayer1.Status',
                                     shell=True)

    if status.decode("utf-8").strip('\n') == 'playing':
        print('It\'s playing!')

        now_playing = subprocess.check_output(
            ' qdbus --system org.bluez  ' + player + ' org.bluez.MediaPlayer1.Track',
            shell=True)

        now_playing_list = list(filter(None, now_playing.decode("utf-8").split('\n')))
        # create a dictionary with now playing details (album, artist, etc..)
        details = {detail.split(': ')[0]: detail.split(':')[1] for detail in now_playing_list}
        artist_and_title = details['Title'] + '.' + '  . From .  ' + details['Artist']
        print(artist_and_title)

        engine = pyttsx3.init()
        rate = engine.getProperty('rate')
        engine.setProperty('rate', rate - 30)
        volume = engine.getProperty('volume')
        engine.setProperty('volume', volume + 0.5)
        engine.setProperty('voice', 'english+f2')
        engine.say(artist_and_title)
        engine.runAndWait()
    else:
        print('Not playing!')


def next_track(channel):
    command_output = subprocess.check_output(
        'qdbus --system org.bluez  ' + player + ' org.bluez.MediaPlayer1.Next',
        shell=True)
    print(command_output.decode("utf-8"))

    # TODO - apresenta informacao atrasada

    now_playing = subprocess.check_output(
        ' qdbus --system org.bluez  ' + player + ' org.bluez.MediaPlayer1.Track',
        shell=True)

    now_playing_list = list(filter(None, now_playing.decode("utf-8").split('\n')))
    # create a dictionary with now playing details (album, artist, etc..)
    details = {detail.split(': ')[0]: detail.split(':')[1] for detail in now_playing_list}
    print("Next track..")
    print("Now playing", details['Title'], "by", details['Artist'])


def previous_track(channel):
    command_output = subprocess.check_output(
        'qdbus --system org.bluez  ' + player + ' org.bluez.MediaPlayer1.Previous',
        shell=True)
    print(command_output.decode("utf-8"))

    # TODO - apresenta informacao atrasada
    now_playing = subprocess.check_output(
        ' qdbus --system org.bluez  ' + player + ' org.bluez.MediaPlayer1.Track',
        shell=True)

    now_playing_list = list(filter(None, now_playing.decode("utf-8").split('\n')))
    # create a dictionary with now playing details (album, artist, etc..)
    details = {detail.split(': ')[0]: detail.split(':')[1] for detail in now_playing_list}
    print("Previous track..")
    print("Now playing", details['Title'], "by", details['Artist'])


def toggle_play(channel):
    status = subprocess.check_output(
        'qdbus --system org.bluez  ' + player + ' org.bluez.MediaPlayer1.Status',
        shell=True)

    if status.decode("utf-8").strip('\n') == 'playing':
        print('It\'s playing, let\'s pause!')
        command_output = subprocess.check_output(
            'qdbus --system org.bluez  ' + player + ' org.bluez.MediaPlayer1.Pause',
            shell=True)
        print(command_output.decode("utf-8"))
    else:
        print('It\'s paused!, let\'s play!')
        command_output = subprocess.check_output(
            'qdbus --system org.bluez  ' + player + ' org.bluez.MediaPlayer1.Play',
            shell=True)
        print(command_output.decode("utf-8"))


def shutdown(channel):
    engine = pyttsx3.init()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate - 30)
    volume = engine.getProperty('volume')
    engine.setProperty('volume', volume + 2)
    engine.setProperty('voice', 'english+f2')
    engine.say("Shutting down")
    engine.runAndWait()

    subprocess.check_output(
        'shutdown -t now',
        shell=True)


engine = pyttsx3.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', rate - 30)
volume = engine.getProperty('volume')
engine.setProperty('volume', volume + 2)
engine.setProperty('voice', 'english+f2')

import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

# Setup dos botoes the input
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# GPIO.add_event_detect(15, GPIO.RISING, callback=double_click, bouncetime=500)
GPIO.add_event_detect(13, GPIO.RISING, callback=next_track, bouncetime=500)
GPIO.add_event_detect(11, GPIO.RISING, callback=toggle_play, bouncetime=500)
GPIO.add_event_detect(7, GPIO.RISING, callback=previous_track, bouncetime=500)

player = None

import bluetooth
import subprocess as sp
i = 0
while player is None:
    try:
        stdoutdata = sp.getoutput("hcitool con")

        if 'CC:21' not in stdoutdata:
            s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            s.connect(('XX:XX:XX:XX:XX:XX', 2))

        player = subprocess.check_output(
            'qdbus --system org.bluez  | grep player',
            shell=True).decode("utf-8").strip()

        command_output = subprocess.check_output(
            'qdbus --system org.bluez  ' + player + ' org.bluez.MediaPlayer1.Play',
            shell=True)

        engine.say("Connect to, 0")
        engine.runAndWait()

        read_track_or_playlist()

    except Exception as e:
        print('Not connected, trying again in 5 seconds..')
        time.sleep(1)
        print('Trying again..')
        if (i == 0) or (i%5 == 0):
            engine.say("I'm ready!")
            engine.runAndWait()
        i += 1

print(player)

new = False

subprocess.check_output('qdbus --system org.bluez  ' + player + ' org.bluez.MediaPlayer1.Play', shell=True)
while True:

    if GPIO.input(15) == 1:
        started_check = time.time()
        red_counter = 1
        got_zero = False
        while True:
            time.sleep(0.2)
            if GPIO.input(15) == 0:
                got_zero = True
                print("Got zero")
            elif GPIO.input(15) == 1 and got_zero:
                red_counter += 1
                print("Got one")
                got_zero = False
            if time.time() - started_check > 1:
                print("Timeout")
                # engine.say(red_counter)
                if red_counter == 1:
                    read_track_or_playlist()
                else:
                    print("TODO1")
                engine.runAndWait()
                red_counter = 0
                break
