############################################################################
# Basic Protection Script to Protect You GameServer Against DDoS Attacks
# Author: Sanjay Singh
# Version: 2.1
# firewall.py
# github.com/SanjaySRocks
############################################################################

import subprocess
from datetime import datetime
import bwtop
import time



ipFilePath = [ 
    "iplogs.txt",
    "iplogs2.txt"
]

ips = str()

for i in range(len(ipFilePath)):
    with open (ipFilePath[i], "r") as f:
        ips += f.read() + ','

ips = ips[0:-1]


gtips="208.167.241.190,208.167.241.185,208.167.241.186,208.167.241.183,208.167.241.189,108.61.78.147,108.61.78.148,108.61.78.149,108.61.78.150"


flush_rules = [
    "iptables -F",
	"iptables -X",
	"iptables -t nat -F",
	"iptables -t nat -X",
	"iptables -t mangle -F",
	"iptables -t mangle -X",
	"iptables -P INPUT ACCEPT",
	"iptables -P FORWARD ACCEPT",
	"iptables -P OUTPUT ACCEPT"
]

block_rules = [
	f"iptables -A INPUT -s {ips} -j ACCEPT",
	f"iptables -A INPUT -s {gtips} -j ACCEPT",
	"iptables -A INPUT -p tcp --dport 22 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT",
	"iptables -P INPUT DROP",
	"iptables -P FORWARD DROP"
]


def flush():
    for x in flush_rules:
        subprocess.run(x, shell=True, 
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def block():
    for x in block_rules:
        subprocess.run(x, shell=True,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    while True:
        bw = int(bwtop.main())
        if bw < 4000:
            continue
        else:
            printx(f"{bw} KB/s Incoming DDoS BLOCKED | [ BLOCKED ]")
            block()
            time.sleep(10)
            printx(f"Allowing Traffic | [ FLUSHED ]")
            flush()
            continue


def printx(text):
    now = datetime.now()
    curtime = now.strftime("%d.%m.%Y - %H:%M:%S")

    with open('ddos.log','a') as f:
        text = f"Time: {curtime} || " + text
        print(text)
        f.write("\n"+text)


if __name__ == "__main__":
    main()