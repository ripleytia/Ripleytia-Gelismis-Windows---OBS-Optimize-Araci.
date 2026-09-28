import os
from PIL import Image, ImageEnhance

assets_dir = r"C:\Users\Ripleytia\Documents\Ripleytia_ST_Opti_V2\assets"
os.makedirs(assets_dir, exist_ok=True)

logo_src = r"C:/Users/Ripleytia/.gemini/antigravity/brain/7433f231-8750-49e5-85ce-64161799daf4/.user_uploaded/media_1790573896263.png"
bg_src = r"C:/Users/Ripleytia/.gemini/antigravity/brain/7433f231-8750-49e5-85ce-64161799daf4/.user_uploaded/media_1790573972542.jpg"

# 1. LOGO KIRPMA VE .ICO OLUŞTURMA
im_logo = Image.open(logo_src).convert("RGBA")
# True bounds: 157, 0, 518, 362 (width: 361, height: 362)
# Biraz padding vererek 370x370 kare kırpma
cx = (157 + 518) // 2  # 337
cy = (0 + 362) // 2    # 181
half_s = 185
box = (max(0, cx - half_s), max(0, cy - half_s), min(im_logo.width, cx + half_s), min(im_logo.height, cy + half_s))
cropped_logo = im_logo.crop(box)

# Kare tuvale yerleştir
square_logo = Image.new("RGBA", (370, 370), (0, 0, 0, 0))
offset_x = (370 - cropped_logo.width) // 2
offset_y = (370 - cropped_logo.height) // 2
square_logo.paste(cropped_logo, (offset_x, offset_y))

# 512x512 PNG olarak kaydet
logo_512 = square_logo.resize((512, 512), Image.Resampling.LANCZOS)
logo_path = os.path.join(assets_dir, "logo.png")
logo_512.save(logo_path, "PNG")

# Header için 48x48 ve 64x64 PNG
logo_64 = square_logo.resize((64, 64), Image.Resampling.LANCZOS)
logo_64.save(os.path.join(assets_dir, "logo_64.png"), "PNG")

# .ICO dosyası oluştur (Windows için 16, 24, 32, 48, 64, 128, 256)
ico_path = os.path.join(assets_dir, "icon.ico")
icon_sizes = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
logo_512.save(ico_path, format="ICO", sizes=icon_sizes)
print("ICO oluşturuldu:", ico_path)

# 2. ARKA PLAN RESMİ (DÜŞÜK OPAKLIKLA GOTHIC DARK PURPLE)
im_bg = Image.open(bg_src).convert("RGBA")
# Hedef boyut: 1100 x 780
bg_resized = im_bg.resize((1100, 780), Image.Resampling.LANCZOS)

# Opaklığı %12 seviyesine düşürüp koyu mor-siyah arka planla harmanla
dark_canvas = Image.new("RGBA", (1100, 780), (15, 9, 24, 255)) # #0f0918
bg_faded = Image.blend(dark_canvas, bg_resized, alpha=0.15) # %15 opaklık
bg_out_path = os.path.join(assets_dir, "bg_dark.png")
bg_faded.convert("RGB").save(bg_out_path, "PNG")
print("Arka plan oluşturuldu:", bg_out_path)
