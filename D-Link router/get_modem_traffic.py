#!/usr/bin/python
'''
    A Munin plugin to graph D-Link DSL-2750U Router's ADSL usage rates
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

if len(sys.argv) == 2 and sys.argv[1] == "autoconf":
    print "yes"
elif len(sys.argv) == 2 and sys.argv[1] == "config":
    print "graph_order down up"
    print "graph_title ADSL traffic"
    print 'graph_args --base 1000'
    print 'graph_vlabel bits in (+) / out (-) per ${graph_period}'
    print 'graph_category ADSL'
    print 'graph_info ADSL connection counters of the D-Link DSL-2750U Router'
    
    # PPP        
    print 'adsldown.label received'
    print 'adsldown.type DERIVE'
    print 'adsldown.graph no'
    print 'adsldown.cdef adsldown,8,*'
    print 'adsldown.min 0'
    print 'adslup.label ADSL'
    print 'adslup.type DERIVE'
    print 'adslup.negative adsldown'
    print 'adslup.cdef adslup,8,*'
    print 'adslup.min 0'

    # Bridge      
    print 'brdown.label received'
    print 'brdown.type DERIVE'
    print 'brdown.graph no'
    print 'brdown.cdef brdown,8,*'
    print 'brdown.min 0'
    print 'brup.label Bridge'
    print 'brup.type DERIVE'
    print 'brup.negative brdown'
    print 'brup.cdef brup,8,*'
    print 'brup.min 0'

    # Wlan     
    print 'wlandown.label received'
    print 'wlandown.type DERIVE'
    print 'wlandown.graph no'
    print 'wlandown.cdef wlandown,8,*'
    print 'wlandown.min 0'
    print 'wlanup.label Wlan'
    print 'wlanup.type DERIVE'
    print 'wlanup.negative wlandown'
    print 'wlanup.cdef wlanup,8,*'
    print 'wlanup.min 0'

else:

    tn = telnetlib.Telnet(HOST)

    tn.read_until("Login: ")
    tn.write(user + "\r")
    tn.read_until("Password: ")
    tn.write(password + "\r")
    tn.read_until("> ")
    tn.write("ifconfig" + "\r")
    info = tn.read_until("> ")
    tn.write("logout" + "\r")
    tn.close    

    pppcnt = re.findall(r'ppp.*?inet addr:.*?RX bytes:(\d*).*?TX bytes:(\d*)', info, flags=re.DOTALL)[0]
    pprint(pppcnt)
    brcnt = re.findall(r'br0.*?inet addr:.*?RX bytes:(\d*).*?TX bytes:(\d*)', info, flags=re.DOTALL)[0]
    pprint(brcnt)
    wlcnt = re.findall(r'wl.*?RX bytes:(\d*).*?TX bytes:(\d*)', info, flags=re.DOTALL)[0]
    pprint(wlcnt)
    # Debug info
    #print info
    #print stats
    
    # No stats if no adsl connection, default to zero
    if len(pppcnt) == 2:
        print 'adsldown.value ', pppcnt[1]
        print 'adslup.value ', pppcnt[0]
    else:
        print 'adsldown.value 0'
        print 'adslup.value 0'

    if len(brcnt) == 2:
        print 'brdown.value ', brcnt[0]
        print 'brup.value ', brcnt[1]
    else:
        print 'brdown.value 0'
        print 'brup.value 0'

    if len(wlcnt) == 2:
        print 'wlandown.value ', wlcnt[0]
        print 'wlanup.value ', wlcnt[1]
    else:
        print 'wlandown.value 0'
        print 'wlanup.value 0'

	


