def encrypt_api(PAYLOAD):
    # هذه نسخة الدالة كما أرسلتها في البداية، بدون تعديل
    import base64

    def dec_to_hex(ask):
        ask_result = hex(ask)
        final_result = str(ask_result)[2:]
        if len(final_result) == 1:
            final_result = "0" + final_result
            return final_result
        else:
            return final_result

    def convert_to_hex(PAYLOAD):
        hex_payload = ''.join([f'{byte:02x}' for byte in PAYLOAD])
        return hex_payload

    def convert_to_bytes(PAYLOAD):
        payload = bytes.fromhex(PAYLOAD)
        return payload

    def xor_encrypt_decrypt(data, key=0x55):
        return bytes([b ^ key for b in data])

    # تحويل سترينج hex إلى bytes
    data_bytes = bytes.fromhex(PAYLOAD)

    # تشفير/فك تشفير عبر XOR بالرقم 0x55 (حسب كودك في بداية المحادثة)
    encrypted_bytes = xor_encrypt_decrypt(data_bytes)

    # إرجاع النتيجة كسلسلة hex
    return encrypted_bytes.hex()
