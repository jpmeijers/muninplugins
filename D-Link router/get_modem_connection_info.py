#!/usr/bin/python
'''
    A Munin plugin to graph D-Link DSL-2750U Router's ADSL sync rates
    Copyright (C) 2014  NC Thompson & JP Meijers

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

'''

import getpass
import sys
import telnetlib
import re
import sys
from pprint import pprint

# Set username and password
HOST = "192.168.2.1"
user = "admin"
password = "meijers"

#linespeed in bits/second as a number
#ex: linespeed_down = 2048000 # for 2mbps line
linespeed_down = 2048000
linespeed_up = 512000

if len(sys.argv) == 2 and sys.argv[1] == "autoconf":
    print "yes"
elif len(sys.argv) == 2 and sys.argv[1] == "config":
    print 'graph_title ADSL Connection Info'
    print 'graph_vlabel Speed in bits per second'
    print 'graph_category ADSL'
    print 'graph_info General ADSL connection stats of the D-Link DSL-2750U Router'
    
    # Max Down
    print 'maxdown.label Attainable downstream rate'
    # Set to your line speed
    print 'maxdown.warning '+str(linespeed_down)+':'
    print 'maxdown.critical '+str(linespeed_down*0.9)+':'
    print 'maxdown.info The maximum attainable downstream rate.'
    
    # Max Up
    print 'maxup.label Attainable upstream rate'
    print 'maxup.warning '+str(linespeed_up)+':'
    print 'maxup.critical '+str(linespeed_up*0.9)+':'
    print 'maxup.info The maximum attainable upstream rate.'
    
    # Sync Down
    print 'syncdown.label Current downstream rate'
    # Set to your line speed
    print 'syncdown.warning '+str(linespeed_down)+':'
    print 'syncdown.critical '+str(linespeed_down*0.9)+':'
    print 'syncdown.info The current downstream rate.'
    
    # Sync Up
    print 'syncup.label Current upstream rate'
    print 'syncup.warning '+str(linespeed_up)+':'
    print 'syncup.critical '+str(linespeed_down*0.9)+':'
    print 'syncup.info The current upstream rate.'

else:

    tn = telnetlib.Telnet(HOST)

    tn.read_until("Login: ")
    tn.write(user + "\r")
    tn.read_until("Password: ")
    tn.write(password + "\r")
    tn.read_until("> ")
    tn.write("adsl info --show" + "\r")
    info = tn.read_until("> ")
    tn.write("logout" + "\r")
    tn.close
    
    # Debug info
    maxup = re.findall(r'Max:.*?Upstream rate = ([-+]?\d*\.\d+|\d+) Kbps', info)
#    pprint(maxup)
    maxdown = re.findall(r'Max:.*?Downstream rate = ([-+]?\d*\.\d+|\d+) Kbps', info)
#    pprint(maxdown)
    syncup = re.findall(r'Channel:.*?Upstream rate = ([-+]?\d*\.\d+|\d+) Kbps', info)
#    pprint(syncup)
    syncdown = re.findall(r'Channel:.*?Downstream rate = ([-+]?\d*\.\d+|\d+) Kbps', info)
#    pprint(syncdown)
    #print info
    #print stats
    
    # No stats if no adsl connection, default to zero
    if len(maxup) == 1:
        maxup = int(maxup[0])*1000
        print 'maxup.value ', str(maxup)
    else:
        print 'maxup.value 0'

    if len(maxdown) == 1:
        maxdown = int(maxdown[0])*1000
        print 'maxdown.value ', maxdown
    else:
        print 'maxdown.value 0'
	
    if len(syncup) == 1:
        syncup = int(syncup[0])*1000
        print 'syncup.value ', syncup
    else:
        print 'syncup.value 0'

    if len(syncdown) == 1:
        syncdown = int(syncdown[0])*1000
        print 'syncdown.value ', syncdown
    else:
        print 'syncdown.value 0'

