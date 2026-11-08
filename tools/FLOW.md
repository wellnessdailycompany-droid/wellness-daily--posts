# Wellness Daily: daily Google Flow upgrade (approved by Brad, Nov 8 2026)

Brad's standing approval: run this every day automatically, spend Flow credits within the cap below, no need to ask him. Text posts from the queue-refill task are the fallback, so if anything here fails, leave the original post untouched — posting must never stop.

## What to upgrade (TOMORROW's posts, America/Chicago)
1. **Morning Reel (07:4x, IG+FB) and its TikTok copy:** prepend a 5–7 s Flow video hook (one Veo 3.1 Lite clip).
2. **Simple post (15:1x–16:2x, IG+FB) and its TikTok copy:** replace the text card with a Flow photo post.
3. **Carousel (11:3x, IG+FB) and its TikTok copy:** replace slide 1 only with a Flow photo cover; keep slides 2–6.
The evening Reel stays as it is (one video a day keeps credits low).

## Credit rules (Flow account bradpanassow@gmail.com, Google AI Pro)
- Images (Nano Banana 2.1) cost 0 credits. Veo 3.1 Lite video = 10 credits.
- Max 2 video generations per day (one retry). Never use Fast, Quality, Omni, upscaling, or x2–x4 outputs.
- Check the balance in the account menu first. If under 150 credits, skip the video and do only the photos.

## Flow steps (built-in browser on Brad's Mac)
- Open https://labs.google/fx/tools/flow. Make sure the account menu shows bradpanassow@gmail.com (NOT wellnessdailycompany@gmail.com); switch accounts if needed. Never sign out.
- New project. Settings menu (bottom-right chip): Image → 9:16 → Nano Banana 2.1 → x1 for photos; Video → Frames → 9:16 → Veo 3.1 - Lite → x1 (must say "10 credits") for the clip.
- Set the prompt with form_input on the "What do you want to create?" textbox, then click the arrow.
- Photo prompts: photo-realistic, vertical, editorial food/lifestyle style, matching the post's topic, "no text, no logos, no brand names", no identifiable faces.
- Video prompt: fast, energetic, appetizing or calming motion matching the Reel's topic, "no text, no faces".
- Download: open the item → download icon → video "720p Original size", image "1K Original size" (never the upscaled options).
- Downloads land in ~/Downloads as hidden temp names (.Q6L2SF6YDW.com.anthropic.claudefordesktop.*). Find the newest by mtime with device_list_dir, then device_stage_files it.

## Build (cloud container)
`python3 tools/flow_upgrade.py hook CLIP REEL "Line one" "line two?" OUT.mp4` (hook text = the Reel's title as a question or punchy 2-line hook, each line ≤ 12 chars)
`python3 tools/flow_upgrade.py post IMG "Kicker" "Title l1|Title l2" "Body l1|Body l2" OUT.png OUT.jpg` (reuse the existing post's wording)
`python3 tools/flow_upgrade.py cover IMG "Title l1|Title l2" OUT.png OUT.jpg`
Look at frames/images before pushing. Copy to new filenames (never overwrite): `videos/YYYY-MM-DD/<name>-hook.mp4`, `images/YYYY-MM-DD-flow-<name>/post.png|post-tt.jpg|slide1.png|slide1-tt.jpg`. Commit and push to main; confirm each raw.githubusercontent URL returns 200.

## Swap in Metricool (brand 7195815)
updateScheduledPost with the full original post (text, times, providers, network data) changing only `media` (and alt text). TikTok video posts keep `videoCoverMilliseconds:1500` and `autoAddMusic:false`; TikTok photo posts use the JPG. isAiGenerated stays false. Re-read with getScheduledPosts to confirm.

## Never
- Mention AI in captions or images. Use music. Spend credits beyond the cap. Touch posts other than tomorrow's.
