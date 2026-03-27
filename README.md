# wechat-dat-to-image-convertor

A Python tool for converting WeChat `.dat` image files into standard image formats such as JPG and PNG.

This project supports:
- decoding a single `.dat` file
- decoding all `.dat` files in one folder
- decoding all `.dat` files under a main folder and its subfolders

Usage:
- For the single-file script, run the script and enter the `.dat` file path when prompted.
- For the folder-based scripts, run the script and enter the folder path when prompted.

After processing:
- In single-file mode, the converted image is saved in the same folder as the source `.dat` file.
- In one-folder batch mode, the converted images are saved in a new subfolder under the selected folder.
- In recursive batch mode, the converted images are saved in a new subfolder under each subfolder that contains `.dat` files.
