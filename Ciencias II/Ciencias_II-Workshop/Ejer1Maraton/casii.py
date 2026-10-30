class ASCIIDecoder:
    def __init__(self, shift_value: int):
        self.shift_value = shift_value

    def decode_char(self, char: str) -> str:
        if char in ('\n', '\r'):
            return char
        
        return chr(ord(char) - self.shift_value)

    def decode_text(self, text: str) -> str:
        return "".join(self.decode_char(c) for c in text)


if __name__ == '__main__':
    sample_input = (
        "1JKJ'pz'{ol'{yhklthyr'vm'{ol'Jvu{yvs'Kh{h'Jvywvyh{pvu5\n"
        "1PIT'pz'h'{yhklthyr'vm'{ol'Pu{lyuh{pvuhs'Izpulzz'Thjopul' Jvywvyh{pvu5\n"
        "1KLJ'pz'{ol'{yhklthyr'vm'{ol'Kpnp{hs'Lx|pwtlu{'Jvywvyh{pvu5"
    )

    decoder = ASCIIDecoder(shift_value=7)

    decoded_message = decoder.decode_text(sample_input)

    print("--- Sample Input ---")
    print(sample_input)
    print("\n--- Sample Output ---")
    print(decoded_message)