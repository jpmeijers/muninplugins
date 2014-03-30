#!/usr/bin/python
'''
    A Munin plugin to graph D-Link DSL-2750U Router's ADSL connection quality
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
    print 'graph_title ADSL Signal Info'
    print 'graph_vlabel Power'
    print 'graph_category ADSL'
    print 'graph_info General ADSL connection quality stats of the D-Link DSL-2750U Router'
    
    # SNR Down
    print 'snrdown.label SNR Margin Down (dB)'
    print 'snrdown.warning 10:'
    print 'snrdown.critical 6:'
    print 'snrdown.info The SNR Margin of the downstream in dB'
    
    # SNR Up
    print 'snrup.label SNR Margin Up (dB)'
    print 'snrup.warning 10:'
    print 'snrup.critical 6:'
    print 'snrup.info The SNR Margin of the upstream in dB'
    
    # Attn Down
    # Attn stats
    # 3.5km = 48.3dB = 6Mbit
    # 4.0km = 56dB = 4Mbit
    # 4.5km = 62.1dB = 3Mbit
    # 5.0km = 69dB = 2Mbit
    print 'attdown.label Attenuation Down (dB)'
    print 'attdown.warning :60'
    print 'attdown.critical :69'	
    print 'attdown.info The Attenuation of the downstream in dB'
    
    # Attn Up
    print 'attup.label Attenuation Up (dB)'
    print 'attup.warning :60'
    print 'attup.critical :69'	
    print 'attup.info The Attenuation of the upstream in dB'
    
    # Transmit Power
    print 'transup.label Uplink TX power (dBm)'
    print 'transup.info The uplink transmitter power in dBm'
    print 'transdn.label Downlink TX Power (dBm)'
    print 'transdn.info The downlink transmitter power in dBm'


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

    snr = re.findall(r'SNR \(dB\):.*?([-+]?\d*\.\d+|\d+).*?([-+]?\d*\.\d+|\d+)', info)[0]
#    pprint(snr)
    attn = re.findall(r'Attn\(dB\):.*?([-+]?\d*\.\d+|\d+).*?([-+]?\d*\.\d+|\d+)', info)[0]
#    pprint(attn)
    trans = re.findall(r'Pwr\(dBm\):.*?([-+]?\d*\.\d+|\d+).*?([-+]?\d*\.\d+|\d+)', info)[0]
#    pprint(trans)
    # Debug info
    #print info
    #print stats
    
    # No stats if no adsl connection, default to zero
    if len(snr) == 2:
        print 'snrdown.value ', snr[0]
        print 'snrup.value ', snr[1]
    else:
        print 'snrdown.value 0'
        print 'snrup.value 0'

    if len(attn) == 2:
        print 'attdown.value ', attn[0]
        print 'attup.value ', attn[1]
    else:
        print 'attdown.value 0'
        print 'attup.value 0'

    if len(trans) == 2:
        print 'transdn.value ', trans[0]
        print 'transup.value ', trans[1]
    else:
        print 'transdn.value 0'
        print 'transup.value 0'

	


