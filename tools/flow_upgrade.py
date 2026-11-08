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

CLI (see also reel/carousel below):
  python3 flow_upgrade.py hook CLIP REEL "Line one" "line two?" OUT.mp4
  python3 flow_upgrade.py post IMG "Kicker" "Title l1|Title l2" "Body l1|Body l2" OUT.png OUT.jpg
  python3 flow_upgrade.py cover IMG "Title l1|Title l2|Title l3" OUT.png OUT.jpg
  python3 flow_upgrade.py reel SPEC.json OUT.mp4
      SPEC: {"images":[...],"title_small":"Dinner in 20 minutes:","title_big":["3 tips"],
             "tips":[[["Pick one pan"],["Fewer dishes and","less cleanup."]],...],"cta":["Quick and","easy wins."]}
  python3 flow_upgrade.py carousel SPEC.json FOLDER
      SPEC: {"images":[...],"cover":["Eggs","four ways"],"label":"Egg idea",
             "items":[[["Scrambled"],["Soft and quick."]],...4 items],"cta_big":["Save","this."],"cta_sub":["Which is your favorite?"]}
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



# ---------------- photo-background reels and carousels ----------------
import os, json, tempfile, shutil


def _darken(img, W, H, amount=0.55, top_frac=0.5):
    src = Image.open(img).convert('RGB')
    s = max(W / src.width, H / src.height)
    im = src.resize((round(src.width * s), round(src.height * s)), Image.LANCZOS)
    left = (im.width - W) // 2
    top = int((im.height - H) * top_frac)
    im = im.crop((left, top, left + W, top + H))
    return Image.blend(im, Image.new('RGB', (W, H), DARK), amount)


def _lines(d, x, y, lines, path, size, fill, lh=1.15, maxw=900):
    size = min(_fit(d, l, path, size, maxw).size for l in lines) if lines else size
    f = ImageFont.truetype(path, size)
    for l in lines:
        d.text((x, y), l, font=f, fill=fill)
        y += int(size * lh)
    return y


def reel_scenes(images, title_small, title_big, tips, cta, out):
    """Photo reel: title, 3 numbered tips, CTA. images: list of paths, cycled.
    tips: [(["Title"],["sub line","sub line"]), ...]. Silent audio (no music).
    Frame 0 shows the title (thumbnail rule)."""
    W, H = 1080, 1920
    tmp = tempfile.mkdtemp()
    scenes = []
    im = _darken(images[0], W, H, 0.6); d = ImageDraw.Draw(im)
    y = _lines(d, 90, 640, [title_small], B, 66, MINT)
    _lines(d, 90, y + 20, title_big, B, 130, CREAM, 1.05)
    scenes.append((im, 3.0))
    for i, (ti, su) in enumerate(tips):
        im = _darken(images[(i + 1) % len(images)], W, H, 0.62, 0.3 + 0.2 * i); d = ImageDraw.Draw(im)
        d.ellipse((90, 520, 260, 690), fill=(255, 94, 126))
        n = str(i + 1); f = ImageFont.truetype(B, 96)
        d.text((175 - d.textlength(n, font=f) / 2, 545), n, font=f, fill=CREAM)
        y = _lines(d, 90, 760, ti, B, 92, CREAM, 1.12)
        _lines(d, 94, y + 30, su, R, 50, (235, 240, 236), 1.35)
        scenes.append((im, 3.2))
    im = _darken(images[(len(tips) + 1) % len(images)], W, H, 0.62, 0.7); d = ImageDraw.Draw(im)
    y = _lines(d, 90, 700, cta, B, 120, CREAM, 1.1)
    d.text((94, y + 60), 'General info only, not medical advice.', font=ImageFont.truetype(R, 34), fill=(220, 225, 222))
    scenes.append((im, 3.0))
    for im, _ in scenes:  # brand tag
        _pill(ImageDraw.Draw(im), 1500)
    args = ['ffmpeg', '-v', 'error', '-y']
    for k, (im, dur) in enumerate(scenes):
        fp = f'{tmp}/s{k}.png'; im.save(fp)
        args += ['-loop', '1', '-framerate', '30', '-t', str(dur + 0.4), '-i', fp]
    args += ['-f', 'lavfi', '-i', 'anullsrc=channel_layout=stereo:sample_rate=44100']
    fc = []
    for k, (_, dur) in enumerate(scenes):
        frames = int((dur + 0.4) * 30)
        fc.append(f"[{k}:v]scale=1188:2112,zoompan=z='1+0.05*on/{frames}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30,trim=duration={dur + 0.4},setpts=PTS-STARTPTS,setsar=1,format=yuv420p[z{k}]")
    prev, off = 'z0', 0.0
    for k in range(1, len(scenes)):
        off += scenes[k - 1][1]
        fc.append(f"[{prev}][z{k}]xfade=transition=fade:duration=0.4:offset={off:.2f}[x{k}]")
        prev = f'x{k}'
    total = sum(d for _, d in scenes) + 0.4
    args += ['-filter_complex', ';'.join(fc), '-map', f'[{prev}]', '-map', f'{len(scenes)}:a', '-t', f'{total:.2f}',
             '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-c:a', 'aac', '-movflags', '+faststart', out]
    subprocess.run(args, check=True)
    shutil.rmtree(tmp)


