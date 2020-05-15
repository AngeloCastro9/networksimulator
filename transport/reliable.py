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
        global ACK,Loop, PacketNumber
        packet = Packet({'payload': payload})
        packet.set_field("Pacote", PacketNumber)
        checksum.calculate_checksum(packet)
        self.udt.send(packet)

        while(ACK == False):
            if(ACK == False):
                Loop += 1
                if(ACK == True):
                    break
                if(Loop == 10):
                    print("Resend packet - timeout")
                    print(packet)
                    self.udt.send(packet)
                    Loop = 0
                time.sleep(1)
            else:
                break
        ACK = False
        PacketNumber = PacketNumber + 1
        Loop = 0

    def receive(self):
        global ACK
        packet = self.udt.receive(timeout=100)
        if(packet is None):
            print("Lost packet")
            return
        else:
            ACK = True
        valid = checksum.validate_checksum(packet)
        if valid:
            return packet.get_field('payload')
        else:
            print(packet)
            print("invalid checksum")