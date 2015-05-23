#!/usr/bin/python

import os
import sys
import getopt
import re
import time
import addrnhost
from usrgrp import getusrgrpnames 

DEBUG = 1

addrpfx = '$IP_ADDRESS'
addrcnt = 1
addrmap = {}

hostpfx = '$HOST_NAME'
hostcnt = 1
hostmap = {}

maxstrlen = 0

def check(inputfile, outputfile):
  """
  Check if the input and output files are good
  """
  try:
    open(inputfile, 'r')
  except IOError as e:
    print 'Cannot open the input file: ', e
    return False
  try:
    open(inputfile, 'r')
  except IOError as e:
    print 'Cannot open the output file: ', e
    return False
  return True

def anonymize(inputfile, outputfile):
  ins = open(inputfile, 'r')
  ous = open(outputfile, 'w')
  for l in ins:
    #print l
    
    #Handle ip addresses
    addrs = addrnhost.findaddrs(l) 
    if len(addrs) != 0:
      if DEBUG:
        print 'Find IP address: ', addrs
      for addr in addrs:
        naddr = replace(addr, addrpfx, addrcnt, addrmap)
        l = l.replace(addr, naddr)

    #Handle hostname
    hosts = addrnhost.findhosts(l)
    if len(hosts) != 0:  
      if DEBUG:
        print 'Find host names: ', hosts
      for host in hosts:
        nhost = replace(host, hostpfx, hostcnt, hostmap)
        l = l.replace(host, nhost)
    
    if l.count('/') > 1:
      print 'Contain files: ', l
   
    #names = getusrgrpnames()
    #for name in names:
    #  if l.find(name) != -1:
    #    print name, '|',  l
    ous.write(l)

  ins.close()
  ous.close()
  printrmaps()

def replace(rstr, prefix, cnt, rmap):
  global maxstrlen
  if rstr not in rmap:
    rmap[rstr] = prefix + str(cnt)
    cnt += cnt + 1
    if len(rstr) > maxstrlen:
      maxstrlen = len(rstr)
  return rmap[rstr] 


def printrmaps():
  for s in addrmap:
    print padding(s), '--->',  addrmap[s]
  for s in hostmap:
    print padding(s), '--->', hostmap[s]

def padding(s):
  global maxstrlen
  pl = maxstrlen-len(s)
  return s.ljust(pl, ' ')

if __name__ == '__main__':
  inputfile = ''
  outputfile = ''
  try:
    opts, args = getopt.getopt(sys.argv[1:],"hi:o:",["ifile=","ofile="])
  except getopt.GetoptError:
    print 'main.py -i <inputfile> -o <outputfile>'
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      print 'main.py -i <inputfile> -o <outputfile>'
      sys.exit()
    elif opt in ("-i", "--ifile"):
      inputfile = arg
    elif opt in ("-o", "--ofile"):
      outputfile = arg

  if len(inputfile) == 0:
    print 'main.py -i <inputfile> -o <outputfile>'
    sys.exit(2)
  if len(outputfile) == 0:
    outputfile = inputfile + '.anon'

  print 'inputfile:  ', inputfile
  print 'outputfile: ', outputfile

  start = time.time()

  if check(inputfile, outputfile) == True:
    anonymize(inputfile, outputfile)
  
  done = time.time()
  elapsed = done - start
  print 'It spends ', elapsed, 'sec'
