import zmq
import socket
import sys
import argparse
import time, datetime
import struct
import datetime

from RF24 import RF24_PA_LOW, RF24_PA_HIGH, RF24_PA_MAX
from RF24 import RF24_1MBPS, RF24_250KBPS, RF24_2MBPS
from RF24 import RF24_CRC_16, RF24_CRC_8, RF24_CRC_DISABLED
from RF24 import RF24 as RF24_CLASS
from RF24 import RF24_CRC_DISABLED
from RF24 import RF24_CRC_8 
from RF24 import RF24_CRC_16


addr = ("127.0.0.1", 3077)

ss = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#radio1=RF24_CLASS(24, 1)
radio2=RF24_CLASS(24, 1)



def generate_logfile_name():
	now = datetime.datetime.utcnow().replace(microsecond=0)
	isostring = now.isoformat()  # string 2021-04-27T23:17:31
	isostring = isostring.replace("-", "")  # string 20210427T23:17:31
	isostring = isostring.replace(":", "")  # string 20210427T231731, oi ?oi iaai
	return "monolit_malinaS-" + isostring + ".bin"



if __name__ == '__main__':
	static_payload_size = None
	#static_payload_size = 16

	radio2.begin()

	radio2.openReadingPipe(1, b'\xac\xac\xac\xac\xac')

	radio2.setCRCLength(RF24_CRC_8)
	radio2.setAddressWidth(5)
	radio2.channel = 111
	radio2.setDataRate(RF24_250KBPS)

	radio2.setAutoAck(True)


	if static_payload_size is not None:
		radio2.disableDynamicPayloads()
		radio2.payloadSize = static_payload_size
	else:
		radio2.enableDynamicPayloads()

	radio2.enableAckPayload()
	radio2.enableDynamicAck()

	radio2.startListening()
	radio2.printDetails()



	#filename = 'monolit_malinaS.bin'
	filename = generate_logfile_name()
	f = open(filename, 'wb')
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	zmq_ctx = zmq.Context()

	pub_socket = zmq_ctx.socket(zmq.PUB)
	pub_socket.bind("tcp://0.0.0.0:1234")

	COUNTER = 0
	LOSS = 0
	PREV_PACKET_NUMBER = None
	while True:
		has_payload, pipe_number = radio2.available_pipe()
		#print(f'has_payload-{has_payload}, pipe_number={pipe_number}')

		if has_payload:
			payload_size = static_payload_size
			if payload_size is None:
				payload_size = radio2.getDynamicPayloadSize()

			data = radio2.read(payload_size)
			
			print('got data %s' % data)
			
			packet = data
			packet_size = len(packet)
			biter = struct.pack("<B", packet_size)
			unix = time.time()
			p_unix = struct.pack("d", unix)
			record = biter + packet + p_unix
			
			f.write(record)
			f.flush()
			try:
				s.sendto(packet, addr)
				pub_socket.send_multipart([packet], zmq.DONTWAIT)
			except Exception as e:
				print("unable to send data to socket")
			
		else:
			#print('got no data')
			time.sleep(0.001)
