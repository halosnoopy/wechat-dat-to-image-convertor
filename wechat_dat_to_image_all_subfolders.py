import os
from PIL import Image
import io

def detect_xor_key(data):
    """
    Detect XOR key from the first few bytes using known image headers.
    Returns: (key, extension) or (None, None)
    """
    headers = {
        b'\xFF\xD8': 'jpg',   # JPEG
        b'\x89\x50': 'png',   # PNG
        b'\x47\x49': 'gif',   # GIF
        b'\x42\x4D': 'bmp',   # BMP
    }

    first_two = data[:2]

    for key in range(256):
        decoded_head = bytes([b ^ key for b in first_two])
        for h, ext in headers.items():
            if decoded_head == h:
                return key, ext

    return None, None


def is_valid_image(decoded_bytes):
    """
    Validate whether decoded bytes are actually a readable image.
    """
    try:
        with Image.open(io.BytesIO(decoded_bytes)) as img:
            img.verify()
        return True
    except Exception:
        return False


def decode_dat_file(dat_path, output_folder):
    """
    Decode one .dat file and save to output_folder.
    Returns True if successful, False otherwise.
    """
    try:
        with open(dat_path, 'rb') as f:
            data = f.read()

        if len(data) < 2:
            return False

        key, ext = detect_xor_key(data)
        if key is None:
            return False

        decoded = bytes([b ^ key for b in data])

        if not is_valid_image(decoded):
            return False

        base_name = os.path.splitext(os.path.basename(dat_path))[0]
        output_path = os.path.join(output_folder, f"{base_name}.{ext}")

        with open(output_path, 'wb') as out:
            out.write(decoded)

        return True

    except Exception:
        return False


def batch_decode_dat_in_folder(folder_path):
    """
    Decode all .dat files in folder_path and save them into folder_path/conv_img
    Skip files that cannot be processed.
    """
    if not os.path.isdir(folder_path):
        print(f"[ERROR] Folder not found: {folder_path}")
        return

    output_folder = os.path.join(folder_path, "conv_img")
    os.makedirs(output_folder, exist_ok=True)

    dat_files = [f for f in os.listdir(folder_path) if f.lower().endswith(".dat")]

    if not dat_files:
        print("[INFO] No .dat files found in the folder.")
        return

    success_count = 0
    skip_count = 0

    for file_name in dat_files:
        dat_path = os.path.join(folder_path, file_name)
        ok = decode_dat_file(dat_path, output_folder)

        if ok:
            print(f"[OK] Decoded: {file_name}")
            success_count += 1
        else:
            print(f"[SKIP] Could not process: {file_name}")
            skip_count += 1

    print("\nDone.")
    print(f"Decoded: {success_count}")
    print(f"Skipped: {skip_count}")
    print(f"Output folder: {output_folder}")


if __name__ == "__main__":
    folder_path = input("Enter folder path containing .dat files: ").strip()
    batch_decode_dat_in_folder(folder_path)