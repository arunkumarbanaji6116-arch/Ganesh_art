import os
from PIL import Image, ImageDraw, ImageFont

def make_card():
    qr_img = Image.open("qr_arun.png").convert("RGBA")
    qr_img = qr_img.resize((320, 320), Image.Resampling.NEAREST)

    width, height = 520, 640
    card = Image.new("RGBA", (width, height), (15, 10, 22, 255))
    draw = ImageDraw.Draw(card)

    # Draw luxury gold border
    draw.rectangle([8, 8, width - 8, height - 8], outline=(255, 215, 0, 180), width=2)
    draw.rectangle([14, 14, width - 14, height - 14], outline=(255, 140, 0, 90), width=1)

    # Fonts
    try:
        font_title = ImageFont.truetype("arialbd.ttf", 26)
        font_author = ImageFont.truetype("arialbd.ttf", 20)
        font_url = ImageFont.truetype("arialbd.ttf", 18)
        font_tip = ImageFont.truetype("arial.ttf", 14)
    except Exception:
        font_title = ImageFont.load_default()
        font_author = font_title
        font_url = font_title
        font_tip = font_title

    # Header
    title_text = "LORD GANESHA ART"
    author_text = "ARUN"
    
    # Measure text
    bbox_t = draw.textbbox((0, 0), title_text, font=font_title)
    t_w = bbox_t[2] - bbox_t[0]
    draw.text(((width - t_w) // 2, 35), title_text, fill=(255, 220, 120), font=font_title)

    bbox_a = draw.textbbox((0, 0), author_text, font=font_author)
    a_w = bbox_a[2] - bbox_a[0]
    draw.text(((width - a_w) // 2, 75), author_text, fill=(255, 215, 0), font=font_author)

    # QR container box (white with soft rounded feel)
    qr_box = [ (width - 340) // 2, 120, (width + 340) // 2, 460 ]
    draw.rectangle(qr_box, fill=(255, 255, 255, 255), outline=(255, 215, 0, 220), width=3)
    
    # Paste QR code centered in box
    card.paste(qr_img, ((width - 320) // 2, 130), qr_img)

    # URL box
    url_box = [30, 485, width - 30, 535]
    draw.rectangle(url_box, fill=(25, 18, 38, 255), outline=(255, 215, 0, 140), width=1)
    url_text = "https://spoo.me/arun-ganesh-art"
    bbox_u = draw.textbbox((0, 0), url_text, font=font_url)
    u_w = bbox_u[2] - bbox_u[0]
    draw.text(((width - u_w) // 2, 498), url_text, fill=(255, 245, 180), font=font_url)

    # Tip at bottom
    tip_text = "Scan to Open Directly (No IP / No Password Needed!)"
    bbox_tip = draw.textbbox((0, 0), tip_text, font=font_tip)
    tip_w = bbox_tip[2] - bbox_tip[0]
    draw.text(((width - tip_w) // 2, 560), tip_text, fill=(180, 230, 200), font=font_tip)

    rotate_tip = "Rotate phone to Landscape mode for best experience"
    bbox_rtip = draw.textbbox((0, 0), rotate_tip, font=font_tip)
    rtip_w = bbox_rtip[2] - bbox_rtip[0]
    draw.text(((width - rtip_w) // 2, 585), rotate_tip, fill=(255, 200, 80), font=font_tip)

    # Save to workspace and artifact directory
    card_rgb = card.convert("RGB")
    card_rgb.save("mobile_qr.png")
    print("Saved mobile_qr.png successfully!")

if __name__ == "__main__":
    make_card()
