import struct


FILEPATH = "/home/gcs/TELEMETRY-SAMPLE/etalon-telemetry.bin"
CSV_ORIENT_FILEPATH = FILEPATH + '-orient' + '.csv'
CSV_BME280_FILEPATH = FILEPATH + '-bme280' + '.csv'
CSV_DOSIM_FILEPATH = FILEPATH + '-dosim' + '.csv' 
CSV_GPS_FILEPATH = FILEPATH + '-gps' + '.csv'
CSV_STATE_FILEPATH = FILEPATH + '-state' + '.csv'

# Формат лога:
# 4 байта, флоат - время
# 1 байт, беззнаковое целое - размер пакета
# пакет длинной с указанным размером


stream = open(FILEPATH, mode="rb")


def read_packet(stream):
	packet_size_raw = stream.read(1)
	if not packet_size_raw:
		return None

	packet_size, = struct.unpack(">B", packet_size_raw)

	packet = stream.read(packet_size)

	time_raw = stream.read(8)
	time, = struct.unpack("<d", time_raw)

	return time, packet





class OrientParser:
	def __init__(self):
		self.csv_orient = open(CSV_ORIENT_FILEPATH, "w")
		line_name = '%s;%s;%s;%s;%s;%s;%s;;%s;%s;%s;%s;%s;%s' % ("flag", "acc_x", "acc_y", "acc_z", "gyro_x", "gyro_y", "gyro_z", "mag_x", "mag_y", "mag_z", "num", "time", "crc")
		print(line_name, file = self.csv_orient)
	def parse(self, data: bytes):
		unpacked = struct.unpack("<BhhhhhhhhhHIH", data[:27])

		flag = unpacked[0]
		acc_x = unpacked[1] / 1000
		acc_y = unpacked[2] / 1000
		acc_z = unpacked[3] / 1000
		gyro_x = unpacked[4] / 100
		gyro_y = unpacked[5] / 100
		gyro_z = unpacked[6] / 100
		mag_x = unpacked[7] / 1000
		mag_y = unpacked[8] / 1000
		mag_z = unpacked[9] / 1000
		num = unpacked[10]
		time = unpacked[11]
		crc = unpacked[12]

		line_orient = "%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s" % (flag, acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z, mag_x, mag_y, mag_z, num, time, crc) 
		print(line_orient, file = self.csv_orient)
		print(line_orient)
		

class BME280Parser:
	def __init__(self):
		self.csv_bme = open(CSV_BME280_FILEPATH, "w")
		line_name = "%s;%s;%s;%s;%s;%s" % ("flag", "bme280_temp", "num", "bme280_pres", "time", "crc")
		print(line_name, file = self.csv_bme)
	def parse(self, data: bytes):
		unpacked = struct.unpack("<BhHIIH", data[:15])

		flag = unpacked[0]		
		bme280_temp = unpacked[1] / 10
		num = unpacked[2]
		bme280_pres = unpacked[3]
		time = unpacked[4]
		crc = unpacked[5]
		line_bme280 = "%s;%s;%s;%s;%s;%s" %(flag, bme280_temp, num, bme280_pres, time, crc)
		print(line_bme280, file = self.csv_bme)
		print(line_bme280)

class DosimetrParser:
	def __init__(self):
		self.csv_dosim = open(CSV_DOSIM_FILEPATH, "w")
		line_name = '%s;%s;%s;%s;%s;%s;%s' % ("flag", "num", "time", "time_now", "tick_min", "tick_sum", "crc")
		print(line_name, file = self.csv_dosim)
	def parse(self, data: bytes):
		unpacked = struct.unpack("<BHIIIIH", data[:21])	

		flag = unpacked[0]
		num = unpacked[1]
		time = unpacked[2]
		time_now = unpacked[3]
		tick_min = unpacked[4]
		tick_sum = unpacked[5]
		crc = unpacked[6]
		line_dosim = "%s;%s;%s;%s;%s;%s;%s" % (flag, num, time, time_now, tick_min, tick_sum, crc)
		print(line_dosim, file = self.csv_dosim)
		print(line_dosim)

class GpsParser:
	def __init__(self):
		self.csv_gps = open(CSV_GPS_FILEPATH, "w")
		line_name = '%s;%s;%s;%s;%s;%s;%s;%s;%s;%s' % ("flag", "gps_fix", "gps_altitude", "num", "gps_latitude", "gps_longtitude", "time", "gps_time_s", "gps_time_us", "crc")
		print(line_name, file = self.csv_gps)
	def parse(self, data: bytes):
		unpacked = struct.unpack("<BBhHffIIIH", data[:28])

		flag = unpacked[0]
		gps_fix = unpacked[1]
		gps_altitude = unpacked[2] / 10
		num = unpacked[3]
		gps_latitude = unpacked[4]
		gps_longtitude = unpacked[5]
		time = unpacked[6]
		gps_time_s = unpacked[7]
		gps_time_us = unpacked[8]
		crc = unpacked[9]
		line_gps = "%s;%s;%s;%s;%s;%s;%s;%s;%s;%s" % (flag, gps_fix, gps_altitude, num, gps_latitude, gps_longtitude, time, gps_time_s, gps_time_us, crc)
		print(line_gps, file = self.csv_gps)
		print(line_gps)
		
class DSandStateParser:
	def __init__(self):
		self.csv_state = open(CSV_STATE_FILEPATH, "w")
		line_name = "%s;%s;%s;%s;%s" % ("flag", "state_apparate", "num", "temp", "crc")
		print(line_name, file = self.csv_state)
	def parse(self, data: bytes):
		unpacked = struct.unpack("<BBHHIH", data[:12])

		flag = unpacked[0]
		state_apparate = unpacked[1]
		num = unpacked[2]
		DS18temp = unpacked[3]
		crc = unpacked[4]
		line_state = "%s;%s;%s;%s;%s" % (flag, state_apparate, num, DS18temp, crc)

		print(line_state, file = self.csv_state)
		print(line_state)


orient = OrientParser()
bme = BME280Parser()
dosim = DosimetrParser()
ds8state = DSandStateParser()
gps = GpsParser()



while True:
	data = read_packet(stream)
	if data is None:
		break

	time, packet = data
	flag = packet[0]
	#print(f"flag={flag}, data={packet}, len(data)={len(packet)}")

	try:
		if flag == 228:
			orient.parse(packet)
		elif flag == 117:
			bme.parse(packet)
		elif flag == 66:
			dosim.parse(packet)
		elif flag == 99:
			ds8state.parse(packet)
		elif flag == 71:
			gps.parse(packet)
		else:
			print("НЕИЗВЕСТНЫЙ ФЛАГ %d" % flag)
	except Exception as e:
		print("НЕ МОГУ РАЗОБРАТЬ ПАКЕТ С ФЛАГОМ %d: %s" % (flag, e))


	# unpacked_bme = struct.unpack("<B", packet[:117])
	# unpacked_dosim = struct.unpack("<B", packet[:99])
	# unpacked_gps = struct.unpack("<B", packet[:66])
	# unpacked_state = struct.unpack("<B", packet[:71])

	#print(unpacked)
	#print("readed bytes %s of data %s at time %s" % (len(packet), packet, time))

#print("flag;BMP_temperature;LSM_acc_x;LSM_acc_y;LSM_acc_z;LSM_gyro_x;LSM_gyro_y;LSM_gyro_z;num;time_from_start;BMP_pressure;crc;time", file=csv_stream)

