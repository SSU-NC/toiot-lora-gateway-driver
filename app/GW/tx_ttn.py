#!/usr/bin/env python3
import sys
from time import sleep
from SX127x.LoRa import *
from SX127x.LoRaArgumentParser import LoRaArgumentParser
from SX127x.board_config import BOARD
import LoRaWAN
from LoRaWAN.MHDR import MHDR

BOARD.setup()
parser = LoRaArgumentParser("LoRaWAN sender")

class LoRaWANsend(LoRa):
    def __init__(self, devaddr = [], nwkey = [], appkey = [], verbose = False):
        super(LoRaWANsend, self).__init__(verbose)
        self.devaddr = devaddr
        self.nwkey = nwkey
        self.appkey = appkey

    def on_tx_done(self):
        self.set_mode(MODE.STDBY)
        self.clear_irq_flags(TxDone=1)
        print("TxDone")
        self.lorawan.create(MHDR.UNCONF_DATA_DOWN, {'devaddr': devaddr, 'fcnt': 1, 'data': list(map(ord, 'Python rules!')) })
        self.write_payload(self.lorawan.to_raw())
        self.set_mode(MODE.TX)


    def start(self):
        self.lorawan = LoRaWAN.new(nwskey, appskey)
        self.lorawan.create(MHDR.UNCONF_DATA_DOWN, {'devaddr': devaddr, 'fcnt': 1, 'data': list(map(ord, 'Python rules!')) })

        self.write_payload(self.lorawan.to_raw())
        self.set_mode(MODE.TX)
        while True:
            sleep(1)


# Init
devaddr = [0x26, 0x01, 0x11, 0x5F]
nwskey = [0x00]*16
appskey = [0x00]*16
lora = LoRaWANsend(False)

# Setup
lora.set_mode(MODE.SLEEP)
lora.set_dio_mapping([1,0,0,0,0,0])
lora.set_freq(433.175)
lora.set_pa_config(pa_select=1)
lora.set_spreading_factor(8)
lora.set_pa_config(max_power=0x0F, output_power=0x0E)
lora.set_sync_word(0x34)
lora.set_rx_crc(True)

print(lora)
assert(lora.get_agc_auto_on() == 1)

try:
    print("Sending LoRaWAN message\n")
    lora.start()
except KeyboardInterrupt:
    sys.stdout.flush()
    print("\nKeyboardInterrupt")
finally:
    sys.stdout.flush()
    lora.set_mode(MODE.SLEEP)
    BOARD.teardown()
