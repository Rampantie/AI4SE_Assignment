import argparse
import os
from PIL import Image, ImageDraw, ImageFont, ExifTags
from pathlib import Path
import piexif

def get_exif_date(image_path):
    """Extract date from EXIF data"""
    try:
        exif_dict = piexif.load(str(image_path))
        
        # Check for DateTimeOriginal (36867 in EXIF)
        if piexif.ExifIFD.DateTimeOriginal in exif_dict["Exif"]:
            date_str = exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal].decode('utf-8')
            return date_str.split(' ')[0].replace(':', '-')  # Format: YYYY-MM-DD
        
        # Alternative date field
        if piexif.ImageIFD.DateTime in exif_dict["0th"]:
            date_str = exif_dict["0th"][piexif.ImageIFD.DateTime].decode('utf-8')
            return date_str.split(' ')[0].replace(':', '-')
            
    except Exception as e:
        print(f"Error reading EXIF from {image_path}: {e}")
    
    return None

def calculate_position(img_width, img_height, text_width, text_height, position):
    """Calculate text position based on user input"""
    padding = 10
    if position == "top-left":
        return (padding, padding)
    elif position == "top-right":
        return (img_width - text_width - padding, padding)
    elif position == "bottom-left":
        return (padding, img_height - text_height - padding)
    elif position == "bottom-right":
        return (img_width - text_width - padding, img_height - text_height - padding)
    elif position == "center":
        return ((img_width - text_width) // 2, (img_height - text_height) // 2)
    else:
        return (padding, padding)  # Default to top-left

def add_watermark_to_image(image_path, output_dir, font_size, color, position):
    """Add watermark to a single image"""
    try:
        # Open image
        img = Image.open(image_path)
        draw = ImageDraw.Draw(img)
        
        # Get date from EXIF
        date = get_exif_date(image_path)
        if not date:
            print(f"No EXIF date found for {image_path}, skipping...")
            return False
        
        # Create font
        try:
            font = ImageFont.truetype("Arial", font_size)
        except:
            font = ImageFont.load_default()
            print("Arial font not found, using default font")
        
        # Calculate text size and position
        bbox = draw.textbbox((0, 0), date, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        text_position = calculate_position(img.width, img.height, text_width, text_height, position)
        
        # Add text watermark
        draw.text(text_position, date, font=font, fill=color)
        
        # Save watermarked image
        output_path = output_dir / image_path.name
        img.save(output_path)
        
        print(f"Watermarked: {output_path}")
        return True
        
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Add EXIF date watermarks to images")
    parser.add_argument("image_path", help="Path to image file or directory")
    parser.add_argument("--font-size", type=int, default=40, help="Font size (default: 40)")
    parser.add_argument("--color", default="white", help="Text color (default: white)")
    parser.add_argument("--position", choices=["top-left", "top-right", "bottom-left", "bottom-right", "center"],
                       default="bottom-right", help="Text position (default: bottom-right)")
    
    args = parser.parse_args()
    
    # Convert color name to RGB if needed
    color_map = {
        "white": (255, 255, 255),
        "black": (0, 0, 0),
        "red": (255, 0, 0),
        "green": (0, 255, 0),
        "blue": (0, 0, 255)
    }
    color = color_map.get(args.color.lower(), args.color)
    
    # Handle input path
    input_path = Path(args.image_path)
    
    # Create output directory
    if input_path.is_dir():
        output_dir = input_path.parent / f"{input_path.name}_watermark"
        image_files = list(input_path.glob("*.[jJ][pP][gG]")) + \
                     list(input_path.glob("*.[jJ][pP][eE][gG]")) + \
                     list(input_path.glob("*.[pP][nN][gG]")) + \
                     list(input_path.glob("*.[tT][iI][fF][fF]"))
    else:
        output_dir = input_path.parent / f"{input_path.stem}_watermark"
        image_files = [input_path]
    
    output_dir.mkdir(exist_ok=True)
    
    # Process images
    success_count = 0
    for image_file in image_files:
        if add_watermark_to_image(image_file, output_dir, args.font_size, color, args.position):
            success_count += 1
    
    print(f"Processed {success_count}/{len(image_files)} images successfully")
    print(f"Watermarked images saved to: {output_dir}")

if __name__ == "__main__":
    main()
