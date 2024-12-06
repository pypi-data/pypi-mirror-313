from pyjuni.deflib import *


class Packet:
    def __init__(self, model=JDCODE):
        self.isBusy = False
        self.model = model
        self.packet = bytearray(20) 
        if self.model == JDCODE:
            self.packet[0:5] = [0x26, 0xA8, 0x14, 0xB1, 0x14]
        elif self.model == JCBOARD:
            self.packet[0:5] = [0x26, 0xA8, 0x14, 0xC1, 0x14]            
        elif self.model == JDMISSION:
            self.packet[0:5] = [0x26, 0xA8, 0x14, 0xD1, 0x14]
        elif self.model == UGLYBOT:
            self.packet[0:5] = [0x26, 0xA8, 0x14, 0xE1, 0x14]
        elif self.model == JDCODE_CMD:
            self.packet[0:5] = [0x26, 0xA8, 0x14, 0xB2, 0x14]
        elif self.model == ROBODOG:
            self.packet = bytearray(0x30) 
            self.packet[0:5] = [0x26, 0xA8, 0x14, 0x81, 0x30]
        else:
            self.packet[0:5] = [0x26, 0xA8, 0x14, 0x00, 0x14]


    def getCopiedPacket(self):
        if self.isBusy:
            return None
        self.isBusy = True
        pkt = bytearray(self.packet)
        self.isBusy = False
        return pkt


    def getPacket(self):
        return self.packet


    def makePacket(self, start, data):
        if self.isBusy:
            return
        self.isBusy = True

        for n in range(start, start+len(data)):
            self.packet[n] = data[n-start]
        self.packet[5] = DefLib.checksum(self.packet)
        #DefLib._print(self.packet)
        self.isBusy = False
        return self.packet
       

    def clearPacket(self):
        if self.isBusy:
            return
        self.isBusy = True

        if self.model == ROBODOG:
            for n in range(5, 0x28):
                self.packet[n] = 0
        else: 
            for n in range(5, 20):
                self.packet[n] = 0
        if self.model == JDCODE:
            self.packet[14] = 0x01
            self.packet[16] = self.packet[18] = 0x64
            self.packet[5] = DefLib.checksum(self.packet)
        self.isBusy = False
        return self.packet


