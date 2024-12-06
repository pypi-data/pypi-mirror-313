import serial
import binascii
import math
import sys
from time import sleep
import platform
import random
from operator import eq
from queue import Queue
from threading import Thread
import subprocess
from serial.tools.list_ports import comports
from pyjuni.parse import *
from pyjuni.packet import *
from pyjuni.deflib import *


class RoboDog(Parse, Packet):
    def __init__(self, receiveCallback=None, index=0):
        super().__init__()
        self.serial = None
        self.isTXThreadRun = False
        self.isRXThreadRun = False
        self.parse = Parse(ROBODOG)
        self.makepkt = Packet(ROBODOG)
        self.receiveCallback = receiveCallback
        self.ledPacket = bytearray(34)
        self.rcvPacket = bytearray(20)
        self.portIndex = index;
        self.txCnt = 0;
        self.menualPacket = None

    def transmitHandler(self):
        while self.isTXThreadRun:
            if self.menualPacket != None:
                self.serial.write(self.menualPacket)
                sleep(0.1)
                continue;

            pkt = self.makepkt.getCopiedPacket()
            if (pkt[14]&0xC0) == 0xC0 :
                if (self.txCnt%2) == 0 : 
                    pkt[14] = self.ledPacket[0];
                    pkt[24:40] = self.ledPacket[2:18];
                else :
                    pkt[14] = self.ledPacket[1];
                    pkt[24:40] = self.ledPacket[18:34];
                pkt[5] = DefLib.checksum(pkt)

            if pkt != None:
                self.serial.write(pkt)
            sleep(0.05)
            self.txCnt += 1

    def receiveHandler(self):
        while self.isRXThreadRun:
            readData = self.serial.read(self.serial.in_waiting or 1)
            packet = self.parse.packetArrange(readData)
            if not eq(packet, "None"):
                self.rcvPacket[:len(packet)] = packet
                if self.receiveCallback is not None:
                    self.receiveCallback(self, packet)

    def Open(self, portName="None"):
        if eq(portName, "None"):
            nodes = comports()
            for node in nodes:
                if "USB " in node.description:
                    portName = node.device
                if "Dongle" in node.description:
                    portName = node.device

            if eq(portName, "None"):
                print("Can't find Serial Port")
                return False
        try:
            self.serial = serial.Serial(port=portName, baudrate=115200, timeout=1)
            if self.serial.isOpen():
                self.isTXThreadRun = True
                self.txThread = Thread(target=self.transmitHandler, args=(), daemon=True)
                self.txThread.start()
                self.isRXThreadRun = True
                self.rxThread = Thread(target=self.receiveHandler, args=(), daemon=True)
                self.rxThread.start()
                print("Connected to", portName)
                return True
            else:
                print("Can't open " + portName)
                exit()
            return False
        except BaseException:
            print("Can't open " + portName)
            return False

    def Close(self):
        pkt = self.makepkt.clearPacket()
        self.serial.write(pkt)
        self.isTXThreadRun = False
        self.isRXThreadRun = False
        sleep(0.1)
        if self.serial is not None:
            if self.serial.isOpen():
                self.serial.close()

    def leg(self, what, height, step, height_speed=100, step_speed=100):
        what = DefLib.constrain(what, 0, 3)
        height = DefLib.constrain(height, 20, 90)
        step = DefLib.constrain(step, -90, 90)
        pkt = self.makepkt.getPacket()

        if pkt[15] != 0x02 :
            pkt[16:24] = bytearray([DefLib.comp(-127)] * 8)
        pkt[15] = 0x02; 
        pkt[16 + what * 2] = height
        pkt[16 + what * 2 + 1] = DefLib.comp(step)
        pkt[40 + what * 2] = DefLib.constrain(height_speed, 0, 100)
        pkt[40 + what * 2 + 1] = DefLib.constrain(step_speed, 0, 100)
        pkt[5] = DefLib.checksum(pkt)


    def motor(self, what, shoulder, knee, shld_speed=100, knee_speed=100):
        what = DefLib.constrain(what, 0, 3)
        shoulder = DefLib.constrain(shoulder, -90, 90)
        knee = DefLib.constrain(knee, -90, 90)
        pkt = self.makepkt.getPacket()

        if pkt[15] != 0x03 :
            pkt[16:24] = bytearray([DefLib.comp(-127)] * 8)
        pkt[15] = 0x03; 

        pkt[16 + what * 2] = DefLib.comp(shoulder)
        pkt[16 + what * 2 + 1] = DefLib.comp(knee)
        pkt[40 + what * 2] = DefLib.constrain(shld_speed, 0, 100)
        pkt[40 + what * 2 + 1] = DefLib.constrain(knee_speed, 0, 100)
        pkt[5] = DefLib.checksum(pkt)

    def motor_speed(self, speed):
        pkt = self.makepkt.getPacket()
        pkt[13] = DefLib.constrain(speed, 10, 100)
        pkt[5] = DefLib.checksum(pkt)



    def leg_bend(self, leftup, rightup, leftdw, rightdw):
        pkt = self.makepkt.getPacket()

        if pkt[15] != 0x01 :
            pkt[16:24] = bytearray([0] * 8)
        pkt[15] = 0x01; 

        pkt[16] = DefLib.constrain(leftup, 20, 90)
        pkt[17] = DefLib.constrain(leftdw, 20, 90)
        pkt[18] = DefLib.constrain(rightdw, 20, 90)
        pkt[19] = DefLib.constrain(rightup, 20, 90)
        pkt[5] = DefLib.checksum(pkt)

    def move(self, vel):
        pkt = self.makepkt.getPacket()

        if pkt[15] != 0x01 :
            pkt[16:24] = bytearray([0] * 8)
        pkt[15] = 0x01; 

        pkt[20] = DefLib.comp(DefLib.constrain(vel, -100, 100))
        pkt[5] = DefLib.checksum(pkt)


    def rotate(self, deg, degVel):
        pkt = self.makepkt.getPacket()

        if pkt[15] != 0x01 :
            pkt[16:24] = bytearray([0] * 8)
        pkt[15] = 0x01; 

        deg = DefLib.constrain(deg, -1000, 1000)
        pkt[21] = DefLib.constrain(degVel, 10, 100)
        pkt[22] = deg&0xFF 
        pkt[23] = (deg>>8)&0xFF
        pkt[5] = DefLib.checksum(pkt)

    def rotate_ex(self, deg, degVel, mode):
        pkt = self.makepkt.getPacket()

        if pkt[15] != 0x01 :
            pkt[16:24] = bytearray([0] * 8)
        pkt[15] = 0x01; 

        deg = DefLib.constrain(deg, -1000, 1000)
        deg = deg | (mode<<14)
        pkt[21] = DefLib.constrain(degVel, 10, 100)
        pkt[22] = deg&0xFF 
        pkt[23] = (deg>>8)&0xFF
        pkt[5] = DefLib.checksum(pkt)


    def gesture(self, action):
        pkt = self.makepkt.getPacket()

        if pkt[15] != 0x04 :
            pkt[16:24] = bytearray([0] * 8)
        pkt[15] = 0x04; 

        pkt[16] = DefLib.constrain(action, 0, 4)
        pkt[5] = DefLib.checksum(pkt)

    def headLEDDraw(self, leftLED, rightLED):
        if not isinstance(leftLED, bytearray) or len(leftLED) != 8:
            return
        if not isinstance(rightLED, bytearray) or len(rightLED) != 8:
            return
        pkt = self.makepkt.getPacket()
        pkt[14] = (pkt[14]&0xC0) | 0x81;
        pkt[24:32] = leftLED
        pkt[32:40] = rightLED
        pkt[5] = DefLib.checksum(pkt)
        self.ledPacket[0] = pkt[14];
        self.ledPacket[1] = self.ledPacket[1] | 0x80;
        self.ledPacket[2:18]  = pkt[24:40]

    def headLEDExp(self, what):
        pkt = self.makepkt.getPacket()
        pkt[14] = (pkt[14]&0xC0) | 0x82;
        pkt[24] = what
        pkt[5] = DefLib.checksum(pkt)
        self.ledPacket[0] = pkt[14];
        self.ledPacket[1] = self.ledPacket[1] | 0x80;
        self.ledPacket[2:18]  = pkt[24:40]


    def bodyLED(self, what, red, green, blue):
        pkt = self.makepkt.getPacket()
        what = DefLib.constrain(what, 0, 0x0F)
        red = DefLib.constrain(red, 0, 255)
        green = DefLib.constrain(green, 0, 255)
        blue = DefLib.constrain(blue, 0, 255)
        pkt[14] = (pkt[14]&0xC0) | 0x44;
        for n in range(4):
            if (what & (0x01<<n)) > 0 :
                pkt[24 + n*4] = red;
                pkt[25 + n*4] = green;
                pkt[26 + n*4] = blue;
        pkt[5] = DefLib.checksum(pkt)
        self.ledPacket[1] = pkt[14];
        self.ledPacket[0] = self.ledPacket[0] | 0x40;
        self.ledPacket[18:34]  = pkt[24:40]


    def sound(self, thema, track, volume):
        pkt = self.makepkt.getPacket()
        trackID = 0 if (pkt[7]&0x80)==0x80 else 0x80;
        pkt[7] = (thema*10 + track) | trackID;
        pkt[8] = volume;
        pkt[5] = DefLib.checksum(pkt)

    def extServo(self, degree):
        pkt = self.makepkt.getPacket()
        deg = DefLib.constrain(degree, -90, 90)
        pkt[12] = DefLib.comp(deg)
        pkt[5] = DefLib.checksum(pkt)
		

    def ledPrint(self, leftChar, rightChar):
        pkt = self.makepkt.getPacket()
        pkt[14] = 3;
        pkt[32] = leftChar
        pkt[24] = rightChar
        pkt[5] = DefLib.checksum(pkt)

    def txMenualPacket(self, pkt, rxHead):
        if pkt != None:
            pkt[5] = DefLib.checksum(pkt)
        self.parse.setManualHead(rxHead)
        self.menualPacket = pkt;

    def rb_runfile(self, filename=""):
        name_bytes = filename.encode("utf-8")
        if len(name_bytes) > 23:
            return
        req_packet = bytearray(0x20)
        req_packet[:7] = [0x26, 0xA8, 0x14, 0x87, 0x20, 0x00, 0x01];
        req_packet[7:len(name_bytes)+7] = name_bytes
        req_packet[5] = DefLib.checksum(req_packet)
        self.menualPacket = req_packet;
        while True:
            if self.rcvPacket[4] == len(req_packet) and self.rcvPacket[6] == 2 :
                name_bytes = self.rcvPacket[7:]
                self.menualPacket = None;
                return name_bytes.decode("utf-8")
            sleep(0.01)

    def get_battery(self):
        return self.rcvPacket[6]

    def get_distance(self):
        return self.rcvPacket[7]

    def get_tilt(self):
        return [DefLib.toSigned8(self.rcvPacket[8]), DefLib.toSigned8(self.rcvPacket[9])]

    def get_rotation(self):
        return DefLib.toSigned16((self.rcvPacket[11]<<8) | self.rcvPacket[10]);

    def get_rb_data(self, index):
        index = DefLib.constrain(index, 0, 4)
        return DefLib.toSigned8(self.rcvPacket[12+index])

    def get_rb_bytearray(self):
        return self.rcvPacket[12:16] + self.rcvPacket[18:20]

    def is_button_pressed(self):
        return True if self.rcvPacket[16] == 1 else False

    def is_rb_alive(self):
        return True if self.rcvPacket[17] == 1 else False

