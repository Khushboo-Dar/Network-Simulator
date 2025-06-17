from .switch import Switch
from .access_control import CSMA_CD
from .error_control import CRC
from .frame import Frame
from .end_device import EndDevice

class DataLinkInterface:
    def __init__(self):
        self.switch = Switch()
        self.csma_cd = CSMA_CD()
        self.crc = CRC()

    def send(self, sender: EndDevice, receiver: EndDevice, payload: str):
        print(f"\n[DLL] Sending from {sender.name} ({sender.mac_address}) → {receiver.name} ({receiver.mac_address})")

        # 1. Encode with CRC
        codeword = self.crc.crc_encode(payload)

        # 2. Simulate error for realism
        codeword = self.crc.introduce_error(codeword)

        # 3. Create Frame
        frame = Frame(sender.mac_address, receiver.mac_address, codeword)

        # 4. Apply CSMA/CD access control
        self.csma_cd.send_frame(frame)

        # 5. Learn MACs in switch
        self.switch.learn_mac(sender.mac_address, 1)
        self.switch.learn_mac(receiver.mac_address, 2)

        # 6. Forward frame via switch
        self.switch.forward_frame(sender.mac_address, receiver.mac_address, codeword)

        # 7. CRC Check at Receiver
        if self.crc.crc_check(codeword):
            receiver.receive_frame(frame)
        else:
            print(f"[DLL] CRC Check Failed. Frame corrupted. Retransmission needed.")
