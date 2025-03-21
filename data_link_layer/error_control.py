import random

class CRC:
    def __init__(self, generator="1011"):  # Default polynomial (CRC-3)
        self.generator = generator

    def xor(self, a, b):
        """Perform XOR operation for CRC division."""
        return "".join("0" if i == j else "1" for i, j in zip(a, b))

    def crc_encode(self, data):
        """Encode data using CRC by appending the remainder."""
        data_augmented = data + "0" * (len(self.generator) - 1)  # Append zero bits
        remainder = self.crc_division(data_augmented)
        return data + remainder  # Append remainder as CRC

    def crc_division(self, data):
        """Perform binary division (mod-2) for CRC calculation."""
        divisor = self.generator
        temp = data[: len(divisor)] #If data = "1101001000" and divisor = "1011", then temp = "1101"

        for i in range(len(data) - len(divisor) + 1):
            if temp[0] == "1":
                temp = self.xor(temp, divisor) + (data[len(divisor) + i] if len(divisor) + i < len(data) else "") #If the first bit of temp is "1", XOR is performed with the divisor.
            else:
                temp = self.xor(temp, "0" * len(divisor)) + (data[len(divisor) + i] if len(divisor) + i < len(data) else "") #If the first bit of temp is "1", XOR is performed with the divisor.
            temp = temp[1:]  # Remove processed bit

        return temp  # Remainder

    def crc_check(self, received_data):
        """Verify CRC at the receiver side."""
        remainder = self.crc_division(received_data)
        return all(bit == "0" for bit in remainder)  # No errors if remainder is all zeros

    def introduce_error(self, data):
        """Introduce a random error for testing."""
        if random.random() < 0.3:  # 30% chance of error
            index = random.randint(0, len(data) - 1)
            corrupted_data = data[:index] + ("1" if data[index] == "0" else "0") + data[index + 1:] #If data = "1101001110" and index = 4, then:data[:4] = "1101", data[4] = "0" → Flipped to "1" , data[5:] = "001110"
            print(f"Error introduced at index {index}")
            return corrupted_data
        return data


# --- Simulating Transmission ---
crc = CRC()
message = "1101001"  # Binary data

# **Encoding**
encoded_crc = crc.crc_encode(message)
corrupted_crc = crc.introduce_error(encoded_crc)  # Simulating error
print(f"\nTransmitting (CRC): {encoded_crc}")
print(f"Received    (CRC): {corrupted_crc}")
print("CRC Check:", "No Errors" if crc.crc_check(corrupted_crc) else "Error Detected - Retransmit!")
