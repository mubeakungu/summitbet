import math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 640, 420
OUT = "static/img/games"

def font(size, bold=True):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for p in paths:
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            continue
    return ImageFont.load_default()

def lerp(a, b, t):
    return tuple(int(a[i] + (b[i]-a[i])*t) for i in range(3))

def hexrgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def vertical_gradient(size, top, bottom):
    w, h = size
    img = Image.new("RGB", size)
    for y in range(h):
        t = y / (h - 1)
        c = lerp(top, bottom, t)
        ImageDraw.Draw(img).line([(0, y), (w, y)], fill=c)
    return img

def radial_glow(img, center, radius, color, alpha=110):
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    d.ellipse([center[0]-radius, center[1]-radius, center[0]+radius, center[1]+radius],
              fill=color+(alpha,))
    overlay = overlay.filter(ImageFilter.GaussianBlur(radius//2))
    img.paste(Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB"), (0, 0))

def noise_specks(draw, n, area, color, size_range=(1, 3)):
    for _ in range(n):
        x = random.randint(area[0], area[2])
        y = random.randint(area[1], area[3])
        r = random.randint(*size_range)
        draw.ellipse([x-r, y-r, x+r, y+r], fill=color)

def badge(draw, text, xy, fg, bg):
    f = font(20)
    pad = 10
    tw = draw.textlength(text, font=f)
    x, y = xy
    draw.rounded_rectangle([x, y, x+tw+pad*2, y+34], radius=8, fill=bg)
    draw.text((x+pad, y+6), text, font=f, fill=fg)

def base_card(top_hex, bottom_hex):
    img = vertical_gradient((W, H), hexrgb(top_hex), hexrgb(bottom_hex))
    return img

def dashed_curve(draw, points, color, width=6, dash=14, gap=10):
    for i in range(len(points)-1):
        x1, y1 = points[i]
        x2, y2 = points[i+1]
        dist = math.hypot(x2-x1, y2-y1)
        steps = max(1, int(dist / (dash+gap)))
        for s in range(steps):
            t0 = s/steps
            t1 = min(1, t0 + dash/dist) if dist else 1
            p0 = (x1+(x2-x1)*t0, y1+(y2-y1)*t0)
            p1 = (x1+(x2-x1)*t1, y1+(y2-y1)*t1)
            draw.line([p0, p1], fill=color, width=width)

def save(img, slug):
    img.save(f"{OUT}/{slug}.png", "PNG", optimize=True)
    print("wrote", slug)

# ---------- CRASH GAMES ----------

def aviator():
    img = base_card("#173025", "#0a1712")
    d = ImageDraw.Draw(img)
    radial_glow(img, (480, 120), 160, (63, 174, 122)); d = ImageDraw.Draw(img)
    pts = [(60, 340), (180, 300), (300, 220), (420, 150), (520, 100)]
    dashed_curve(d, pts, (120, 230, 170), width=5)
    px, py = 520, 100
    d.polygon([(px-46, py+10), (px+34, py-6), (px+46, py), (px+34, py+6), (px-46, py+22)], fill=(235, 245, 240))
    d.polygon([(px-6, py-4), (px+2, py-34), (px+10, py-4)], fill=(235, 245, 240))
    d.polygon([(px-16, py+14), (px-8, py+34), (px+2, py+14)], fill=(200, 220, 212))
    d.ellipse([px-52, py+2, px-42, py+12], fill=(235, 245, 240))
    f = font(46)
    d.text((70, 40), "2.34x", font=f, fill=(120, 235, 175))
    badge(d, "DEMO", (24, H-58), (20, 30, 24), (255, 255, 255))
    save(img, "aviator")

def jetx():
    img = base_card("#101c33", "#060c18")
    d = ImageDraw.Draw(img)
    radial_glow(img, (470, 110), 170, (95, 179, 217))
    d = ImageDraw.Draw(img)
    pts = [(50, 350), (170, 300), (290, 230), (410, 160), (500, 100)]
    dashed_curve(d, pts, (150, 210, 240), width=5)
    px, py = 500, 100
    d.polygon([(px-50, py+16), (px+40, py-4), (px+50, py+4), (px+40, py+12), (px-50, py+28)], fill=(225, 240, 250))
    d.polygon([(px-56, py+8), (px-40, py+2), (px-40, py+26), (px-56, py+22)], fill=(255, 150, 60))
    d.ellipse([px-2, py-2, px+18, py+18], fill=(90, 200, 255))
    f = font(46)
    d.text((70, 40), "3.5x", font=f, fill=(140, 220, 255))
    badge(d, "DEMO", (24, H-58), (10, 20, 35), (255, 255, 255))
    save(img, "jetx")

def plinko():
    img = base_card("#1b1330", "#0a0716")
    d = ImageDraw.Draw(img)
    rows = 7
    top_y = 90
    for r in range(rows):
        n = r + 3
        y = top_y + r*32
        start_x = W/2 - (n-1)*32/2
        for c in range(n):
            x = start_x + c*32
            d.ellipse([x-6, y-6, x+6, y+6], fill=(190, 160, 255))
    slot_colors = [(255,120,120),(255,180,110),(255,225,120),(160,230,150),(160,230,150),(255,225,120),(255,180,110),(255,120,120)]
    sw = W / len(slot_colors)
    for i, c in enumerate(slot_colors):
        d.rectangle([i*sw+3, H-70, (i+1)*sw-3, H-20], fill=c)
    f = font(30)
    d.text((36, 30), "PLINKO", font=f, fill=(230, 210, 255))
    save(img, "plinko")

def mines():
    img = base_card("#241a12", "#0f0a06")
    d = ImageDraw.Draw(img)
    grid = 5
    margin = 60
    cell = (W - margin*2) / grid
    random.seed(3)
    gems = random.sample(range(grid*grid), 5)
    for i in range(grid*grid):
        r, c = divmod(i, grid)
        x0 = margin + c*cell + 5
        y0 = 60 + r*cell + 5
        x1 = margin + (c+1)*cell - 5
        y1 = 60 + (r+1)*cell - 5
        d.rounded_rectangle([x0, y0, x1, y1], radius=10, fill=(58, 44, 30))
        cx, cy = (x0+x1)/2, (y0+y1)/2
        if i in gems:
            d.polygon([(cx, cy-16), (cx+16, cy), (cx, cy+16), (cx-16, cy)], fill=(120, 220, 255))
        else:
            d.text((cx-8, cy-12), "?", font=font(22), fill=(150, 130, 100))
    save(img, "mines")

def chicken_road():
    img = base_card("#3a2410", "#160d05")
    d = ImageDraw.Draw(img)
    for i in range(6):
        y = 340 - i*40
        d.rectangle([40+i*90, y, 40+i*90+70, y+18], fill=(200, 140, 70))
    cx, cy = 300, 210
    d.ellipse([cx-30, cy-30, cx+30, cy+30], fill=(230, 90, 60))
    d.polygon([(cx+22, cy-6), (cx+42, cy), (cx+22, cy+6)], fill=(255, 200, 60))
    d.ellipse([cx-14, cy-38, cx+2, cy-22], fill=(230, 90, 60))
    d.polygon([(cx-24, cy+26), (cx-14, cy+50), (cx-4, cy+26)], fill=(255, 180, 40))
    radial_glow(img, (500, 100), 120, (255, 150, 60))
    save(img, "chicken-road")

def dragon_tower():
    img = base_card("#241206", "#0d0602")
    d = ImageDraw.Draw(img)
    radial_glow(img, (470, 90), 150, (255, 120, 40), alpha=140)
    d = ImageDraw.Draw(img)
    cx = W/2
    for i in range(6):
        y0 = H - 40 - i*48
        y1 = y0 + 40
        w = 90 - i*8
        d.rectangle([cx-w/2, y0, cx+w/2, y1], fill=(70+i*5, 40, 20))
        d.rectangle([cx-w/2, y0, cx+w/2, y0+6], fill=(120, 70, 30))
    d.polygon([(cx-60, H-260), (cx, H-320), (cx+60, H-260)], fill=(90, 30, 20))
    d.polygon([(cx-60, H-40), (cx-90, H+10), (cx+90, H+10), (cx+60, H-40)], fill=(30, 15, 10))
    f = font(30)
    d.text((30, 30), "DRAGON TOWER", font=f, fill=(255, 170, 90))
    save(img, "dragon-tower")

# ---------- SLOTS ----------

def sweet_bonanza():
    img = base_card("#4a1550", "#1c0620")
    d = ImageDraw.Draw(img)
    random.seed(5)
    colors = [(255,120,150),(255,200,80),(140,220,255),(180,255,150),(255,255,255)]
    for _ in range(20):
        x = random.randint(30, W-30)
        y = random.randint(30, H-30)
        c = random.choice(colors)
        r = random.randint(14, 26)
        shape = random.choice(["circle", "diamond"])
        if shape == "circle":
            d.ellipse([x-r, y-r, x+r, y+r], fill=c)
            d.ellipse([x-r+r/3, y-r+r/3, x-r+r, y-r+r], fill=(255,255,255,120))
        else:
            d.polygon([(x, y-r), (x+r, y), (x, y+r), (x-r, y)], fill=c)
    save(img, "sweet-bonanza")

def wolf_gold():
    img = base_card("#0f1c22", "#03080a")
    d = ImageDraw.Draw(img)
    d.ellipse([440, 40, 550, 150], fill=(238, 232, 205))
    radial_glow(img, (495, 95), 120, (230, 220, 180), alpha=100)
    d = ImageDraw.Draw(img)
    # distant hills
    d.polygon([(0, 330), (150, 260), (300, 320), (460, 250), (W, 300), (W, H), (0, H)], fill=(20, 34, 30))
    # wolf head silhouette (side profile, howling)
    cx, cy = 230, 300
    d.polygon([
        (cx-70, cy+60),      # back of neck
        (cx-40, cy-10),      # top of head
        (cx-10, cy-70),      # ear tip back
        (cx+2, cy-20),       # ear notch
        (cx+18, cy-90),      # ear tip front
        (cx+28, cy-30),      # forehead
        (cx+80, cy-50),      # snout top
        (cx+96, cy-20),      # nose
        (cx+70, cy-4),       # mouth
        (cx+40, cy+10),      # jaw
        (cx+40, cy+60),      # chest
    ], fill=(30, 40, 46))
    d.ellipse([cx+20, cy-30, cx+30, cy-20], fill=(230, 220, 180))
    f = font(30)
    d.text((30, 30), "WOLF GOLD", font=f, fill=(230, 220, 180))
    save(img, "wolf-gold")

def sugar_rush():
    img = base_card("#2a1040", "#0e0420")
    d = ImageDraw.Draw(img)
    grid = 3
    margin = 90
    cell = (W - margin*2) / grid
    colors = [(255,100,140),(120,220,255),(255,210,90),(160,255,160),(255,140,220),(255,255,255),(255,170,90),(150,190,255),(255,120,120)]
    for i in range(grid*grid):
        r, c = divmod(i, grid)
        x0 = margin + c*cell + 8
        y0 = 60 + r*cell + 8
        x1 = margin + (c+1)*cell - 8
        y1 = 60 + (r+1)*cell - 8
        d.rounded_rectangle([x0, y0, x1, y1], radius=14, fill=(40, 20, 60))
        cx, cy = (x0+x1)/2, (y0+y1)/2
        rr = min(x1-x0, y1-y0)/2 - 14
        d.ellipse([cx-rr, cy-rr, cx+rr, cy+rr], fill=colors[i % len(colors)])
    save(img, "sugar-rush")

def big_bass_bonanza():
    img = base_card("#0c2a3a", "#03121c")
    d = ImageDraw.Draw(img)
    for i in range(4):
        y = 320 + i*10
        d.line([(0, y), (W, y-10)], fill=(20, 60, 80), width=6)
    cx, cy = 320, 220
    d.polygon([(cx-100, cy), (cx+60, cy-60), (cx+60, cy+60)], fill=(70, 150, 170))
    d.polygon([(cx+60, cy-40), (cx+120, cy), (cx+60, cy+40)], fill=(70, 150, 170))
    d.ellipse([cx-90, cy-16, cx-60, cy+14], fill=(20, 40, 50))
    d.arc([cx-40, cy-40, cx+40, cy+40], start=200, end=340, fill=(220, 240, 245), width=4)
    f = font(30)
    d.text((30, 30), "BIG BASS", font=f, fill=(160, 220, 235))
    save(img, "big-bass-bonanza")

def gates_of_olympus():
    img = base_card("#241040", "#0c0420")
    d = ImageDraw.Draw(img)
    radial_glow(img, (320, 90), 180, (255, 210, 100), alpha=130)
    d = ImageDraw.Draw(img)
    base_y = 300
    for i in range(6):
        x = 90 + i*90
        d.rectangle([x, 140, x+26, base_y], fill=(210, 200, 220))
        d.polygon([(x-6, 140), (x+32, 140), (x+13, 116)], fill=(230, 220, 235))
    d.rectangle([60, base_y, W-60, base_y+22], fill=(190, 180, 205))
    random.seed(2)
    for _ in range(10):
        x = random.randint(40, W-40)
        y = random.randint(base_y+40, H-20)
        r = random.randint(6, 12)
        d.ellipse([x-r, y-r, x+r, y+r], fill=(255, 210, 90))
    f = font(28)
    d.text((30, 30), "GATES OF OLYMPUS", font=f, fill=(255, 220, 140))
    save(img, "gates-of-olympus")

def fortune_tiger():
    img = base_card("#3a0d10", "#160305")
    d = ImageDraw.Draw(img)
    radial_glow(img, (480, 100), 150, (255, 190, 60), alpha=120)
    d = ImageDraw.Draw(img)
    cx, cy = 300, 250
    d.ellipse([cx-90, cy-70, cx+90, cy+70], fill=(240, 160, 40))
    d.polygon([(cx-90, cy-30), (cx-140, cy-70), (cx-70, cy-50)], fill=(240, 160, 40))
    d.polygon([(cx+90, cy-30), (cx+140, cy-70), (cx+70, cy-50)], fill=(240, 160, 40))
    for i in range(4):
        d.line([(cx-70+i*20, cy-40), (cx-40+i*20, cy+40)], fill=(30, 15, 10), width=6)
    d.ellipse([cx-24, cy-10, cx-6, cy+8], fill=(20, 10, 5))
    d.ellipse([cx+6, cy-10, cx+24, cy+8], fill=(20, 10, 5))
    f = font(28)
    d.text((30, 30), "FORTUNE TIGER", font=f, fill=(255, 210, 130))
    save(img, "fortune-tiger")

def book_of_dead():
    img = base_card("#2a2008", "#0f0b02")
    d = ImageDraw.Draw(img)
    radial_glow(img, (470, 100), 150, (230, 190, 90), alpha=110)
    d = ImageDraw.Draw(img)
    cx, cy = 300, 240
    d.polygon([(cx-110, cy-70), (cx, cy-100), (cx+110, cy-70), (cx+110, cy+80), (cx, cy+110), (cx-110, cy+80)], fill=(70, 40, 15))
    d.line([(cx, cy-100), (cx, cy+110)], fill=(30, 15, 5), width=4)
    for i in range(4):
        y = cy - 40 + i*30
        d.line([(cx-70, y), (cx-15, y-6)], fill=(230, 190, 90), width=3)
        d.line([(cx+15, y-6), (cx+70, y)], fill=(230, 190, 90), width=3)
    d.ellipse([cx-16, cy-70, cx+16, cy-38], outline=(230, 190, 90), width=4)
    f = font(28)
    d.text((30, 30), "BOOK OF DEAD", font=f, fill=(230, 195, 120))
    save(img, "book-of-dead")

def money_train_3():
    img = base_card("#101418", "#04060a")
    d = ImageDraw.Draw(img)
    radial_glow(img, (500, 90), 140, (120, 220, 150), alpha=110)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([80, 220, 320, 300], radius=16, fill=(60, 60, 70))
    d.rounded_rectangle([300, 190, 460, 300], radius=16, fill=(70, 70, 82))
    for x in [140, 200, 260, 340, 400]:
        d.ellipse([x-24, 300, x+24, 348], fill=(20, 20, 25))
        d.ellipse([x-10, 314, x+10, 334], fill=(90, 90, 100))
    d.rectangle([320, 210, 400, 250], fill=(120, 220, 150))
    for i in range(6):
        d.line([(460+i*10, 200-i*4), (500+i*10, 200-i*4)], fill=(150, 230, 170), width=3)
    f = font(28)
    d.text((30, 30), "MONEY TRAIN 3", font=f, fill=(140, 230, 165))
    save(img, "money-train-3")

for fn in [aviator, jetx, plinko, mines, chicken_road, dragon_tower,
           sweet_bonanza, wolf_gold, sugar_rush, big_bass_bonanza,
           gates_of_olympus, fortune_tiger, book_of_dead, money_train_3]:
    fn()

print("done")
