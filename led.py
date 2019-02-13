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
from threading import _Timer

# Import gpio methods
from gpio import *

# Cancel all pre-existing timers
def clear_all_timers():
    for thing in threading.enumerate():
        #print("\n\nhallloooo")
        #print(thing.name)
        #print("giiga:")
        if isinstance(thing, threading._Timer):
            thing.cancel()


# Cancel all pre-existing timers matching a name
def clear_named_timers(x):
    for thing in threading.enumerate():
        if isinstance(thing, threading._Timer):
            if thing.name == x:
                thing.cancel()

def named_timer(name, interval, function, *args, **kwargs):
    timer = _Timer(interval, function, *args, **kwargs)
    timer.name = name
    return timer

# Check if allowed
def check_permission(passw, minutes):
    if (len(passw) < 16 and len(minutes) < 3 and int(minutes) < 61):
        if "452504d58348a5ea316a2f0d417999d4" == hashlib.md5(passw).hexdigest() or "0e1c46abe6015f039d3be387b616a6b1" == hashlib.md5(passw).hexdigest():
            return True
        else:
            return False
    else:
        return False

# What's done when API /led get (off) is called
def aus():
    clear_named_timers("vorn")
    set_led_on_index(0)
    return "", 200


# What's done when API /led post (on) is called
def ein(params):
    # Get params of post body
    passw = params.get("passw", None)
    minutes = params.get("minutes", None)

    # Check Passw
    if check_permission(passw, minutes):
        # Turn on Light
        set_led_on_index(0)
        # Set of new timer
        clear_named_timers("vorn")
        a = named_timer("vorn" ,int(minutes)*60, set_led_off_index, args=[0])
        a.start()
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

# What's done when API /led get (off) is called
def aus2():
    clear_named_timers("wald")
    set_led_off_index(1)
    return "", 200


# What's done when API /led post (on) is called
def ein2(params):
    # Get params of post body
    passw = params.get("passw", None)
    minutes = params.get("minutes", None)

    # Check Passw
    if check_permission(passw, minutes):
        # Turn on Light
        set_led_on_index(1)
        # Set of new timer
        clear_named_timers("wald")
        a = named_timer("vorn" ,int(minutes)*60, set_led_off_index, args=[1])
        a.start()
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

