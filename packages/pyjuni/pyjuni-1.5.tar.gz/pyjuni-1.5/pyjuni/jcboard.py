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

class JCBoard(Parse,  Packet):
    def __init__(self, receiveCallback = None):
        self.serial = None
        self.isThreadRun = False
        self.parse = Parse(JCBOARD)
        self.makepkt = Packet(JCBOARD)
        self.receiveCallback = receiveCallback
        self.noteID = random.randrange(1,15)


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


	
    def useUltrasonic(self, pin):
        if pin>4:
            return

        data = bytearray(1)
        data[0] = 0x01 << pin
        pkt = self.makepkt.makePacket(16, data)
        self.serial.write(pkt)


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
        pkt = self.makepkt.makePacket(8, data)
        self.serial.write(pkt)


    def motor(self, right, left):
        left = DefLib.constrain(left, 100, -100)
        right = DefLib.constrain(right, 100, -100)
        data = bytearray(2)
        data[0] = DefLib.comp(right)
        data[1] = DefLib.comp(left)
        pkt = self.makepkt.makePacket(10, data)
        self.serial.write(pkt)

    def servo(self, pin, angle):
        if pin>4:
            return
        angle = DefLib.constrain(angle, 90, -90)
        data = bytearray(1)
        data[0] = DefLib.comp(angle)
        pkt = self.makepkt.makePacket(12+pin, data)
        self.serial.write(pkt)

	
    def digitalPin(self, pins):
        pins = pins & 0x1F
        data = bytearray(1)
        data[0] = pins
        pkt = self.makepkt.makePacket(7, data)
        self.serial.write(pkt)

