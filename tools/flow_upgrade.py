"""Wellness Daily: upgrade queued text posts with Google Flow media.

hook(clip, reel, line1, line2, out)
    First 6 s of a Flow clip (720x1280 or larger, 9:16) with a two-line title
    overlay visible from frame 0, then the existing text reel. Keeps the clip's
    own sound (no music). Output 1080x1920, 30 fps, H.264/AAC.

photo_post(img, kicker, title_lines, body_lines, out_png, out_jpg)
    1080x1350 post: Flow photo, dark top gradient, text at top, brand pill at
    bottom. Writes PNG (IG/FB) and JPG (TikTok).

photo_cover(img, title_lines, out_png, out_jpg)
    1080x1350 carousel cover: Flow photo with big title at top (replaces slide1).

CLI:
  python3 flow_upgrade.py hook CLIP REEL "Line one" "line two?" OUT.mp4
  python3 flow_upgrade.py post IMG "Kicker" "Title l1|Title l2" "Body l1|Body l2" OUT.png OUT.jpg
  python3 flow_upgrade.py cover IMG "Title l1|Title l2|Title l3" OUT.png OUT.jpg
"""
import subprocess, sys
from PIL import Image, ImageDraw, ImageFont

B = '/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf'
R = '/usr/share/fonts/truetype/google-fonts/Poppins-Regular.ttf'
DARK = (8, 24, 26)
MINT = (168, 230, 193)
CREAM = (255, 247, 232)
CORAL = (255, 150, 130)


def _esc(s):
    return s.replace('\\', '\\\\').replace(':', '\\:').replace("'", "’")


def hook(clip, reel, line1, line2, out, seconds=6):
    fade = seconds - 0.4
    fc = (
        f"[0:v]trim=0:{seconds},setpts=PTS-STARTPTS,scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,"
        f"crop=1080:1920,fps=30,format=yuv420p,"
        f"drawbox=x=0:y=0:w=iw:h=520:color=black@0.35:t=fill,"
        f"drawtext=fontfile={B}:text='{_esc(line1)}':fontsize=120:fontcolor=white:x=(w-tw)/2:y=170:shadowcolor=black@0.6:shadowx=3:shadowy=3,"
        f"drawtext=fontfile={B}:text='{_esc(line2)}':fontsize=120:fontcolor=0xA8E6C1:x=(w-tw)/2:y=310:shadowcolor=black@0.6:shadowx=3:shadowy=3,"
        f"fade=t=out:st={fade}:d=0.4,setsar=1[v0];"
        f"[0:a]atrim=0:{seconds},asetpts=PTS-STARTPTS,aresample=44100,afade=t=out:st={seconds-0.6}:d=0.6[a0];"
        f"[1:v]scale=1080:1920,fps=30,format=yuv420p,setsar=1[v1];[1:a]aresample=44100[a1];"
        f"[v0][a0][v1][a1]concat=n=2:v=1:a=1[v][a]"
    )
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', clip, '-i', reel, '-filter_complex', fc,
                    '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20',
                    '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', out], check=True)


def _base(img, top_frac=0.15, grad=0.52, strength=215):
    W, H = 1080, 1350
    src = Image.open(img).convert('RGB')
    s = max(W / src.width, H / src.height)
    im = src.resize((round(src.width * s), round(src.height * s)), Image.LANCZOS)
    left = (im.width - W) // 2
    top = int((im.height - H) * top_frac)
    im = im.crop((left, top, left + W, top + H))
    g = Image.new('L', (1, H))
    for y in range(H):
        v = 1 - y / (H * grad)
        g.putpixel((0, y), int(max(0, v) ** 0.9 * strength))
    return Image.composite(Image.new('RGB', (W, H), DARK), im, g.resize((W, H)))


def _fit(d, text, path, size, maxw=900):
    while size > 40 and d.textlength(text, font=ImageFont.truetype(path, size)) > maxw:
        size -= 4
    return ImageFont.truetype(path, size)


def _pill(d, H, x=90):
    f = ImageFont.truetype(B, 32)
    tw = d.textlength('Wellness Daily', font=f)
    d.rounded_rectangle((x - 22, H - 118, x + tw + 22, H - 62), radius=28, fill=DARK)
    d.text((x, H - 112), 'Wellness Daily', font=f, fill=MINT)


def photo_post(img, kicker, title_lines, body_lines, out_png, out_jpg):
    im = _base(img)
    d = ImageDraw.Draw(im)
    x, y = 90, 95
    d.text((x, y), kicker, font=ImageFont.truetype(B, 46), fill=CORAL)
    y += 80
    size = min(_fit(d, l, B, 88).size for l in title_lines)
    for l in title_lines:
        d.text((x, y), l, font=ImageFont.truetype(B, size), fill=CREAM)
        y += int(size * 1.23)
    y += 18
    for l in body_lines:
        d.text((x, y), l, font=_fit(d, l, R, 44), fill=(232, 238, 234))
        y += 58
    _pill(d, im.height)
    im.save(out_png)
    im.save(out_jpg, quality=92)


def photo_cover(img, title_lines, out_png, out_jpg):
    im = _base(img, grad=0.6, strength=225)
    d = ImageDraw.Draw(im)
    x, y = 90, 110
    size = min(_fit(d, l, B, 120).size for l in title_lines)
    for l in title_lines:
        d.text((x, y), l, font=ImageFont.truetype(B, size), fill=CREAM)
        y += int(size * 1.18)
    d.text((x, y + 20), 'Swipe for more >>', font=ImageFont.truetype(B, 44), fill=MINT)
    _pill(d, im.height)
    im.save(out_png)
    im.save(out_jpg, quality=92)


if __name__ == '__main__':
    a = sys.argv[1:]
    if a[0] == 'hook':
        hook(a[1], a[2], a[3], a[4], a[5])
    elif a[0] == 'post':
        photo_post(a[1], a[2], a[3].split('|'), a[4].split('|'), a[5], a[6])
    elif a[0] == 'cover':
        photo_cover(a[1], a[2].split('|'), a[3], a[4])
