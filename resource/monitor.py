import socket
from subprocess import Popen, PIPE
import re
import threading
import time
import argparse


class PhonePing(threading.Thread):
    def __init__(self, ip_address):
        super(PhonePing, self).__init__()
        self.daemon = True
        self.ip_address = ip_address

    def run(self):
        lost_since = None   # None == Not lost. Number == time that we lost phone.
        record_lost_time = 0
        at_home = None

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
            # print(time.ctime(), 'Ping Success')
            # else:
            #     print(time.ctime(), 'Ping Failed')

            try:
                s.connect((self.ip_address, 62078))
                # print(time.ctime(), 'Ping Success')

                if lost_since:
                    lost_time = round(time.time() - lost_since)
                    lost_since = None

                    if lost_time > record_lost_time:
                        record_lost_time = lost_time

                    print(time.ctime(), '- Found again after', lost_time, 'seconds (Record:', record_lost_time, 'seconds)')

                    if at_home == False:
                        print('Home again')

                    at_home = True

            except Exception as e:
                # print(time.ctime(), 'Ping Failed:', e)
                if not lost_since:
                    print(time.ctime(), '- Lost')
                    lost_since = time.time()

                elif at_home and time.time() - lost_since > 3000:
                    print('Left home')
                    at_home = False

            s.close()
            elapsed = time.time() - start

            if 0 < elapsed < 5:
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


parser = argparse.ArgumentParser()
parser.add_argument('--ip', help='list of IP addresses', nargs='*')
parser.add_argument('--mac', help='list of MAC addresses', nargs='*', default=[])
args = parser.parse_args()

if args.ip:
    workers = []

    for ip in args.ip:
        worker = PhonePing(ip)
        worker.start()
        workers.append(worker)

    try:
        while True:
            pass
    except KeyboardInterrupt:
        pass

else:
    # mac_addresses = ['90:8d:6c:ce:42:85']
    workers = {}
    mac_addresses = args.mac

    try:
        while True:
            disc_detect()
    except KeyboardInterrupt:
        pass
