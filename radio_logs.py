import struct
import time
import socket

def crc16(data : bytearray, offset=0, length=-1):
	if length < 0:
		length = len(data)
	
	if data is None or offset < 0 or offset > len(data)- 1 and offset+length > len(data):
		return 0

	crc = 0xFFFF
	for i in range(0, length):
		crc ^= data[offset + i] << 8

	for j in range(0,8):
		if (crc & 0x8000) > 0:
			crc =(crc << 1) ^ 0x1021
		else:
			crc = crc << 1

	return crc & 0xFFFF

class OrientParser:


	def parse(self, data: bytes):
		unpacked = struct.unpack("<BhhhhhhhhhHIH", data[:27])

		print("IMU PACKET =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")

		flag = unpacked[0]
		print ('flag: %s' %  flag)
		acc_x = unpacked[1] / 1000
		print ('acc_x: %s' % acc_x)
		acc_y = unpacked[2] / 1000
		print ('acc_y: %s' % acc_y)
		acc_z = unpacked[3] / 1000
		print ('acc_z: %s' % acc_z)
		gyro_x = unpacked[4] / 100
		print ('gyro_x: %s' % gyro_x)
		gyro_y = unpacked[5] / 100
		print ('gyro_y: %s' % gyro_y)
		gyro_z = unpacked[6] / 100
		print ('gyro_z: %s' % gyro_z)
		mag_x = unpacked[7] / 1000
		print ('mag_x: %s' % mag_x)
		mag_y = unpacked[8] / 1000
		print ('mag_y: %s' % mag_y)
		mag_z = unpacked[9] / 1000
		print ('mag_z: %s' % mag_z)
		num = unpacked[10]
		print ('num: %s' % num)
		time = unpacked[11]
		print ('time: %s' % time)
		crc = unpacked[12]
		print ('crc: %s' % crc)

		expected = crc
		actual = crc16(data[:25])
		if expected != actual:
			print("bad crc")
		else:
			print("good crc")



class BME280Parser:

		

	def parse(self, data: bytes):
		unpacked = struct.unpack("<BhHIIH", data[:15])

		print("BME280 PACKET =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")

		flag = unpacked[0]
		print ('flag: %s' % flag)
		bme280_temp = unpacked[1] / 10
		print ('bme280_temp: %s' % bme280_temp)
		num = unpacked[2]
		print ('num: %s' % num)
		bme280_pres = unpacked[3]
		print ('bme280_pres: %s' % bme280_pres)
		time = unpacked[4]
		print ('time: %s' % time)
		crc = unpacked[5]
		print ('crc: %s' % crc)
		expected = crc
		actual = crc16(data[:13])
		if expected != actual:
			print("bad crc")
		else:
			print("good crc")

	

class DosimetrParser:

	def parse(self, data: bytes):
		unpacked = struct.unpack("<BHIIIIH", data[:21])

		print("DOSIM PACKET =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")

		flag = unpacked[0]
		print ('flag: %s' % flag)
		num = unpacked[1]
		print ('num: %s' % num)
		time = unpacked[2]
		print ('time: %s' % time)
		time_now = unpacked[3]
		print ('time_now: %s' % time_now)
		tick_min = unpacked[4]
		print ('tick_min: %s' % tick_min)
		tick_sum = unpacked[5]
		print ('time_sum: %s' % tick_sum)
		crc = unpacked[6]
		print ('crc: %s' % crc)
		expected = crc
		actual = crc16(data[:19])
		if expected != actual:
			print("bad crc")
		else:
			print("good crc")

class GpsParser:


	def parse(self, data: bytes):
		unpacked = struct.unpack("<BBhHffIIIH", data[:28])
	
		print("GPS PACKET =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
		flag = unpacked[0]
		print ('flag: %s'  % flag)
		gps_fix = unpacked[1]
		print ('gps_fix: %s' % gps_fix)
		
		gps_altitude = unpacked[2] / 10
		print ('gps_altitude: %s' % gps_altitude)
		num = unpacked[3]
		print ('num: %s' % num)
		gps_latitude = unpacked[4]
		print('gps_latitude: %s' % gps_latitude)
		gps_longtitude = unpacked[5]
		print('gps_longtitude: %s' % gps_longtitude)
		time = unpacked[6]
		print ('time: %s' % time)
		gps_time_s = unpacked[7]
		print ('gps_time: %s' % gps_time_s)
		gps_time_us = unpacked[8]
		print ('gps_time_us: %s' % gps_time_us)
		crc = unpacked[9]
		print ('crc: %s' % crc)
		expected = crc
		actual = crc16(data[:26])
		if expected != actual:
			print("bad crc")
		else:
			print("good crc")

class DSandStateParser:

	def parse(self, data: bytes):
		unpacked = struct.unpack("<BBHHIH", data[:12])
		print("STATE PACKET =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
		flag = unpacked[0]
		print ('flag: %s' % flag)
		state_apparate = unpacked[1]
		print ('state_apparate: %s' % state_apparate)
		num = unpacked[2]
		print ('num: %s' % num)
		
		DS18temp = unpacked[3]
		print ('DS18temp: %s' % DS18temp)
		crc = unpacked[4]
		print ('crc: %s' % crc)
		expected = crc
		actual = crc16(data[:10])
		if expected != actual:
			print("bad crc")
		else:
			print("good crc")


orient = OrientParser()
bme = BME280Parser()
dosim = DosimetrParser()
ds8state = DSandStateParser()
gps = GpsParser()

def dispatch(data: bytes):
	print(data)
	print(len(data))
	flag = data[0]
	if flag == 228:
		orient.parse(data)
	elif flag == 117:
		bme.parse(data)
	elif flag == 66:
		dosim.parse(data)
	elif flag == 99:
		ds8state.parse(data)
	elif flag == 71:
		gps.parse(data)
	else:
		print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!непонятный флаг пакета: %d!!!" % flag)


client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind(('127.0.0.1', 3077))

while True:
	data = client.recv(0xFFFF)
	dispatch(data)





now = time.time()
print(now)

data = struct.pack("<d", now)
print(("0x" + "%02X"*4) % tuple([data[x] for x in range(0, 4)]))

file = open("good_telemetry.bin", "w")
adsd = str(data) + "," + str(crc) + "," + str(orient) + "," + str(bme) + "," + str(dosim) + "," + str(ds8state) + "," + str(gps) + "\n"
file.write(adsd)
file.close()
