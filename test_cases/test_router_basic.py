from models.router import Router

print("=== [TEST] Router Creation ===")

router = Router("R1")
router.add_interface("192.168.1.1", "AA:BB:CC:DD:EE:01")
router.add_interface("10.0.0.1", "AA:BB:CC:DD:EE:02")

router.show_interfaces()
router.show_arp_table()
