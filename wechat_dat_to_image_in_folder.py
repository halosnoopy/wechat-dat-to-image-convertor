import os
import io
from PIL import Image

def detect_xor_key(data):
    """
    Detect the XOR key using known image headers.
    Returns (key, extension) or (None, None)
    """
    headers = {
        b'\xFF\xD8': 'jpg',   # JPEG
        b'\x89\x50': 'png',   # PNG
        b'\x47\x49': 'gif',   # GIF
        b'\x42\x4D': 'bmp',   # BMP
        b'\x49\x49': 'tif',   # TIFF little-endian
        b'\x4D\x4D': 'tif',   # TIFF big-endian
    }

    if len(data) < 2:
        return None, None

    first_two = data[:2]

    for key in range(256):
        decoded_head = bytes([b ^ key for b in first_two])
        for header, ext in headers.items():
            if decoded_head == header:
                return key, ext

    return None, None


def is_valid_image(decoded_bytes):
    """
    Check whether the decoded bytes form a valid image.
    """
    try:
        with Image.open(io.BytesIO(decoded_bytes)) as img:
            img.verify()
        return True
    except Exception:
        return False


def get_unique_output_path(output_dir, base_name, ext):
    """
    Avoid overwriting files with the same name.
    """
    output_path = os.path.join(output_dir, f"{base_name}.{ext}")
    if not os.path.exists(output_path):
        return output_path

    counter = 1
    while True:
        output_path = os.path.join(output_dir, f"{base_name}_{counter}.{ext}")
        if not os.path.exists(output_path):
            return output_path
        counter += 1


def decode_dat_file(dat_path, output_dir):
    """
    Decode one .dat file and save it into output_dir.
    Returns True if successful, False otherwise.
    """
    try:
        with open(dat_path, "rb") as f:
            data = f.read()

        key, ext = detect_xor_key(data)
        if key is None:
            return False

        decoded = bytes(b ^ key for b in data)

        if not is_valid_image(decoded):
            return False

        base_name = os.path.splitext(os.path.basename(dat_path))[0]
        output_path = get_unique_output_path(output_dir, base_name, ext)

        with open(output_path, "wb") as f:
            f.write(decoded)

        return True

    except Exception:
        return False


def process_root_folder(root_folder):
    """
    Walk through all subfolders under root_folder.
    For each folder containing .dat files, create an 'img_c' subfolder there
    and save decoded images into it.
    """
    if not os.path.isdir(root_folder):
        print(f"[ERROR] Folder does not exist: {root_folder}")
        return

    total_success = 0
    total_skipped = 0
    total_dat_files = 0
    folders_processed = 0

    for current_root, dirs, files in os.walk(root_folder):
        # Prevent scanning inside output folders
        dirs[:] = [d for d in dirs if d != "img_c"]

        dat_files = [f for f in files if f.lower().endswith(".dat")]

        if not dat_files:
            continue

        folders_processed += 1
        output_dir = os.path.join(current_root, "img_c")
        os.makedirs(output_dir, exist_ok=True)

        print(f"\n[Folder] {current_root}")
        print(f"  Found {len(dat_files)} .dat file(s)")

        folder_success = 0
        folder_skipped = 0

        for file_name in dat_files:
            total_dat_files += 1
            dat_path = os.path.join(current_root, file_name)

            ok = decode_dat_file(dat_path, output_dir)

            if ok:
                print(f"  [OK]   {file_name}")
                folder_success += 1
                total_success += 1
            else:
                print(f"  [SKIP] {file_name}")
                folder_skipped += 1
                total_skipped += 1

        print(f"  Saved decoded images to: {output_dir}")
        print(f"  Folder summary -> decoded: {folder_success}, skipped: {folder_skipped}")

    print("\n========== ALL DONE ==========")
    print(f"Folders with .dat files: {folders_processed}")
    print(f"Total .dat files found:  {total_dat_files}")
    print(f"Total decoded:           {total_success}")
    print(f"Total skipped:           {total_skipped}")


if __name__ == "__main__":
    root_folder = input("Enter the root folder path: ").strip().strip('"')
    process_root_folder(root_folder)