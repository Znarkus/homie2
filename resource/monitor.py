from socket import *
from subprocess import Popen, PIPE
import re

s = socket(AF_INET, SOCK_DGRAM)
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
s.bind(('', 67))
m = s.recvfrom(1024)
hex_hex = m[0][28:34]
hex_string = ':'.join(hex(hex_hex[i])[2:] for i in range(0, 6))

print('Mac address:', hex_string)

pid = Popen(["arp", "-n", '-a'], stdout=PIPE)
s = pid.communicate()[0]
ip_address = re.search(r"\(([0-9\.]+)\) at " + hex_string, s.decode('ascii')).group(1)

print('IP address:', ip_address)