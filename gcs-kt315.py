import sys
import argparse
import time, datetime
import struct
import datetime

from RF24 import RF24_PA_LOW, RF24_PA_HIGH, RF24_PA_MAX
from RF24 import RF24_1MBPS, RF24_250KBPS, RF24_2MBPS
from RF24 import RF24_CRC_16, RF24_CRC_8, RF24_CRC_DISABLED
from RF24 import RF24 as RF24_CLASS


radio1=RF24_CLASS(22, 0)
#radio2=RF24_CLASS(24, 1)


def generate_logfile_name():
	now = datetime.datetime.utcnow().replace(microsecond=0)
	isostring = now.isoformat()  # string 2021-04-27T23:17:31
	isostring = isostring.replace("-", "")  # string 20210427T23:17:31
	isostring = isostring.replace(":", "")  # string 20210427T231731, oi ?oi iaai
	return "kt315-" + isostring + ".bin"


if __name__ == '__main__':
	#static_payload_size = None
	static_payload_size = 26

	radio1.begin()

	radio1.openReadingPipe(1, b'\xac\xac\xac\xac\xac')

	radio1.setCRCLength(RF24_CRC_DISABLED)
	radio1.setAddressWidth(5)
	radio1.channel = 116
	radio1.setDataRate(RF24_250KBPS)

	radio1.setAutoAck(False)


	radio1.enableAckPayload()
	radio1.enableDynamicAck()

	if static_payload_size is not None:
		radio1.disableDynamicPayloads()
		radio1.payloadSize = static_payload_size
	else:
		radio1.enableDynamicPayloads()


	radio1.startListening()
	radio1.printDetails()


	filename = generate_logfile_name()
	f = open(filename, 'wb')

	COUNTER = 0
	LOSS = 0
	PREV_PACKET_NUMBER = None
	while True:
		has_payload, pipe_number = radio1.available_pipe()
		if has_payload:
			payload_size = static_payload_size
			if payload_size is None:
				payload_size = radio1.getDynamicPayloadSize()
				print(payload_size)

			data = radio1.read(payload_size)
			print('\n\ngot data %s' % data)
			packet_size = len(data)
			biter = struct.pack(">B", packet_size)
			unix = time.time()
			p_unix = struct.pack("<d", unix)
			record = biter + data + p_unix
			

			try:
				unpacked = struct.unpack("<2B6hH2IH", data)
			except Exception as e:
				print(e)
				print(("data received: "),len(data), "bytes")
			else:

				flag = unpacked[0]
				bmp_temperature = unpacked[1] / 10
				acc_x = unpacked[2] / 1000
				acc_y = unpacked[3] / 1000
				acc_z = unpacked[4] / 1000
				gyro_x = unpacked[5] / 1000
				gyro_y = unpacked[6] / 1000
				gyro_z = unpacked[7] / 1000
				num = unpacked[8]
				time_from_start = unpacked[9]
				bmp_pressure = unpacked[10]
				crc = unpacked[11]

				if PREV_PACKET_NUMBER is not None:
					if (PREV_PACKET_NUMBER + 1 )& 0xFFFF != num:
						LOSS += num - PREV_PACKET_NUMBER - 1
					COUNTER += num - PREV_PACKET_NUMBER
				PREV_PACKET_NUMBER = num
				


				print("\nPressure: ", bmp_pressure)
				print("Temperature: ", bmp_temperature)
				print("Time: ", time_from_start)
				print("Accelerometer_y: " , acc_y)
				print("Accelerometer_z: ", acc_z)
				print("Accelerometer_x: ", acc_x)
				print("Gyroscope_x: ", gyro_x)
				print("Gyroscope_y: ", gyro_y)
				print("Gyroscope_z: ", gyro_z)
				print("Number_packet: ", num)
				print(f"LOSS = {LOSS}, COUNTER = {COUNTER}, LOSS PERCENT = {int(LOSS / COUNTER * 10000) / 100 if COUNTER > 0 else 0}%")

			f.write(record)
			f.flush()
		else:
			pass

		#time.sleep(0.005)
