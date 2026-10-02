"""
Script to generate the official publisher logo and icons for MoviePulse.
Guarantees 1:1 square aspect ratio and >= 96x96 px requirement for Google AMP Web Stories.
"""

from PIL import Image, ImageDraw, ImageFont
import math
import os

def create_logo(output_paths, size=512):
    # Create image with transparent or deep rich background
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Rounded rectangle background with deep dark cinema gradient
    corner_radius = size // 6
    bg_box = [(size * 0.04, size * 0.04), (size * 0.96, size * 0.96)]
    
    # Draw rounded background with dark border
    draw.rounded_rectangle(bg_box, radius=corner_radius, fill=(15, 17, 26, 255), outline=(225, 29, 72, 180), width=size // 64)

    # Draw inner subtle glowing film badge
    inner_box = [(size * 0.08, size * 0.08), (size * 0.92, size * 0.92)]
    draw.rounded_rectangle(inner_box, radius=corner_radius - 8, outline=(245, 158, 11, 80), width=size // 128)

    # Draw modern cinema clapper / play emblem
    center_x = size // 2
    center_y = size // 2 - size // 20

    # Draw film strip reels / clapper top
    clapper_width = int(size * 0.58)
    clapper_height = int(size * 0.38)
    clapper_left = center_x - clapper_width // 2
    clapper_top = center_y - clapper_height // 2

    # Draw clapper base (crimson gradient tone)
    draw.rounded_rectangle(
        [(clapper_left, clapper_top + clapper_height // 4), (clapper_left + clapper_width, clapper_top + clapper_height)],
        radius=14,
        fill=(225, 29, 72, 255),
        outline=(255, 255, 255, 100),
        width=3
    )

    # Draw clapper slate stripes on top
    slate_top = clapper_top
    slate_bottom = clapper_top + clapper_height // 4
    draw.rounded_rectangle(
        [(clapper_left, slate_top), (clapper_left + clapper_width, slate_bottom)],
        radius=8,
        fill=(30, 41, 59, 255),
        outline=(255, 255, 255, 180),
        width=3
    )

    # Stripes on the slate
    stripe_w = clapper_width // 5
    for i in range(5):
        if i % 2 == 1:
            sx = clapper_left + i * stripe_w
            draw.polygon([
                (sx, slate_top + 3),
                (sx + stripe_w - 6, slate_top + 3),
                (sx + stripe_w - 14, slate_bottom - 3),
                (sx - 8, slate_bottom - 3)
            ], fill=(255, 255, 255, 230))

    # Draw a vibrant golden play triangle in center of clapper base
    play_size = int(size * 0.12)
    play_cx = center_x + play_size // 6
    play_cy = center_y + clapper_height // 8
    p1 = (play_cx + play_size, play_cy)
    p2 = (play_cx - play_size // 2, play_cy - int(play_size * 0.866))
    p3 = (play_cx - play_size // 2, play_cy + int(play_size * 0.866))
    draw.polygon([p1, p2, p3], fill=(251, 191, 36, 255))

    # Text at the bottom: "MOVIEPULSE"
    # Using built-in font rendering or geometric lettering
    text_y = int(size * 0.76)
    
    # Try to load a clean TTF font if available, otherwise use bold default text
    font_loaded = False
    try:
        # Check standard Windows fonts
        for font_path in [
            "C:/Windows/Fonts/segoeuib.ttf",
            "C:/Windows/Fonts/arialbd.ttf",
            "C:/Windows/Fonts/calibrib.ttf",
        ]:
            if os.path.exists(font_path):
                font = ImageFont.truetype(font_path, int(size * 0.082))
                sub_font = ImageFont.truetype(font_path, int(size * 0.042))
                font_loaded = True
                break
    except Exception:
        font_loaded = False

    if font_loaded:
        title = "MOVIEPULSE"
        bbox = draw.textbbox((0, 0), title, font=font)
        tw = bbox[2] - bbox[0]
        draw.text((center_x - tw // 2, text_y), title, font=font, fill=(255, 255, 255, 255))

        subtitle = "WEB STORIES"
        sub_bbox = draw.textbbox((0, 0), subtitle, font=sub_font)
        stw = sub_bbox[2] - sub_bbox[0]
        draw.text((center_x - stw // 2, text_y + int(size * 0.09)), subtitle, font=sub_font, fill=(245, 158, 11, 230))
    else:
        # Fallback text
        draw.text((center_x - size // 4, text_y), "MOVIEPULSE", fill=(255, 255, 255, 255))

    # Save to all destination paths
    for path in output_paths:
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        img.save(path, format="PNG")
        print(f"Generated publisher logo: {path} ({size}x{size} px)")

if __name__ == "__main__":
    create_logo(["assets/logo.png", "dist/assets/logo.png"], size=512)
