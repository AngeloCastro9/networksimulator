from network.packet import Packet
from network.unreliable import UnreliableDataTransfer
from transport import checksum
import time

ACK = False
Loop = 0
PacketNumber = 0


class ReliableDataTransfer:

    def __init__(self, udt):
        if not isinstance(udt, UnreliableDataTransfer):
            raise Exception("udt parameter must be an instance of UnreliableDataTransfer")
        self.udt = udt

    def send(self, payload):
        global ACK, Loop, PacketNumber
        packet = Packet({'payload': payload})
        packet.set_field("Pacote", PacketNumber)
        checksum.calculate_checksum(packet)
        self.udt.send(packet)

        while (ACK == False):
            if (Loop == 10):
                print("timeout - resend")
                self.udt.send(packet)
                Loop = 0
            Loop += 1
            time.sleep(1)
        ACK = False
        PacketNumber = PacketNumber + 1
        Loop = 0

    def receive(self):
        global ACK
        packet = self.udt.receive(timeout=1000)
        while packet is None:
            packet = self.udt.receive(timeout=100)
        valid = checksum.validate_checksum(packet)
        while valid is not True:
            if valid is False:
                print("invalid checksum")
            packet = self.udt.receive(timeout=1000)
            valid = checksum.validate_checksum(packet)

            if valid:
                ACK = True
                return packet.get_field('payload')