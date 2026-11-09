# Wellness Daily: daily Google Flow upgrade (approved by Brad, Nov 8 2026)

Brad's standing approval: run this every day automatically, spend Flow credits within the cap below, no need to ask him. Text posts from the queue-refill task are the fallback, so if anything here fails, leave the original post untouched — posting must never stop.

## What to upgrade: ALL of TOMORROW's posts (America/Chicago)
Brad (Nov 8): photos cost nothing, so every post uses Flow photos from now on, never text on a blank background. Only ONE video clip a day.
1. **Morning Reel (07:4x, IG+FB) + TikTok copy:** 6 s Flow video hook (`hook`) in front of a photo reel (`reel`) rebuilt from the same title/tips/CTA. Build the photo reel first, then `hook CLIP photo_reel.mp4 ...`.
2. **Evening Reel (20:0x, IG+FB) + TikTok copy:** photo reel (`reel`), no video.
3. **Carousel (11:3x, IG+FB) + TikTok copy:** photo carousel (`carousel`), all 6 slides.
4. **Simple post (15:1x-16:2x, IG+FB) + TikTok copy:** photo post (`post`).
Get the wording from the scheduled post's caption and alt text (alt text lists slide/tip titles); keep the same message. Tips: title <= 15 chars per line, sub lines <= 26 chars.
**A DIFFERENT photo for every scene and slide — never repeat a photo within a post or across the day (Brad, Nov 8).** Photos cost 0 credits, so generate one per scene:
- Each Reel: 5 photos (title, tip 1, tip 2, tip 3, CTA) → `images` list of 5 in the SPEC.
- Carousel: 6 photos (cover, 4 items, CTA) → `images` list of 6.
- Simple post: 1 photo.
That is about 17 photos a day. Each prompt must show that scene's own idea (e.g. tip "Pick one pan" → one skillet on a stove; tip "Chop while it heats" → hands chopping vegetables), with varied angles and settings so the set doesn't look repetitive. Before building, check the `images` lists have no duplicates. If a photo fails to generate, generate a new one; only reuse as a last resort, and say so in the summary.

## Credit rules (Flow account bradpanassow@gmail.com, Google AI Pro) — protect credits for Prime Media Marketing
- Images (Nano Banana 2.1) cost 0 credits. Veo 3.1 Lite video = 10 credits.
- Exactly ONE video generation per day, no retries (max 10 credits/day, about 300/month). If the clip is unusable, skip the hook and post the photo reel.
- Never use Fast, Quality, Omni, upscaling, or x2-x4 outputs.
- Check the balance in the account menu first. If under 400 credits, skip the video (the rest is reserved for Prime Media Marketing) and do only photos.

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
`python3 tools/flow_upgrade.py reel SPEC.json OUT.mp4` and `python3 tools/flow_upgrade.py carousel SPEC.json FOLDER` (SPEC format in the script's docstring)
Look at frames/images before pushing. Copy to new filenames (never overwrite): `videos/YYYY-MM-DD/<name>-hook.mp4`, `images/YYYY-MM-DD-flow-<name>/post.png|post-tt.jpg|slideN.png|slideN-tt.jpg`. Commit and push to main; confirm each raw.githubusercontent URL returns 200.

## Swap in Metricool (brand 7195815)
updateScheduledPost with the full original post (text, times, providers, network data) changing only `media` (and alt text). Carousels: IG/FB get slide1..6.png, TikTok gets slide1..6-tt.jpg. TikTok video posts keep `videoCoverMilliseconds:1500` and `autoAddMusic:false`; TikTok photo posts use the JPG. isAiGenerated stays false. Re-read with getScheduledPosts to confirm.

## Never
- Mention AI in captions or images. Use music. Spend credits beyond the cap (1 video/day). Touch posts other than tomorrow's.

## Run log
- 2026-11-08 run (for Nov 10): Flow media generated (17 photos + 1 Veo Lite clip, 10 credits, 1,030 left) and downloaded, but ~/Downloads is NOT a connected folder for scheduled runs; the access prompt went unanswered, so nothing was staged and Nov 10 posts kept their original media. Fix: Brad approves the "allow access to Downloads" prompt once (it then persists for later runs) or connects ~/Downloads to the task. Tip: images can be saved in-page with fetch(flow-content URL) -> blob -> <a download> (native 768x1376 = 1K original); the container proxy blocks flow-content.google directly.
