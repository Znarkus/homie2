import socket
from subprocess import Popen, PIPE
import re
import threading
import time


class PhonePing(threading.Thread):
    def __init__(self, ip_address):
        super(PhonePing, self).__init__()
        self.daemon = True
        self.ip_address = ip_address

    def run(self):
        while True:
            s = socket.socket()
            s.settimeout(5)
            start = time.time()

            # print(['nmap', '-PN', self.ip_address])
            # pid = Popen(['nmap', '-PN', self.ip_address], stdout=PIPE)
            # s = pid.communicate()[0]
            # nmap_output = s.decode('ascii')
            # print(nmap_output)
            #
            # if 'Host is up.' in nmap_output:
            #     print(time.ctime(), 'Ping Success')
            # else:
            #     print(time.ctime(), 'Ping Failed')

            try:
                s.connect((self.ip_address, 62078))
                print(time.ctime(), 'Ping Success')
            except Exception as e:
                # print(time.ctime(), 'Ping Failed:', e)
                pass

            s.close()

            elapsed = time.time() - start

            if elapsed > 0 and elapsed < 5:
                time.sleep(5 - elapsed)


def disc_detect():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.bind(('', 67))

    m = s.recvfrom(1024)
    hex_hex = m[0][28:34]
    mac_string = ':'.join(hex(hex_hex[i])[2:] for i in range(0, 6))

    print('Mac address:', mac_string)

    if mac_string in mac_addresses:
        while True:
            pid = Popen(["arp", "-n", '-a'], stdout=PIPE)
            s = pid.communicate()[0]
            arp_output = s.decode('ascii')

            print('ARP:\n', arp_output)

            regex_search = re.search(r"\(([0-9\.]+)\) at " + mac_string, arp_output)

            if regex_search:
                break

        ip_address = regex_search.group(1)

        print('IP address:', ip_address)

        # if workers[mac_string]:

        workers[mac_string] = PhonePing(ip_address)
        workers[mac_string].start()

mac_addresses = ['90:8d:6c:ce:42:85']
workers = {}

try:
    while True:
        disc_detect()
except KeyboardInterrupt:
    pass
