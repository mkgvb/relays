from django.http import HttpResponse
from django.shortcuts import render, redirect
from relays import relays
import json
import atexit

    
r = relays.get_relays()
def exit_handler():
    relays.end()

relays.start()
atexit.register(exit_handler)



def get_status():
    relays = {}
    relays['relays'] = []
    relays['relays'] = r.status()
    return relays

def index(request, relay_id=None):
    #return HttpResponse("Hello, world. You're at the polls index. %s" % json.dumps(text, indent=4))
    return render(request, 'index.html', context=get_status())

def detail(request, relay_id):
    return HttpResponse("You're looking at relay %s." % relay_id)

def on(request, relay_id):
    r.on(relay_id)
    return HttpResponse("You're turning on relay %s." % relay_id)

def off(request, relay_id):
    r.off(relay_id)
    #r.override(question_id)
    return HttpResponse("You're turning off relay %s." % relay_id)

def toggle(request, relay_id):
    r.toggle(relay_id)
    return redirect('/')
    