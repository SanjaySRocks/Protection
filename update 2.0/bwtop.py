#!/usr/bin/env python3
__author__ = 'Mahmoud Adel <mahmoud.adel2@gmail.com>'
__version__ = 0.7
__license__ = "The MIT License (MIT)"

'''
CLI tool to monitor network interfaces bandwidth rate.
'''

import argparse
import time
import curses
import os

#Setting cmd arguments
parser = argparse.ArgumentParser(prog='bwtop')
parser.add_argument('-i', '--interface', required=False)
parser.add_argument('-t', '--timeout',  type=int, required=False)
parser.add_argument('-d', '--disable-colors', action='store_false', help='Disable colored output "enabled by default"')
parser.add_argument('-s', '--single-output', action='store_false', help='Print the output single time and exit')
args = vars(parser.parse_args())

#Setting global vars
sortkeys = dict()
hostname = str()

#Checking arguments
interface = args['interface']
timeout = args['timeout']
disablecolorskipped = args['disable_colors']
singleoutskipped = 0

if interface == None:
    nic = ':'
else:
    nic = interface

if timeout != None and timeout > 0:
    hastimeout = True
else:
    hastimeout = False
    timeout = 1

#Setting functions
def checkOS():
    osdetails = tuple(os.uname())
    ostype = osdetails[0]
    global hostname
    hostname = osdetails[1]
    if ostype != 'Linux':
        exit("OS not Supported!")

def sleep(sec, pressedkey):
    if pressedkey < 0: 
        try:
            time.sleep(sec)
        except KeyboardInterrupt:
            curses.endwin()
            exit(0)

def getTraf(iface):
    rawstatus = list()
    destatus = dict()
    counter = 0
    matchediface = 0
    with open('/proc/net/dev') as f:
        for i in f:
            if iface in i:
                matchediface = matchediface + 1
                rawstatus.append(i.split())
                rcv = float(rawstatus[0][1])
                sent = float(rawstatus[0][9])
                counter = counter + rcv + sent
                destatus[rawstatus[0][0]] = {'rcv': rcv, 'sent': sent, 'total': rcv + sent}
                sortkeys[rawstatus[0][0]]= rcv + sent
                rawstatus = list()
    if matchediface == 0:
        curses.endwin()
        print('-i value should be "all" or a valid network interface')
        exit(2)
    statistics = [counter / 1024, destatus]
    return statistics

if not singleoutskipped:
    def main():
        checkOS()
        total ,data = getTraf(nic)
        time.sleep(1)
        newtotal ,newdata = getTraf(nic)
        traf = "%.2f" % (newtotal - total)
        for key in sorted(sortkeys, key=sortkeys.get, reverse=True):
            try:
                sent = "%.2f" % ((newdata[key]['sent'] - data[key]['sent']) / 1024)
                rcv = "%.2f" % ((newdata[key]['rcv'] - data[key]['rcv']) / 1024)
            except KeyError:
                sent = 0.00
                rcv = 0.00
            #print('{0}   Sent: {1}  Received: {2}'.format(key.ljust(15), sent, rcv))
        print('{0}'.format(traf))
else:
    def main():
        checkOS()
        stdscr = curses.initscr()
        curses.start_color()
        curses.use_default_colors()
        if not disablecolorskipped:
            curses.init_pair(1, -1, -1)
            curses.init_pair(2, -1, -1)
            curses.init_pair(3, -1, -1)
            curses.init_pair(4, -1, -1)
        else:
            curses.init_pair(1, curses.COLOR_MAGENTA, -1)
            curses.init_pair(2, curses.COLOR_BLUE, -1)
            curses.init_pair(3, curses.COLOR_GREEN, -1)
            curses.init_pair(4, curses.COLOR_YELLOW, -1)
        xdefault = 3
        x = xdefault
        stdscr.timeout(1)
        curses.noecho()
        while True:
            pressedkey = stdscr.getch()
            if pressedkey == ord('q'):
                 curses.endwin()
                 break
            total ,data = getTraf(nic)
            sleep(1, pressedkey)
            newtotal ,newdata = getTraf(nic)
            stdscr.clear()
            stdscr.border(0)
            timenow = time.strftime("%H:%M:%S")
            stdscr.addstr(1, 1, 'BWTop on: {0}     Time: {1}       Refresh every: {2}s'.format(hostname, timenow, timeout), curses.A_BOLD)
            for key in sorted(sortkeys, key=sortkeys.get, reverse=True):
                try:
                    sent = "%.2f" % ((newdata[key]['sent'] - data[key]['sent']) / 1024)
                    rcv = "%.2f" % ((newdata[key]['rcv'] - data[key]['rcv']) / 1024)
                except KeyError:
                    sent = 0.00
                    rcv = 0.00
                stdscr.addstr(x, 1, '{0}'.format(key), curses.color_pair(1))
                stdscr.addstr(x, 20, 'Sent:', curses.color_pair(2))
                stdscr.addstr(x, 26, '{0} KB'.format(sent), curses.color_pair(3))
                stdscr.addstr(x, 50, 'Received:', curses.color_pair(2))
                stdscr.addstr(x, 60, '{0} KB'.format(rcv), curses.color_pair(3))
                stdscr.refresh()
                x = x + 1
            traf = newtotal - total
            stdscr.addstr(x + 1, 1, 'Total:', curses.color_pair(4))
            stdscr.addstr(x + 1, 8, '{} KB/s'.format("%.2f" % traf), curses.color_pair(3))
            stdscr.refresh()
            x = xdefault
            sortkeys.clear()
            if hastimeout:
                sleep(timeout - 1, pressedkey)

#Calling main function
if __name__ == '__main__': main()
