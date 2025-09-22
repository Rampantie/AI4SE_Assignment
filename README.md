# AI4SE_Assignment

## Photo Date Watermarker

**This program:**

1. Takes an image file path or directory path as input
2. Extracts the EXIF date information using the piexif library
3. Allows customization of font size, color, and position through command-line arguments
4. Adds the date watermark to all supported images in the directory
5. Saves watermarked images to a new subdirectory with the "_watermark" suffix

**To use this program:**

Install required libraries: 

```shell
pip install Pillow piexif
```

Run the script (example): 

```shell
python main.py /path/to/images --font-size 30 --color white --position bottom-right
```

The program supports common image formats (JPEG, PNG, TIFF) and will create a new directory with watermarked versions of all images in the input picture directory.

