"""
This is the led module and supports all the ReST actions for the
led collection


 sudo pip install --upgrade pip
 sudo pip install flask
 sudo pip install connexion
 sudo pip install RPi.GPIO

"""

# System modules
from datetime import datetime

# 3rd party modules
from flask import make_response, abort
import hashlib
from threading import Timer
import threading

# Import gpio methods
from gpio import *

# Cancel all pre-existing timers
def clear_all_timers():
    for thing in threading.enumerate():
        if isinstance(thing, threading._Timer):
            thing.cancel()

# Check if allowed
def check_permission(passw, minutes):
    if (len(passw) < 20 and len(minutes) < 3 and int(minutes) < 20):
        if "452504d58348a5ea316a2f0d417999d4" == hashlib.md5(passw).hexdigest():
            return True
        else:
            return False
    else:
        return False

# What's done when API /led get (off) is called
def aus():
    clear_all_timers()
    set_led_off()
    return "", 200

# What's done when API /led post (on) is called
def ein(params):
    # Get params of post body
    passw = params.get("passw", None)
    minutes = params.get("minutes", None)

    # Check Passw
    if check_permission(passw, minutes):
        # Turn on Light
        set_led_on()
        # Set of new timer
        clear_all_timers()
        Timer(int(minutes)*60, set_led_off, ()).start()
        # Return API response
        return "", 201
    else:
        # Don't do anything
        print("Passwort war falsch. Schalte Licht nicht ein.")
        no_set_led()
        abort(
            406,
            "",
        )

# initially turn of
aus()

