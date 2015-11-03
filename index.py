from tellcore.telldus import TelldusCore
from bottle import get, post, run, template, static_file

core = TelldusCore()
lamps = {
    'taklampor': core.add_device("Taklampor", "arctech", "selflearning-dimmer", house=13, unit=1),
    'byra': core.add_device("Byrå", "arctech", "selflearning-dimmer", house=21079520, unit=1),
    'bordslampor': core.add_device("Bordslampor", "arctech", "selflearning-switch", house=12345, unit=11)
}

# lamp.turn_on()
# lamp2.turn_on()
# lamp3.turn_on()
#
# for device in core.devices():
#     device.turn_off()

@post('/all/<mode>')
def turn_all(mode):
    for device in core.devices():
        if mode == 'on':
            device.turn_on()
        else:
            device.turn_off()

    # return ''

@post('/turn/<lamp>/<mode>')
def turn_lamp(lamp, mode):
    if mode == 'on':
        lamps[lamp].turn_on()
    else:
        lamps[lamp].turn_off()

    # return ''

@get('/')
def send_static():
    return static_file('index.html', root='www')

@get('/lib/<filename:path>')
def send_static(filename):
    return static_file(filename, root='bower_components')

run(host='localhost', port=8888)