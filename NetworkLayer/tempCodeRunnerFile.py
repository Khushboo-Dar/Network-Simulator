def receive_frame(self, frame, sender):
        sender_port = self.find_port(sender)
        if 'sender_mac' in frame:
            self.mac_table[frame['sender_mac']] = sender_port
        elif 'l2' in frame:
            self.mac_table[frame['l2']['src_mac']] = sender_port

        self.print_mac_table()

        if frame['type'] == 'ARP_REQUEST':
            for port, device in self.ports.items():
                if device != sender:
                    print(f"[{self.name}] flooding ARP Request to {device.name}")
                    device.receive_arp_request(frame)

        elif frame['type'] == 'ARP_REPLY':
            dst_mac = frame['target_mac']
            if dst_mac in self.mac_table:
                out_port = self.mac_table[dst_mac]
                dest_device = self.ports[out_port]
                print(f"[{self.name}] unicasting ARP Reply to {dest_device.name}")
                dest_device.receive_arp_reply(frame)
            else:
                print(f"[{self.name}] unknown destination MAC {dst_mac}, dropping ARP Reply")

        elif frame['type'] == 'DATA':
            dst_mac = frame['l2']['dst_mac']
            if dst_mac in self.mac_table:
                out_port = self.mac_table[dst_mac]
                dest_device = self.ports[out_port]
                print(f"[{self.name}] forwarding DATA frame to {dest_device.name}")
                dest_device.receive_data(frame)
            else:
                print(f"[{self.name}] unknown destination MAC {dst_mac}, flooding not implemented for DATA")