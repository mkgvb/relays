#!/usr/bin/env python3.7
import RPi.GPIO as GPIO
import time
import random
import yaml
import datetime
import pprint

ON = GPIO.LOW
OFF = GPIO.HIGH

def loadConfig():
    with open("config.yml", "r") as stream:
        try:
            relays = yaml.safe_load(stream)
            return relays
        except yaml.YAMLError as exc:
            print(exc)
            return None

class Relays:
    def __init__(self):
        self.relays = loadConfig()
        pp = pprint.PrettyPrinter(indent=4)
        pinList = [r["pin"] for r in self.relays]

        GPIO.setmode(GPIO.BCM)
        # init list with pin numbers
        m_pin = 21
        GPIO.setup(m_pin, GPIO.OUT)
        GPIO.setup(pinList, GPIO.OUT)
        GPIO.output(pinList, GPIO.HIGH)
        GPIO.output(m_pin, GPIO.HIGH)




        GPIO.setup(pinList, GPIO.OUT)

        try:
            while True:
                self._removeExpiredOverrides()
                print(datetime.datetime.now().strftime("%H:%M:%S"))
                self.process()


                print([r["state"] for r in self.relays])
                print("Overrides: {}".format([r.get("override", None) for r in self.relays]))
                pp.pprint(self.relays)
                # wait until the first second of the next minute
                time.sleep(61 - datetime.datetime.now().second)
        except KeyboardInterrupt:
            print("keyboard quit")
        finally:
            print("cleanup gpio")
            GPIO.cleanup()

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
                GPIO.output(i["pin"], OFF)

            i['state'] = GPIO.input(i['pin'])
            print(GPIO.input(i['pin']))


    def _removeExpiredOverrides(self):
        now = datetime.datetime.now()
        for r in self.relays:
            if now > r.get("override", now ):
                print("Override expired on {}".format(r["name"]))
                r.pop("override")


    def override(self, relay, minutes=30):
        self.toggle(relay)
        self.relays[relay]['override'] = datetime.datetime.now() + datetime.timedelta(minutes=minutes)

    def toggle(self, relay):
        pin = self.relays[relay]["pin"]
        GPIO.output(pin, not GPIO.input(pin))


rrrr = Relays()


