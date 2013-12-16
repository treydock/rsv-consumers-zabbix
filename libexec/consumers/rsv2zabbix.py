#!/usr/bin/env /apps/Modules/wrappers/python_wrapper.sh

import sys
import re
import base64
from urlparse import urlparse
import string
import ConfigParser
import os
import socket
import struct
import json

def translate_rsv_2_zabbix(rsvOutput):
    zabbixCode = {}
    zabbixCode["OK"]="0"
    zabbixCode["CRITICAL"]="2"
    zabbixCode["WARNING"]="1"
    zabbixCode["UNKNOWN"]="3"

    zabbixStatus=zabbixCode["UNKNOWN"]
    zabbixOutput="RSV probe has no summaryData/detailsData"
    zabbixHost="UNKNOWN"
    detailsDataField=""
    for line in string.split(rsvOutput,"\n"):
	if string.find(line,"serviceURI")==0:
	    zabbixHost=string.strip(string.split(line,":")[1])
        if string.find(line,"metricStatus")==0:
            status=string.strip(string.split(line,":")[1])
            zabbixStatus = zabbixCode[status]
        if detailsDataField!="":
            detailsDataField+=string.strip(line)
        if string.find(line,"detailsData")==0:
            detailsDataField=string.strip(string.split(line,":",1)[1])
    if detailsDataField!="":
         zabbixOutput=detailsDataField[0:255]
    return (zabbixStatus,zabbixOutput,zabbixHost)


def send_2_zabbix(ZABX_HOST, ZABX_PORT, SERVICE, HOST, ZABX_ITEM_KEY, PLUGIN_STATE, PLUGIN_OUTPUT):
	HEADER = 'ZBXD\1'
	DATA = {
		"request":"sender data",
		"data":[
			{
				"host":"%s" % HOST,
				"key":"%s[%s]" % (ZABX_ITEM_KEY, SERVICE),
				"value":"%s" % PLUGIN_STATE,
			}
		]
	}

	data_string = json.dumps(DATA)

	data_length = len(data_string)
	data_header = HEADER.encode("ascii") + struct.pack('i', data_length) + '\0\0\0\0'

	data_to_send = data_header + data_string

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((ZABX_HOST, int(ZABX_PORT)))

	# Send data to Zabbix server
	sock.send(data_to_send)

	# Read response, first five bytes
	response_header = sock.recv(5)
	if not response_header == 'ZBXD\1':
    		raise ValueError('Got invalid response')

	# read the data header to get the length of the response
	response_data_header = sock.recv(8)
	response_data_header = response_data_header[:4] # we are only interested in the first four bytes
	response_len = struct.unpack('i', response_data_header)[0]

	# read the whole rest of the response now that we know the length
	response_raw = sock.recv(response_len)

	sock.close()

	response = json.loads(response_raw)

	print response
	sys.exit(0)

#MAIN
#Get the RSV probe output, host and state from STDIN and convert to NAGIOS format
rsvOutput=""
for line in sys.stdin.readlines():
        rsvOutput = rsvOutput + line
(PLUGIN_STATE,PLUGIN_OUTPUT,PLUGIN_HOST)=translate_rsv_2_zabbix(rsvOutput)

#Get the NAGIOS server, username and password from the config file
if not os.path.exists(sys.argv[1]):
    print "ERROR: The supplied configuration file '%s' does not exist." % sys.argv[1]
    sys.exit(1)

config = ConfigParser.ConfigParser();
config.read(sys.argv[1]);
ZABX_HOST=config.get("RSV", "ZABX_HOST");
ZABX_PORT=config.get("RSV", "ZABX_PORT");
ZABX_ITEM_KEY=config.get("RSV", "ZABX_ITEM_KEY");
#Send output to NAGIOS server, using the service name passed by the zabbix consumer
send_2_zabbix(ZABX_HOST, ZABX_PORT, sys.argv[2], PLUGIN_HOST, ZABX_ITEM_KEY, PLUGIN_STATE, PLUGIN_OUTPUT);
