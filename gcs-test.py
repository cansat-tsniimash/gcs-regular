import sys
import argparse
import time
import struct

from RF24 import RF24_PA_LOW, RF24_PA_HIGH, RF24_PA_MAX
from RF24 import RF24_1MBPS, RF24_250KBPS, RF24_2MBPS
from RF24 import RF24_CRC_16, RF24_CRC_8, RF24_CRC_DISABLED
from RF24 import RF24 as RF24_CLASS
from RF24 import RF24_CRC_DISABLED
from RF24 import RF24_CRC_8 
from RF24 import RF24_CRC_16

#radio2=RF24_CLASS(24, 1)
radio1=RF24_CLASS(22, 0)

if __name__ == '__main__':
	static_payload_size = None
	#static_payload_size = 16

	radio1.begin()

	radio1.setCRCLength(RF24_CRC_DISABLED)
	radio1.openWritingPipe(b'\xac\xac\xac\xac\xac')
	radio1.setCRCLength(RF24_CRC_16)
	radio1.setAddressWidth(5)
	radio1.channel = 111
	radio1.setDataRate(RF24_250KBPS)
	radio1.disableAckPayload()
	radio1.enableDynamicAck()
	radio1.setAutoAck(False)
	if static_payload_size is not None:
		radio1.disableDynamicPayloads()
		radio1.payloadSize = static_payload_size
	else:
		radio1.enableDynamicPayloads()

	radio1.stopListening()
	radio1.printDetails()

	while True:
		buffer = b"p"*32

		radio1.write(buffer, 10)
		print("sent %s" % buffer)

		time.sleep(5.0)
