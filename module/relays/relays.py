#!/usr/bin/env python3.7
import RPi.GPIO as GPIO
import time
import random
import yaml
import datetime
import threading
import sys
import atexit

GPIO.cleanup()
ON = GPIO.LOW
OFF = GPIO.HIGH

def loadConfig():
    with open("/home/pi/relays/module/relays/config.yml", "r") as stream:
        try:
            relays = yaml.safe_load(stream)
            return relays
        except yaml.YAMLError as exc:
            print(exc)
            return None

class Relays:
    def __init__(self):
        self.relays = loadConfig()
        pinList = [r["pin"] for r in self.relays]

        GPIO.setmode(GPIO.BCM)
        # init list with pin numbers
        m_pin = 21
        GPIO.setup(m_pin, GPIO.OUT)
        GPIO.setup(pinList, GPIO.OUT)
        GPIO.output(pinList, GPIO.HIGH)
        GPIO.output(m_pin, GPIO.HIGH)
        self.runLoop = True



        GPIO.setup(pinList, GPIO.OUT)

    def go(self):
        # try:
        minute = 0
        while self.runLoop:
            if not minute == datetime.datetime.now().minute:
                print("-------------------------------------------")
                print(datetime.datetime.now().strftime("%H:%M:%S"))
                self._removeExpiredOverrides()
                self.process()

                print("Overrides: {}".format([r.get("override", None) for r in self.relays]))
                minute = datetime.datetime.now().minute
            time.sleep(1)



    def process(self):
        now = int(datetime.datetime.now().strftime("%H%M"))
        for i in self.relays:
            i["state"] = GPIO.input(i['pin'])
            if "override" in i:
                print("Relay {} is in override it is {}".format(i["name"], i["state"]))
                continue
            
            for event in i.get("events", []):
                if int(event['start']) < now and int(event['end']) > now:
                    print("turn {} on".format(i["name"]))
                    GPIO.output(i["pin"], ON)
                    break
            else:    #when no for break occurs
                print("turn {} off".format(i["name"]))
                GPIO.output(i["pin"], OFF)


            i['state'] = GPIO.input(i['pin'])
            
            #GPIO.input(i['pin']) This gives the current state of the pin 0 is on 1 is off


    def _removeExpiredOverrides(self):
        now = datetime.datetime.now()
        for r in self.relays:
            if now > r.get("override", now ):
                print("Override expired on {}".format(r["name"]))
                r.pop("override")

    def _isOn(self, relay_obj):
        pin = relay_obj['pin']
        raw = GPIO.input(pin)
        if relay_obj.get('inverted', False):
            raw = not raw
        if raw == 0:
            return True
        else:
            return False

    def override(self, relay, minutes=30):
        self.relays[relay]['override'] = datetime.datetime.now() + datetime.timedelta(minutes=minutes)

    def toggle(self, relay):
        self.override(relay)
        pin = self.relays[relay]["pin"]
        GPIO.output(pin, not GPIO.input(pin))

    def on(self, relay):
        self.override(relay)
        pin = self.relays[relay]["pin"]
        GPIO.output(pin, ON)
        print("Turn on {}".format(relay))


    def off(self, relay):
        self.override(relay)
        pin = self.relays[relay]["pin"]
        GPIO.output(pin, OFF)
        print("Turn off {}".format(relay))

    def status(self):
        statuses = []
        index = 0
        for r in self.relays:
            override = r.get("override", "")
            status = {
                "name": r['name'],
                "is_on": self._isOn(r),
                "index": index,
                "override": r.get("override", ""),

            }
            print(status['override'])
            index = index + 1
            statuses.append(status)
        return statuses


    def quit(self):
            print("cleanup gpio")
            self.runLoop = False
            time.sleep(1)
            GPIO.cleanup()


def start():
    t.start()
    time.sleep(1)

def end():
    rrrr.quit()
    t.join()

def get_relays():
    return rrrr

def main():
    start()


rrrr = Relays()
t = threading.Thread(target=rrrr.go, name="Relay Thread", args=[])

if __name__ == '__main__':
    t = threading.Thread(target=rrrr.go, name="Relay Thread", args=[])
    t.start()
    time.sleep(1)

    #user input loop
    running=True
    while running:
        print(running)
        try:
            userInput = input("Enter a relay to override")
            rrrr.status()
            rrrr.override(int(userInput))
        except KeyboardInterrupt:
            print("Quitting input loop")
            running=False
            rrrr.quit()
            t.join()
            


        

