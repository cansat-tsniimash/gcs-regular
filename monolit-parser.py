import struct


FILEPATH = "/home/gcs/kt315-telemetry-etalon.bin"
CSV_FILEPATH = FILEPATH + '.csv'

# Формат лога:
# 4 байта, флоат - время
# 1 байт, беззнаковое целое - размер пакета
# пакет длинной с указанным размером


def read_packet(stream):
	packet_size_raw = stream.read(1)
	if not packet_size_raw:
		return None

	packet_size, = struct.unpack(">B", packet_size_raw)

	packet = stream.read(packet_size)

	time_raw = stream.read(8)
	time, = struct.unpack("<d", time_raw)

	return time, packet


stream = open(FILEPATH, mode="rb")
csv_stream = open(CSV_FILEPATH, mode="w")
print("flag;BMP_temperature;LSM_acc_x;LSM_acc_y;LSM_acc_z;LSM_gyro_x;LSM_gyro_y;LSM_gyro_z;num;time_from_start;BMP_pressure;crc;time", file=csv_stream)

while True:
	data = read_packet(stream)
	if data is None:
		break

	time, packet = data
	print(time, packet, len(packet))

	if len(packet) == 0:
		continue

	unpacked = struct.unpack("<BB3H3HH2IH", packet)
	print(unpacked)
	print("readed bytes %s of data %s at time %s" % (len(packet), packet, time))
						#uint8_t flag;
						#uint8_t BMP_temperature;
						#uint16_t LSM_acc_x;
						#uint16_t LSM_acc_y;
						#uint16_t LSM_acc_z;
						#uint16_t LSM_gyro_x;
						#uint16_t LSM_gyro_y;
						#uint16_t LSM_gyro_z;
						#uint16_t num;
						#uint32_t time_from_start;
						#uint32_t BMP_pressure;
						#uint16_t crc;
	flag = unpacked[0]
	BMP_temperature = unpacked[1]
	LSM_acc_x = unpacked[2]
	LSM_acc_y = unpacked[3]
	LSM_acc_z = unpacked[4]
	LSM_gyro_x = unpacked[5]
	LSM_gyro_y = unpacked[6]
	LSM_gyro_z = unpacked[7]
	num = unpacked[8]
	time_from_start = unpacked[9]
	BMP_pressure = unpacked[10] 
	crc = unpacked[11]

	line = "%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s" % (flag, BMP_temperature, LSM_acc_x, LSM_acc_y, LSM_acc_z, LSM_gyro_x, LSM_gyro_y , LSM_gyro_z, num, time_from_start, BMP_pressure, crc, time)
	print(line, file=csv_stream)
	print(line)

