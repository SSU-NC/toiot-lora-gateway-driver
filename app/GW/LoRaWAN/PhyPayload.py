#
# lorawan packet: mhdr(1) mac_payload(1..N) mic(4)
#
from .MalformedPacketException import MalformedPacketException
from .MHDR import MHDR
from .Direction import Direction
from .MacPayload import MacPayload

class PhyPayload:

    def __init__(self, nwkey, appkey):
        self.nwkey = nwkey
        self.appkey = appkey
    
    def set_nwkey(self, _nwkey):
        self.nwkey = _nwkey
    def set_appkey(self, _appkey):
        self.appkey = _appkey

    def read(self, packet):
        if len(packet) < 12:
            raise MalformedPacketException("Invalid lorawan packet");

        print("MHDR bits: " + str(format(packet[0],'08b')))
        self.mhdr = MHDR(packet[0])
        self.set_direction()
        self.mac_payload = MacPayload()
        self.mac_payload.read(self.get_mhdr().get_mtype(), packet[1:-4])
        self.mic = packet[-4:]

    def create(self, mhdr, args):
        self.mhdr = MHDR(mhdr)
        self.set_direction()
        self.mac_payload = MacPayload()
        if 'fport' in args:
            if args['fport'] == 0x00:
                self.mac_payload.create(self.mhdr, self.get_mhdr().get_mtype(), self.nwkey, args)
            else:
                self.mac_payload.create(self.mhdr, self.get_mhdr().get_mtype(), self.appkey, args)
        else:
            self.mac_payload.create(self.mhdr, self.get_mhdr().get_mtype(), self.appkey, args)
        self.mic = None

    def length(self):
        return len(self.to_raw())

    def to_raw(self):
        phy_payload = [self.get_mhdr().to_raw()]
        phy_payload += self.mac_payload.to_raw()
        phy_payload += self.get_mic()
        return phy_payload

    def get_mhdr(self):
        return self.mhdr;

    def set_mhdr(self, mhdr):
        self.mhdr = mhdr

    def get_direction(self):
        return self.direction.get()

    def set_direction(self):
        self.direction = Direction(self.get_mhdr())

    def get_mac_payload(self):
        return self.mac_payload

    def set_mac_payload(self, mac_payload):
        self.mac_payload = mac_payload

    def get_mic(self):
        if self.mic == None:
            self.set_mic(self.compute_mic())
        return self.mic

    def set_mic(self, mic):
        self.mic = mic

    def compute_mic(self):
        if self.get_mhdr().get_mtype() == MHDR.JOIN_ACCEPT:
            return []
        else:
            return self.mac_payload.frm_payload.compute_mic(self.nwkey, self.get_direction(), self.get_mhdr())

    def valid_mic(self):
        if self.get_mhdr().get_mtype() == MHDR.JOIN_ACCEPT:
            return self.get_mic() == self.mac_payload.frm_payload.compute_mic(self.appkey, self.get_direction(), self.get_mhdr())
        else:
            return self.get_mic() == self.mac_payload.frm_payload.compute_mic(self.nwkey, self.get_direction(), self.get_mhdr())

    def get_devnonce(self):
        if self.get_mhdr().get_mtype == MHDR.JOIN_REQUEST:
            return self.mac_payload.frm_payload.get_devnonce()

    def get_devaddr(self):
        if self.get_mhdr().get_mtype() == MHDR.JOIN_ACCEPT:
            return self.mac_payload.frm_payload.get_devaddr()
        else:
            return self.mac_payload.fhdr.get_devaddr()

    def get_payload(self):
        if self.mac_payload.get_fport() == 0x00:
            return self.mac_payload.frm_payload.decrypt_payload(self.nwkey, self.get_direction(), self.mic)
        else:
            return self.mac_payload.frm_payload.decrypt_payload(self.appkey, self.get_direction(), self.mic)

    def derive_nwskey(self, devnonce):
        self.nwkey = self.mac_payload.frm_payload.derive_nwskey(self.appkey, devnonce)
        return self.nwkey

    def derive_appskey(self, devnonce):
        self.appkey = self.mac_payload.frm_payload.derive_appskey(self.appkey, devnonce)
        return self.appkey

    def get_deveui(self):
        if self.get_mhdr().get_mtype == MHDR.JOIN_REQUEST:
            return self.mac_payload.frm_payload.get_deveui()

    def get_appeui(self):
        if self.get_mhdr().get_mtype == MHDR.JOIN_REQUEST:
            return self.mac_payload.frm_payload.get_appeui()
