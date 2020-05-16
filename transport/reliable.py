from network.packet import Packet
from network.unreliable import UnreliableDataTransfer
from transport import checksum
import time

ACK = True
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
        packet.set_field('Pacote', PacketNumber)
        checksum.calculate_checksum(packet)
        valid = checksum.validate_checksum(packet)
        self.udt.send(packet)

        while ACK is True:
            Loop += 1
            if Loop == 10:
                print("Resend packet - timeout")
                if valid and packet is not None:
                    ACK = False
                    self.udt.send(packet)
                Loop = 0
            time.sleep(1)
        ACK = True
        PacketNumber = PacketNumber + 1
        Loop = 0

    def receive(self):
        global ACK
        packet = self.udt.receive(timeout=800)
        valid = checksum.validate_checksum(packet)
        if packet is None:
            print("Lost packet")
            return
        else:
            ACK = False
        if valid:
            return packet.get_field('payload')
        else:
            print("invalid checksum")