def carousel_slides(images, cover_lines, label, items, cta_big, cta_sub, folder):
    """6-slide photo carousel (1080x1350): cover, 4 items, CTA. images cycled.
    items: [(["Title l1","l2"],["sub"]), ...]. Writes slideN.png and slideN-tt.jpg."""
    os.makedirs(folder, exist_ok=True)
    W, H = 1080, 1350
    total = len(items) + 2
    def foot(d, n):
        f = ImageFont.truetype(B, 32); tw = d.textlength(f'{n}/{total}', font=f)
        d.rounded_rectangle((W - 112 - tw, H - 118, W - 68, H - 62), radius=28, fill=DARK)
        d.text((W - 90 - tw, H - 112), f'{n}/{total}', font=f, fill=MINT)
    slides = []
    photo_cover(images[0], cover_lines, f'{folder}/slide1.png', f'{folder}/slide1-tt.jpg')
    for i, (ti, su) in enumerate(items):
        im = _base(images[(i + 1) % len(images)], top_frac=0.3, grad=0.75, strength=225); d = ImageDraw.Draw(im)
        d.text((90, 100), label, font=ImageFont.truetype(B, 44), fill=CORAL)
        y = _lines(d, 90, 180, ti, B, 96, CREAM, 1.1)
        _lines(d, 94, y + 25, su, R, 46, (235, 240, 236), 1.35)
        _pill(d, H); foot(d, i + 2)
        slides.append(im)
    im = _darken(images[(len(items) + 1) % len(images)], W, H, 0.65); d = ImageDraw.Draw(im)
    y = _lines(d, 90, 330, cta_big, B, 150, CREAM, 1.0)
    y = _lines(d, 94, y + 60, cta_sub, R, 52, (235, 240, 236), 1.35)
    d.text((94, y + 60), 'General info only, not medical advice.', font=ImageFont.truetype(R, 34), fill=(220, 225, 222))
    _pill(d, H); foot(d, total)
    slides.append(im)
    for k, im in enumerate(slides, 2):
        im.save(f'{folder}/slide{k}.png'); im.save(f'{folder}/slide{k}-tt.jpg', quality=92)


def _unique(images, need):
    import hashlib
    hs = [hashlib.md5(open(i, 'rb').read()).hexdigest() for i in images]
    if len(set(hs)) < len(hs):
        print('WARNING: the same photo appears more than once in this post', file=sys.stderr)
    if len(images) < need:
        print(f'WARNING: {len(images)} photos for {need} scenes; photos will repeat', file=sys.stderr)


if __name__ == '__main__':
    a = sys.argv[1:]
    if a[0] == 'hook':
        hook(a[1], a[2], a[3], a[4], a[5])
    elif a[0] == 'post':
        photo_post(a[1], a[2], a[3].split('|'), a[4].split('|'), a[5], a[6])
    elif a[0] == 'cover':
        photo_cover(a[1], a[2].split('|'), a[3], a[4])
    elif a[0] == 'reel':   # reel SPEC.json OUT.mp4
        j = json.load(open(a[1])); _unique(j['images'], 2 + len(j['tips'])); reel_scenes(j['images'], j['title_small'], j['title_big'], j['tips'], j['cta'], a[2])
    elif a[0] == 'carousel':   # carousel SPEC.json FOLDER
        j = json.load(open(a[1])); _unique(j['images'], 2 + len(j['items'])); carousel_slides(j['images'], j['cover'], j['label'], j['items'], j['cta_big'], j['cta_sub'], a[2])
