import serial
import binascii
import math
from time import sleep
import random
from operator import eq
from threading import Thread
from serial.tools.list_ports import comports
from pyjuni.parse import *
from pyjuni.packet import *
from pyjuni.deflib import *


class JDMission(Parse,  Packet):
    def __init__(self, receiveCallback = None):
        self.serial = None
        self.isThreadRun = False
        self.parse = Parse(JDMISSION)
        self.makepkt = Packet(JDMISSION)
        self.makeCmdPkt = Packet(JDCODE_CMD)
        self.receiveCallback = receiveCallback
        self.makepkt.clearPacket()
        self.makeCmdPkt.clearPacket()
        self.posX = 0
        self.posY = 0
        self.rot = 0

    def receiveHandler(self):
        while self.isThreadRun:
            readData = self.serial.read(self.serial.in_waiting or 1)
            packet = self.parse.packetArrange(readData)
            if not eq(packet, "None"):
                if self.receiveCallback != None:
                    self.receiveCallback(packet)
            self.serial.write(self.makepkt.getPacket())


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
        self.isThreadRun = False
        sleep(0.2)
        pkt = self.makepkt.getPacket()
        if (pkt[15]&0x80) == 0x80:
            self.makepkt.clearPacket()
            self.setOption(0x00)
            self.serial.write(self.makepkt.getPacket())
            sleep(0.2)
        self.serial.write(self.makepkt.clearPacket())
        sleep(0.2)
        if self.serial != None:
            if self.serial.isOpen() == True:
                self.serial.close()

    def setOption(self, option):
        data = option.to_bytes(2, byteorder="little", signed=False)
        self.makepkt.makePacket(14, data)


    def takeoff(self):
        alt = 70
        data = alt.to_bytes(2, byteorder="little", signed=False)
        self.makepkt.makePacket(12, data)
        alt = 0x2F 
        data = alt.to_bytes(2, byteorder="little", signed=False)
        self.setOption(0x2F)


    def landing(self):
        alt = 0
        data = alt.to_bytes(2, byteorder="little", signed=False)
        self.makepkt.makePacket(12, data)


    def altitude(self, alt):
        data = alt.to_bytes(2, byteorder="little", signed=False)
        self.makepkt.makePacket(12, data)


    def velocity(self, dir=0, vel=100):
        if dir > 3:
            return
        if dir==1 or dir==3:
            vel *= -1; 
        data = vel.to_bytes(2, byteorder="little", signed=True)
        if dir==0 or dir==1:
            self.makepkt.makePacket(8, data)
        else:
            self.makepkt.makePacket(6, data)
        self.setOption(0x0F)


    def move(self, dir=0, dist=100):
        if dir > 3:
            return
        if dir==1 or dir==3:
            dist *= -1; 
        if dir==0 or dir==1:
            self.posX += dist
            data = self.posX.to_bytes(2, byteorder="little", signed=True)
            self.makepkt.makePacket(8, data)
        else:
            self.posY += dist
            data = self.posY.to_bytes(2, byteorder="little", signed=True)
            self.makepkt.makePacket(6, data)
            self.setOption(0x2F)
    
	
    def rotation(self, rot=90):
        self.rot += rot
        data = self.rot.to_bytes(2, byteorder="little", signed=True)
        self.makepkt.makePacket(10, data)


    def motor(self, what, speed):
        speed = DefLib.constrain(speed, 100, -100)
        data = speed.to_bytes(1, byteorder="little", signed=True)
        if what == LEFT:
            self.makepkt.makePacket(18, data)
        elif what == RIGHT:
            self.makepkt.makePacket(19, data)


    def emergency(self):
        self.setOption(0x00)
        self.serial.write(self.makepkt.getPacket())

    def setCmdOption(self, option):
        data = option.to_bytes(2, byteorder="little", signed=False)
        self.makeCmdPkt.makePacket(6, data)
        self.serial.write(self.makeCmdPkt.getPacket())
