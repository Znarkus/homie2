from tellcore.telldus import TelldusCore, DeviceFactory
import tellcore.telldus as td
from bottle import get, post, run, template, static_file
import tellcore.constants as const
import re
import threading
import time
from queue import Queue
import socket


config = {
    'transmitters': [
        {'house': 15323014, 'unit': 11}
    ]
}


def dim(device, level):
    print('Dimming', device.name, 'to', level)

    if (level == 0):
        device.turn_off()
    else:
        device.dim(int(level * 2.55))


def turn(device, mode):
    print('Turning', mode, device.name)

    if mode == 'on':
        device.turn_on()
    else:
        device.turn_off()


def turn_all(mode):
    for device in core.devices():
        turn(device, mode)


def dim_all(level):
    for device in core.devices():
        if device.methods(const.TELLSTICK_DIM):
            dim(device, level)
        else:
            if level >= 50:
                turn(device, 'on')
            else:
                turn(device, 'off')


def turn_lamp(lamp, mode):
    turn(DeviceFactory(lamp), mode)


def dim_lamp(lamp, level):
    dim(DeviceFactory(lamp), level)


@post('/all/<mode>')
def turn_all2(mode):
    for device in core.devices():
        turn(device, mode)


@post('/turn/<lamp:int>/<mode>')
def turn_lamp2(lamp, mode):
    turn(DeviceFactory(lamp), mode)


@post('/dim/<lamp:int>/<level:int>')
def dim_lamp2(lamp, level):
    dim(DeviceFactory(lamp), level)


@post('/dim/<level:int>')
def dim_all2(level):
    for device in core.devices():
        if device.methods(const.TELLSTICK_DIM):
            dim(device, level)
        else:
            if level >= 50:
                turn(device, 'on')
            else:
                turn(device, 'off')


@post('/remote/<mode>')
def remote2(mode):
    if mode == 'on':
        dim_all(75)
    else:
        turn_all('off')


@get('/')
def send_static():
    return static_file('index.html', root='www')
    # return template('index', devices=core.devices())


@get('/lib/<filename:path>')
def send_static2(filename):
    return static_file(filename, root='bower_components')


def raw_event(data, controller_id, cid):
    string = "[RAW] {0} <- {1}".format(controller_id, data)
    print(string)

    for transmitter in config['transmitters']:
        m = re.search('house:(\d+);unit:(\d+);group:\d+;method:turn(.+);', data)

        if m:
            house, unit, status = int(m.group(1)), int(m.group(2)), m.group(3)
            print(house, unit, status)

            if house == transmitter['house'] and unit == transmitter['unit']:
                print('MATCH!!!!')

                if status == 'on':
                    # dim_all(75)
                    work_queue.put(('dim_all', 75))
                else:
                    # turn_all('off')
                    work_queue.put(('turn_all', 'off'))

                print('Finished')


def queue_worker():
    # while not work_queue.empty():
    while True:
        command = work_queue.get()
        print('New command:', command)
        time.sleep(0.5)

        if command[0] == 'dim_all':
            dim_all(command[1])
        elif command[0] == 'turn_all':
            turn_all(command[1])

        work_queue.task_done()


# class PhonePing(threading.Thread):
#     def __init__(self):
#         super(PhonePing, self).__init__()
#         self.daemon = True
#
#     def run(self):
#         while True:
#             ip = ip_queue.get()
#             s = socket.socket()
#             s.settimeout(1)
#
#             try:
#                 s.connect((ip, 62078))
#                 print(time.ctime(), 'Ping Success')
#             except Exception as e:
#                 print(time.ctime(), 'Ping Failed:', e)
#
#             s.close()
#             ip_queue.task_done()
#             time.sleep(5)
#             ip_queue.put(ip)



try:
    import asyncio

    loop = asyncio.get_event_loop()
    dispatcher = td.AsyncioCallbackDispatcher(loop)
except ImportError:
    loop = None
    dispatcher = td.QueuedCallbackDispatcher()

# core = TelldusCore()
ip_queue = Queue()
ip_queue.put('10.0.0.73')

work_queue = Queue()
core = TelldusCore(callback_dispatcher=dispatcher)
callbacks = [core.register_raw_device_event(raw_event)]

web_thread = threading.Thread(target=run, kwargs={'host': '0.0.0.0', 'port': 8888})
web_thread.daemon = True

worker_thread = threading.Thread(target=queue_worker)
worker_thread.daemon = True

# phone_ping = PhonePing()

# run(host='0.0.0.0', port=8888)
try:
    web_thread.start()
    worker_thread.start()
    # phone_ping.start()

    # while web_thread.is_alive():
    # pass
    if loop:
        loop.run_forever()
    else:
        while True:
            core.callback_dispatcher.process_pending_callbacks()
            time.sleep(0.5)
except KeyboardInterrupt:
    pass
    # print('KeyboardInterrupt!')
    # web_thread.join()
    # print('Joined')