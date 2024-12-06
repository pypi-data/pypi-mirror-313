from pyjuni.deflib import *

class Parse:
    def __init__(self, model=JDCODE):
        self.model = model
        self.packet = bytearray(100)
        self.offset = 0
        self.type = 0
        self.packetLen = 20 
        self.headMatchCnt = 0
        self.manualHead = None
        if self.model == JDCODE or self.model == JDMISSION:
            self.head = (0x26, 0xA8, 0x14, 0xA0)
        elif self.model == UGLYBOT:
            self.head = (0x26, 0xA8, 0x14, 0xE0)
        elif self.model == JCBOARD:
            self.head = (0x26, 0xA8, 0x14, 0xD0)
        elif self.model == ROBODOG:
            self.head = (0x26, 0xA8, 0x14, 0x80)
        else:
            self.head = (0x26, 0xA8, 0x14, 0x00)


    def findHeader(self, ch):
        if self.headMatchCnt==3:
            ch = ch&0xF0
        if self.manualHead == None:
            if ch == self.head[self.headMatchCnt]:
                self.headMatchCnt += 1
            else:
                self.headMatchCnt = 0
        else:
            if ch == self.manualHead[self.headMatchCnt]:
                self.headMatchCnt += 1
            else:
                self.headMatchCnt = 0
        if self.headMatchCnt==4:
            self.headMatchCnt = 0
            self.offset = 4
            self.packetLen = 20 
            return True
        else:
            return False

    def packetArrange(self, data):
        for n in range(0, len(data)):
            if self.findHeader(data[n]) == True:
                self.type = data[n]&0x0F
            elif self.offset>0:
                self.packet[self.offset] = data[n]
                if self.offset == 4:
                    self.packetLen = data[n]
                self.offset += 1
            if self.offset == self.packetLen:
                self.offset = 0
                chksum = DefLib.checksum(self.packet)
                if chksum == self.packet[5]:
                    pkt = bytearray(self.packetLen)
                    for n in range(0, self.packetLen):
                        pkt[n] = self.packet[n];
                    return pkt
            if self.offset >= 100:
                self.offset = 0;
        return "None"

    def setManualHead(self, head):
        self.manualHead = head
