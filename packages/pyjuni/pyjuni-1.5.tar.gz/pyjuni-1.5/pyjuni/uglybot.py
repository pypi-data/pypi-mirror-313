import serial
import binascii
import math
from time import sleep
import random
from operator import eq
from queue import Queue
from threading import Thread
from serial.tools.list_ports import comports
from pyjuni.parse import *
from pyjuni.packet import *
from pyjuni.deflib import *

class UglyBot(Parse,  Packet):
    def __init__(self, receiveCallback = None):
        self.serial = None
        self.isThreadRun = False
        self.parse = Parse(UGLYBOT)
        self.makepkt = Packet(UGLYBOT)
        self.receiveCallback = receiveCallback
        self.noteID = random.randrange(1,15)
        self.moveID = random.randrange(1,15)
        self.rotID = random.randrange(1,15)

    def receiveHandler(self):
        while self.isThreadRun:
            readData = self.serial.read(self.serial.in_waiting or 1)
            packet = self.parse.packetArrange(readData)
            if not eq(packet, "None"):
                if self.receiveCallback != None:
                    self.receiveCallback(packet)


    def Open(self, portName = "None"):
        if eq(portName, "None"):
            nodes = comports()
            for node in nodes:
                if "USB " in node.description:
                    portName = node.device
                if "Dongle" in node.description:
                    portName = node.device
                if "CH340" in node.description:
                    portName = node.device
            
            if eq(portName, "None"):
                print("Can't find Serial Port")
                exit()
                return False
        try:
            self.serial = serial.Serial(port=portName, baudrate=19200, timeout=1)
            if self.serial.isOpen():
                self.isThreadRun = True
                self.thread = Thread(target=self.receiveHandler, args=(), daemon=True)
                self.thread.start()
                print("Connected to", portName)   
                return True
            else:
                print("Can't open " + portName)
                exit()
                return False
        except:
            print("Can't open " + portName)
            exit()
            return False
			

    def Close(self):
        pkt = self.makepkt.clearPacket()
        self.serial.write(pkt)
        self.isThreadRun = False
        sleep(0.2)
        if self.serial != None:
            if self.serial.isOpen() == True:
                self.serial.close()


	
    def led(self, status):
        status = status&0x03
        data = bytearray(1)
        data[0] = status | 0x10
        pkt = self.makepkt.makePacket(6, data)
        self.serial.write(pkt)


    def buzzer(self, note, duration=1):
        note = DefLib.constrain(note, 7, 1)
        duration = DefLib.constrain(duration*10, 50, 1)
        data = bytearray(2)
        data[0] = note | ((self.noteID&0x0F)<<4)
        data[1] = math.floor(duration)
        self.noteID = (self.noteID+1)&0x0F;
        pkt = self.makepkt.makePacket(7, data)
        self.serial.write(pkt)


    def motor(self, left, right):
        left = DefLib.constrain(left, 100, -100)
        right = DefLib.constrain(right, 100, -100)
        data = bytearray(2)
        data[0] = DefLib.comp(right)
        data[1] = DefLib.comp(left)
        pkt = self.makepkt.makePacket(9, data)
        self.serial.write(pkt)

	
    def move(self, distance):
        distance = DefLib.constrain(distance, 1023, -1023)
        distance = (distance&0xFFF) | ((self.moveID&0x0F)<<12)
        self.moveID = (self.moveID+1)&0x0F;
        data = distance.to_bytes(2, byteorder="little", signed=False)
        pkt = self.makepkt.makePacket(11, data)
        self.serial.write(pkt)

	
    def rotation(self, degree):
        degree = DefLib.constrain(degree, 1000, -1000)
        degree = (degree&0xFFF) | ((self.rotID&0x0F)<<12)
        self.rotID = (self.rotID+1)&0x0F;
        data = degree.to_bytes(2, byteorder="little", signed=False)
        pkt = self.makepkt.makePacket(13, data)
        self.serial.write(pkt)

	
    def ir(self, status):
        status = status&0x07
        data = bytearray(1)
        data[0] = status
        pkt = self.makepkt.makePacket(17, data)
        self.serial.write(pkt)