def getWindowsPortList():
    nodes = comports()
    print(len(nodes))
    portList = []
    for node in nodes:
        if "USB " in node.description:
            portList.append(node.device)
        if "Dongle" in node.description:
            portList.append(node.device)

    if len(portList) == 0:
        print("Can't find Serial Port")
        return None
    return portList;

def getLinuxPortList():
    output = subprocess.check_output('ls /dev/ttyACM*', shell=True)
    return tuple(output.decode().strip().split())

def RoboDogMultiOpen(nameList=None, receiveCallback=None):
    if(nameList == None):
        if platform.system() == 'Linux':
            nameList = getLinuxPortList()
        else:
            nameList = getWindowsPortList()
    if(nameList == None):
        return None
    howMany = len(nameList)
    if(howMany == 0):
        return None
    howMany = 10 if howMany > 10 else howMany
    robodog = []
    for n in range(howMany):
        robodog.append(RoboDog(receiveCallback, n))
        if(robodog[n].Open(nameList[n]) == False):
            robodog.pop()
            RoboDogMultiClose(robodog)
            exit()
    return robodog



def RoboDogMultiClose(robodog):
    if(robodog == None):
        return None
    howMany = len(robodog)
    for n in range(len(robodog)):
        robodog[n].gesture(0)
    sleep(0.5)
    for n in range(howMany):
        robodog[n].Close()


def multi_leg_bend(dogs, leftup, rightup, leftdw, rightdw):
    for n in range(len(dogs)):
        dogs[n].leg_bend(leftup, rightup, leftdw, rightdw)

def multi_move(dogs, vel):
    for n in range(len(dogs)):
        dogs[n].move(vel)

def multi_rotate(dogs, deg, degVel):
    for n in range(len(dogs)):
        dogs[n].rotate(deg, degVel)

def multi_leg(dogs, what, height, step, height_speed=100, step_speed=100):
    for n in range(len(dogs)):
        if isinstance(what, int):
            dogs[n].leg(what, height, step, height_speed, step_speed)
        else:
            for k in range(len(what)):
                dogs[n].leg(what[k], height, step, height_speed, step_speed)

def multi_motor(dogs, what, shoulder, knee, shld_speed=100, knee_speed=100):
    for n in range(len(dogs)):
        if isinstance(what, int):
            dogs[n].motor(what, shoulder, knee, shld_speed, knee_speed)
        else:
            for k in range(len(what)):
                dogs[n].motor(what[k], shoulder, knee, shld_speed, knee_speed)

