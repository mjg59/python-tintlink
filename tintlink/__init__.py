# Python module for control of Tintlink bluetooth LED bulbs
#
# Copyright 2016 Matthew Garrett <mjg59@srcf.ucam.org>
#
# This code is released under the terms of the MIT license. See the LICENSE file
# for more details.

import BDAddr
from BluetoothSocket import BluetoothSocket, hci_devba
import random
import socket
import sys
import time

def send_packet(sock, handle, data):
  packet = bytearray([0x12, handle, 0x00])
  for item in data:
    packet.append(item)
  sock.send(packet)
  data = sock.recv(32)
  response = []
  for d in data:
    response.append(ord(d))
  return response

def checksum(data):
    value = 0
    for i in range(1, len(data)-2):
        value = value + data[i]
    value = value + 85
    return value & 0xff

def read_packet(sock, handle):
  packet = bytearray([0x0a, handle, 0x00])
  sock.send(packet)
  data = sock.recv(32)
  response = []
  for d in data:
    response.append(ord(d))
  return response

class tintlink:
  def __init__(self, mac):
    self.mac = mac

  def connect(self):
    my_addr = hci_devba(0) # get from HCI0
    dest = BDAddr.BDAddr(self.mac)
    addr_type = BDAddr.TYPE_LE_PUBLIC
    self.sock = BluetoothSocket(socket.AF_BLUETOOTH, socket.SOCK_SEQPACKET, socket.BTPROTO_L2CAP)
    self.sock.bind_l2(0, my_addr, cid=4, addr_type=BDAddr.TYPE_LE_RANDOM)
    self.sock.connect_l2(0, dest, cid=4, addr_type=addr_type)
    print read_packet(self.sock, 0x24)
    
  def on(self):
      send_packet(self.sock, 0x21, bytearray([0xaa, 0x0a, 0xfc, 0x3a, 0x86, 0x01, 0x10, 0x01, 0x01, 0x00, 0x28, 0x0d]))

  def set_brightness(self, brightness):
      packet=bytearray([0xaa, 0x0a, 0xfc, 0x3a, 0x86, 0x01, 0x0c, 0x01, brightness, 0x00, 0x00, 0x0d])
      packet[9] = random.randint(0, 255)
      packet[10] = checksum(packet)
      send_packet(self.sock, 0x21, packet)

  def set_colour(self, red, green, blue):
      packet=bytearray([0xaa, 0x0a, 0xfc, 0x3a, 0x86, 0x01, 0x0d, 0x06, 0x01, red, green, blue, 0x20, 0x30, 0x00, 0x00, 0x0d])
      packet[14] = random.randint(0, 255)
      packet[15] = checksum(packet)
      send_packet(self.sock, 0x21, packet)

  def set_white(self, white):
      packet=bytearray([0xaa, 0x0a, 0xfc, 0x3a, 0x86, 0x01, 0x0e, 0x01, white, 0x00, 0x00, 0x0d])
      packet[9] = random.randint(0, 255)
      packet[10] = checksum(packet)
      send_packet(self.sock, 0x21, packet)

  def white_reset(self):
      packet=bytearray([0xaa, 0x0a, 0xfc, 0x3a, 0x86, 0x01, 0x0d, 0x06, 0x02, 0x80, 0x80, 0x80, 0x80, 0x80, 0x00, 0x00, 0x0d])
      packet[14] = random.randint(0, 255)
      packet[15] = checksum(packet)

  def rgb_reset(self):
      packet=bytearray([0xaa, 0x0a, 0xfc, 0x3a, 0x86, 0x01, 0x0d, 0x06, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0d])
      packet[14] = random.randint(0, 255)
      packet[15] = checksum(packet)
