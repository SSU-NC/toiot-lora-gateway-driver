class LoRaMAC:
    LORAMAC_IDLE = 0x00
    LORAMAC_STOPPED = 0x01
    LORAMAC_TX_RUNNING = 0x02
    LORAMAC_RX = 0x04
    LORAMAC_ACK_RETRY = 0x10
    LORAMAC_TX_DELAYED = 0x20
    LORAMAC_TX_CONFIG = 0x40
    LORAMAC_RX_ABORT = 0x80

    def __init__(self, _MacState):
        self.MacState = _MacState
    def get_MacState(self):
        return self.MacState
    def set_MacState(self, state):
        self.MacState &= state
