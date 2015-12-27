import socket
s = socket.socket()
s.settimeout(1)

try:
    s.connect(('10.0.0.73', 62078))
    print('Success')
except Exception as e:
    print('Failed')