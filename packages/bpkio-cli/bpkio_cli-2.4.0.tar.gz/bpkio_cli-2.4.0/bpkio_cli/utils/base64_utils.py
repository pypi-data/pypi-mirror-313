import base64


def decode_base64(encoded_str):
    # Calculate how many padding characters are missing
    missing_padding = len(encoded_str) % 4
    if missing_padding != 0:
        encoded_str += "=" * (4 - missing_padding)
    # Decode the potentially padded string
    decoded_bytes = base64.b64decode(encoded_str)
    return decoded_bytes.decode("utf-8")
