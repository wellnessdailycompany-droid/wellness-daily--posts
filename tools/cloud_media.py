"""Wellness Daily cloud fallback: generate photos with the Gemini API and build posts.

Used when Brad's Mac (Google Flow) is asleep/offline. Runs in GitHub Actions
(.github/workflows/cloud-media.yml), which has open internet; the Claude cloud
workspace does not.

Job file: jobs/YYYY-MM-DD.json
{
  "date": "2026-11-10",
  "photos": {"A1": "prompt ...", "A2": "...", ...},          # one photo per scene, all different
  "reels": {"am-dinner20": {<flow_upgrade reel SPEC, images = photo keys>}},
  "carousels": {"frozenveg": {<flow_upgrade carousel SPEC, images = photo keys>}},
  "posts": {"breakfastdinner": {"image": "P", "kicker": "...", "title": ["l1","l2"], "body": ["l1","l2"]}}
}
Outputs (new filenames, never overwrite):
  videos/DATE/<name>-photo.mp4
  images/DATE-flow-<name>/slide1..6.png + slide1..6-tt.jpg   (carousels)
  images/DATE-flow-<name>/post.png + post-tt.jpg             (posts)
Result: jobs/done/DATE.json {"ok", "outputs": {name: [paths]}, "errors": [...], "model", "photos_generated"}
A post whose photos failed is skipped (its original media stays in Metricool).

Env: GEMINI_API_KEY (required unless WD_MOCK=1), WD_IMAGE_MODEL (default gemini-3.1-flash-image),
     WD_MOCK=1 makes placeholder photos (pipeline test, no API calls, no cost).
Usage: python3 tools/cloud_media.py jobs/2026-11-10.json
"""
import base64, io, json, os, sys, time, urllib.request, urllib.error
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import flow_upgrade as F  # noqa: E402

MODEL = os.environ.get('WD_IMAGE_MODEL', 'gemini-3.1-flash-image')
MOCK = os.environ.get('WD_MOCK') == '1'
SUFFIX = (' Photo-realistic, vertical 9:16, editorial food and lifestyle photography, natural light. '
          'No text, no words, no letters, no logos, no brand names, no identifiable faces.')


def gen_photo(prompt, out):
    if MOCK:
        h = abs(hash(prompt)) % 360
        im = Image.new('RGB', (768, 1376), tuple(int(127 + 120 * ((h + k * 120) % 360 < 180)) for k in range(3)))
        ImageDraw.Draw(im).ellipse((200, 500, 568, 868), fill=(40, 80, 60))
        im.save(out, quality=92)
        return
    body = {'contents': [{'parts': [{'text': prompt + SUFFIX}]}],
            'generationConfig': {'responseModalities': ['TEXT', 'IMAGE'],
                                 'imageConfig': {'aspectRatio': '9:16', 'imageSize': '1K'}}}
    req = urllib.request.Request(
        f'https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent',
        data=json.dumps(body).encode(), method='POST',
        headers={'x-goog-api-key': os.environ['GEMINI_API_KEY'], 'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=180) as r:
        j = json.load(r)
    for c in j.get('candidates', []):
        for p in c.get('content', {}).get('parts', []):
            d = p.get('inlineData') or p.get('inline_data')
            if d and d.get('data'):
                Image.open(io.BytesIO(base64.b64decode(d['data']))).convert('RGB').save(out, quality=92)
                return
    raise RuntimeError('no image in response: ' + json.dumps(j)[:400])


def main(job_path):
    job = json.load(open(job_path))
    date = job['date']
    work = f'/tmp/wd-{date}'
    os.makedirs(work, exist_ok=True)
    res = {'ok': False, 'outputs': {}, 'errors': [], 'model': 'mock' if MOCK else MODEL, 'photos_generated': 0}
    photos = {}
    for key, prompt in job['photos'].items():
        out = f'{work}/{key}.jpg'
        for attempt in (1, 2):
            try:
                gen_photo(prompt, out)
                photos[key] = out
                res['photos_generated'] += 1
                break
            except Exception as e:  # noqa: BLE001
                msg = e.read().decode()[:300] if isinstance(e, urllib.error.HTTPError) else str(e)[:300]
                if attempt == 2:
                    res['errors'].append(f'photo {key}: {msg}')
                else:
                    time.sleep(8)

    def imgs(keys, name):
        missing = [k for k in keys if k not in photos]
        if missing:
            res['errors'].append(f'{name}: skipped, missing photos {missing}')
            return None
        return [photos[k] for k in keys]

    for name, spec in job.get('reels', {}).items():
        try:
            im = imgs(spec['images'], name)
            if im:
                os.makedirs(f'videos/{date}', exist_ok=True)
                out = f'videos/{date}/{name}-photo.mp4'
                F.reel_scenes(im, spec['title_small'], spec['title_big'], spec['tips'], spec['cta'], out)
                res['outputs'][name] = [out]
        except Exception as e:  # noqa: BLE001
            res['errors'].append(f'{name}: {e}'[:300])
    for name, spec in job.get('carousels', {}).items():
        try:
            im = imgs(spec['images'], name)
            if im:
                folder = f'images/{date}-flow-{name}'
                F.carousel_slides(im, spec['cover'], spec['label'], spec['items'], spec['cta_big'], spec['cta_sub'], folder)
                res['outputs'][name] = [f'{folder}/slide{k}.png' for k in range(1, 7)] + \
                                       [f'{folder}/slide{k}-tt.jpg' for k in range(1, 7)]
        except Exception as e:  # noqa: BLE001
            res['errors'].append(f'{name}: {e}'[:300])
    for name, spec in job.get('posts', {}).items():
        try:
            im = imgs([spec['image']], name)
            if im:
                folder = f'images/{date}-flow-{name}'
                os.makedirs(folder, exist_ok=True)
                F.photo_post(im[0], spec['kicker'], spec['title'], spec['body'], f'{folder}/post.png', f'{folder}/post-tt.jpg')
                res['outputs'][name] = [f'{folder}/post.png', f'{folder}/post-tt.jpg']
        except Exception as e:  # noqa: BLE001
            res['errors'].append(f'{name}: {e}'[:300])

    res['ok'] = bool(res['outputs'])
    os.makedirs('jobs/done', exist_ok=True)
    json.dump(res, open(f'jobs/done/{date}.json', 'w'), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == '__main__':
    main(sys.argv[1])
