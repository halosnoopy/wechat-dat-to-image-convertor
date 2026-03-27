import os
from PIL import Image
import io

def decode_wechat_dat_fast(file_path, save_output=True):
    with open(file_path, 'rb') as f:
        data = f.read()

    # Known headers
    headers = {
        b'\xFF\xD8': 'jpg',
        b'\x89\x50': 'png',
        b'\x47\x49': 'gif'
    }

    # Only use first 2 bytes to find key
    first_two = data[:2]

    found_key = None
    found_ext = None

    for key in range(256):
        decoded_head = bytes([b ^ key for b in first_two])

        for h, ext in headers.items():
            if decoded_head.startswith(h):
                found_key = key
                found_ext = ext
                break

        if found_key is not None:
            break

    if found_key is None:
        print("[×] Failed to find key.")
        return

    print(f"[√] Found key: {found_key}, format: {found_ext}")

    # Decode FULL file only ONCE
    decoded = bytes([b ^ found_key for b in data])

    # Show image
    try:
        img = Image.open(io.BytesIO(decoded))
        img.show()
    except Exception as e:
        print("[!] Display failed:", e)

    # Save file
    if save_output:
        output_path = file_path + f".decoded.{found_ext}"
        with open(output_path, 'wb') as out:
            out.write(decoded)
        print(f"[√] Saved to: {output_path}")


# ---- RUN ----
if __name__ == "__main__":
    file_path = input("Enter your .dat file path: ").strip()

    if not os.path.exists(file_path):
        print("[×] File not found.")
    else:
        decode_wechat_dat_fast(file_path)