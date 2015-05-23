import os
import socket
import re
import fcntl
import struct
import platform

#ADDR_REGEX = '\(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])'
#HOST_REGEX = '(?:(?:(?:(?:[a-zA-Z0-9][-a-zA-Z0-9]*)?[a-zA-Z0-9])[.])*(?:[a-zA-Z][-a-zA-Z0-9]*[a-zA-Z0-9]|[a-zA-Z])[.]?)'
HOST_REGEX = '(?:(?:(?:(?:[a-zA-Z0-9][-a-zA-Z0-9]{0,61})?[a-zA-Z0-9])[.])*(?:[a-zA-Z][-a-zA-Z0-9]{0,61}[a-zA-Z0-9]|[a-zA-Z])[.]?)'

addrregex = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
#addrregex = re.compile(ADDR_REGEX)
hostregex = re.compile(HOST_REGEX)

hostmap = {}

def getinterfaceip(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s',
                                ifname[:15]))[20:24])

def getlanip():
    ip = socket.gethostbyname(socket.gethostname())
    if ip.startswith("127."):
        interfaces = [
            "eth0",
            "eth1",
            "eth2",
            "wlan0",
            "wlan1",
            "wifi0",
            "ath0",
            "ath1",
            "ppp0",
            ]
        for ifname in interfaces:
            try:
                ip = getinterfaceip(ifname)
                break
            except IOError:
                pass
    return ip

def findaddrs(line):
  res = []
  addrs = re.findall(addrregex, line)
  for addr in addrs:
    if isvalidaddr(addr) == True and ispublic(addr) == True:
      res.append(addr)
  return res

def findhosts(line):
  res = []
  hosts = re.findall(hostregex, line)
  for host in hosts:
    if isvalidhost(host) == True:
      res.append(host)
  return res

def isvalidaddr(addr):
  try:
    socket.inet_aton(addr)
    return True
  except socket.error:
    return False

def isvalidhost(hostname):
  if hostname.find('.') == -1:
    return False
  #TODO: implement some easy rules to filter out the obvious invalid ones
  if hostname in hostmap:
    return hostmap[hostname]
  try:
    h = socket.gethostbyname(hostname)
    #127.0.53.53 is a special IP addresses that is used by ICANN to prevent DNS name collitions with the new gTLDs.
    if h == '127.0.53.53' or h == '198.105.254.228':
      hostmap[hostname] = False
      return False
    hostmap[hostname] = True
    return True  
  except socket.error:
    hostmap[hostname] = False
    return False

def ispublic(addr):
  #TODO
  return True

#print platform.node()
#print socket.gethostname()
#print getlanip()
