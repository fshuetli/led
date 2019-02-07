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
        print("\n\nhallloooo")
        print(thing.name)
        print("giiga:")
        if isinstance(thing, threading._Timer):
            thing.cancel()


# Cancel all pre-existing timers
def clear_named_timers(x):
    for thing in threading.enumerate():
        if isinstance(thing, threading._Timer):
            if thing.name == x:
                thing.cancel()


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
    clear_all_timers()
    set_led_off()
    return "", 200

def named_timer(name, interval, function, *args, **kwargs):
    """Factory function to create named Timer objects.

      Timers call a function after a specified number of seconds:

          t = Timer('Name', 30.0, function)
          t.start()
          t.cancel()  # stop the timer's action if it's still waiting
    """
    timer = _Timer(interval, function, *args, **kwargs)
    timer.name = name
    return timer

# What's done when API /led post (on) is called
def ein():
    # Get params of post body
    #passw = params.get("passw", None)
    #minutes = params.get("minutes", None)
    minutes = 1

    # Check Passw
    if True:
        # Turn on Light
        set_led_on()
        # Set of new timer
        clear_all_timers()
        #a = Timer(int(minutes)*60, set_led_off, ()).start()
        a = named_timer("asdf" ,int(minutes)*60, set_led_off, ())
        #a.name = "asdf"
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
ein()
aus()

