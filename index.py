from tellcore.telldus import TelldusCore, DeviceFactory
from bottle import get, post, run, template, static_file
import tellcore.constants as const

core = TelldusCore()

def dim(device, level):
    if (level == 0):
        device.turn_off()
    else:
        device.dim(int(level * 2.55))

def turn(device, mode):
    if mode == 'on':
        device.turn_on()
    else:
        device.turn_off()

@post('/all/<mode>')
def turn_all(mode):
    for device in core.devices():
        turn(device, mode)

@post('/turn/<lamp:int>/<mode>')
def turn_lamp(lamp, mode):
    turn(DeviceFactory(lamp), mode)

@post('/dim/<lamp:int>/<level:int>')
def turn_lamp(lamp, level):
    dim(DeviceFactory(lamp), level)

@post('/dim/<level:int>')
def dim_all(level):
    for device in core.devices():
        if device.methods(const.TELLSTICK_DIM):
            dim(device, level)
        else:
            if level >= 50:
                turn(device, 'on')
            else:
                turn(device, 'off')

@get('/')
def send_static():
    return static_file('index.html', root='www')
    # return template('index', devices=core.devices())

@get('/lib/<filename:path>')
def send_static(filename):
    return static_file(filename, root='bower_components')

run(host='0.0.0.0', port=8888)