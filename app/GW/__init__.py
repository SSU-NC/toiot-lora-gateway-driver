#!/usr/bin/env python3
from time import sleep
from SX127x.LoRa import *
from SX127x.LoRaArgumentParser import LoRaArgumentParser
from SX127x.board_config import BOARD

import paho.mqtt.client as mqtt

import getmac

from .setup import args
from .LoRaWAN import *

BOARD.setup()
parser = LoRaArgumentParser("LoRaWAN receiver")

class LoRaWANrcv(LoRa):
    def __init__(self, verbose = False):
        super(LoRaWANrcv, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([0]*6)

    def on_rx_done(self):
        print("-------------------------------------RxDone")
        self.clear_irq_flags(RxDone=1)
        payload = self.read_payload(nocheck=True)
        print("".join(format(x, '02x') for x in bytes(payload)))
        lorawan = LoRaWAN.new(nwskey, appskey)
        lorawan.read(payload)
        print("mhdr.mversion: "+str(format(lorawan.get_mhdr().get_mversion(), '08b')))
        print("mhdr.mtype: "+str(format(lorawan.get_mhdr().get_mtype(), '08b')))
        print("mic: "+str(lorawan.get_mic()))
        print("valid mic: "+str(lorawan.valid_mic()))
        print("received message: "+"".join(list(map(chr, lorawan.get_payload()))))
        mqttclient.publish("".join(list(map(chr, lorawan.get_payload()))))
        print("--------------------------------------------\n")

        self.set_mode(MODE.SLEEP)
        self.reset_ptr_rx()
        
        self.set_mode(MODE.RXCONT)
    def start(self):
        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)
        while True:
            sleep(.1)
            sys.stdout.flush()

def Init_client(cname):
    # callback assignment
    client = mqtt.Client(cname, False) #do not use clean session
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    client.on_publish = on_publish
    client.on_subscribe = on_subscribe
    client.on_unsubscribe = on_unsubscribe
    client.topic_ack = []
    client.run_flag = False
    client.running_loop = False
    client.subscribe_flag = False
    client.bad_connection_flag = False
    client.connected_flag = False
    client.disconnect_flag = False
    return client

def on_message(client, userdata, message):
    print("[MQTT] Received message: ",str(message.payload.decode("utf-8")),\
            "| topic: ",message.topic," | retained: ",message.retain)
    if message.retain == 1:
        print("[MQTT] This is a retained message..")

def on_publish(client, userdata, result):
    print("[MQTT] Data Published via MQTT..")
    pass

def on_subscribe(client, userdata, mid, granted_qos):
    if mid != 0:
        print("[MQTT] Subscribe Failed..")
def on_unsubscribe(client, userdata, mid):
    print("[MQTT] Successfully unsubscribed..")

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.connected_flag=True
        print("[MQTT] Successfully connected..[Returned Code="+str(rc)+"]")
    else:
        print("[MQTT] Bad connection..[Returned Code="+str(rc)+"]")
        client.bad_connection_flag=True

def on_disconnect(client, userdata, rc):
    client.disconnect()
    print("[MQTT] Client disconnected..")
    logging.info("[MQTT] Disconnecting reason: "+str(rc))
    client.connected_flag=False
    client.disconnect_flag=True

# Init
#nwskey = [0xC3, 0x24, 0x64, 0x98, 0xDE, 0x56, 0x5D, 0x8C, 0x55, 0x88, 0x7C, 0x05, 0x86, 0xF9, 0x82, 0x26]
#appskey = [0x15, 0xF6, 0xF4, 0xD4, 0x2A, 0x95, 0xB0, 0x97, 0x53, 0x27, 0xB7, 0xC1, 0x45, 0x6E, 0xC5, 0x45]
nwskey = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
appskey = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]




mqttclient = Init_client("lora-GW-" + str(getmac.get_mac_address()))
mqttclient.connect(args.b, args.p)
#mqttclient.loop_start()
print("[MQTT] Connecting to broker ", args.b)
try:
    mqttclient.connect(args.b, args.p)
except:
    print("[MQTT] [ERROR]:Connection failed!")
    exit(1)
'''
while not mqttclient.connected_flag and not mqttclient.bad_connection_flag:
    print("[MQTT] Waiting for connection...")
    sleep(1)
if mqttclient.bad_connection_flag:
    mqttclient.loop_stop()
    sys.exit()
'''


lora = LoRaWANrcv(verbose=False)
lora.set_mode(MODE.STDBY)
lora.set_dio_mapping([0] * 6)
lora.set_freq(433.175)
lora.set_pa_config(pa_select=1)
lora.set_spreading_factor(8)
#lora.set_sync_word(0x34)
lora.set_rx_crc(True)

print(lora)
assert(lora.get_agc_auto_on() == 1)
try:
    print("[LoRaWAN] Waiting for incoming LoRaWAN messages\n")
    lora.start()
except KeyboardInterrupt:
    sys.stdout.flush()
    print("\nKeyboardInterrupt")
finally:
    sys.stdout.flush()
    lora.set_mode(MODE.SLEEP)
    BOARD.teardown()
