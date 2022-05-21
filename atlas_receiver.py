
import sys
import argparse
import time
import struct
import RF24


def main():
    radio = RF24.RF24(24, 1, 1000000)
    if not radio.begin():
        raise RuntimeError("radio hardware is not responding begin")

    #if not radio.isChipConnected():
    #    raise RuntimeError("radio hardware is not responding isChipConnected")

    if not radio.isPVariant():
        raise RuntimeError("radio hardware is not responding isPVariant")

    radio.setPALevel(RF24.RF24_PA_MAX)

    addr = struct.pack("<5B", 0xac, 0xac, 0xac, 0xac, 0xac)
    radio.openWritingPipe(addr)

    radio.openReadingPipe(0, struct.pack("<5B", 0x9a, 0x78, 0x56, 0x34, 0x12))
    radio.openReadingPipe(1, struct.pack("<5B", 0x01, 0x01, 0x01, 0x01, 0x01))
    radio.openReadingPipe(2, struct.pack("<5B", 0x02, 0x02, 0x02, 0x02, 0x02))
    radio.openReadingPipe(3, struct.pack("<5B", 0x03, 0x03, 0x03, 0x03, 0x03))
    radio.openReadingPipe(4, struct.pack("<5B", 0x04, 0x04, 0x04, 0x04, 0x04))
    radio.openReadingPipe(5, struct.pack("<5B", 0x05, 0x05, 0x05, 0x05, 0x05))

    radio.setChannel(100)
    radio.setPayloadSize(32)
    radio.enableAckPayload()
    radio.enableDynamicPayloads()
    radio.enableDynamicAck()
    radio.setAutoAck(True)
    radio.setDataRate(RF24.RF24_250KBPS)
    radio.setCRCLength(RF24.RF24_CRC_8)

    #radio.enableAckPayload()
    #radio.setCRCLength(RF24.RF24_CRC_8)
    
    print(radio.getChannel())
    print(radio.getPayloadSize())
    print(radio.getDynamicPayloadSize())
    print(radio.getPALevel())
    print(radio.getDataRate())
    print(radio.getCRCLength()) 

    radio.startListening()

    radio.printDetails()

    radio.writeAckPayload(0, b'0')
    radio.writeAckPayload(1, b'1')
    radio.writeAckPayload(2, b'2')
    radio.writeAckPayload(3, b'3')
    radio.writeAckPayload(4, b'4')
    radio.writeAckPayload(5, b'5')

    while True:
        #avail = radio.available()
        #if not avail:
        #   continue

        #packet = radio.read()
        
        has_payload, pipe_number = radio.available_pipe()
        if has_payload:
            length = radio.getDynamicPayloadSize()
            received = radio.read(length)
            print(pipe_number)
            print(received)
            received = []
            #buffer = b'Hello?'
            #radio.writeAckPayload(0, buffer)
            #payload[0] = struct.unpack("<f", buffer[:4])[0]
            #print(
            #    "Received {} bytes on pipe {}: {}".format(
            #        radio.payloadSize,
            #        pipe_number,
             #       payload[0]
            #    )
            #)

    radio.stopListening()  # put the radio in TX mode


if __name__ == "__main__":
    main()
