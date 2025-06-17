from NetworkLayer.host import Host
from NetworkLayer.router import Router
from data_link_layer.data_link import DataLinkInterface

class NetworkInterface:
    def __init__(self):
        self.dll = DataLinkInterface()

    def send(self, sender, dest_ip, payload):
        """
        sender: Host or Router object
        dest_ip: destination IP address as string
        payload: application data to deliver
        """
        print(f"\n[NET] Initiating packet send from {sender.name} to {dest_ip}")

        # Build pseudo frame (used only for ARP/routing flow)
        sender.send_data(dest_ip)

        # Actual payload goes into a DATA frame — injected via the same flow
        frame = {
            'type': 'DATA',
            'l2': {'src_mac': sender.mac, 'dst_mac': 'FF:FF:FF:FF:FF:FF'},  # Dummy initially
            'l3': {'src_ip': sender.ip, 'dst_ip': dest_ip, 'payload': payload}
        }

        # Inject into switch like normal routing flow
        if hasattr(sender, 'connected_switch'):
            sender.connected_switch.receive_frame(frame, sender)
        else:
            raise Exception("[NET] Sender must be connected to a switch.")
