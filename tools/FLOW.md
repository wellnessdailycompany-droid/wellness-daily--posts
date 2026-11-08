# Wellness Daily: daily Google Flow upgrade (approved by Brad, Nov 8 2026)

Brad's standing approval: run this every day automatically, spend Flow credits within the cap below, no need to ask him. Text posts from the queue-refill task are the fallback, so if anything here fails, leave the original post untouched — posting must never stop.

## What to upgrade: ALL of TOMORROW's posts (America/Chicago)
Brad (Nov 8): photos cost nothing, so every post uses Flow photos from now on, never text on a blank background. Only ONE video clip a day.
1. **Morning Reel (07:4x, IG+FB) + TikTok copy:** 6 s Flow video hook (`hook`) in front of a photo reel (`reel`) rebuilt from the same title/tips/CTA. Build the photo reel first, then `hook CLIP photo_reel.mp4 ...`.
2. **Evening Reel (20:0x, IG+FB) + TikTok copy:** photo reel (`reel`), no video.
3. **Carousel (11:3x, IG+FB) + TikTok copy:** photo carousel (`carousel`), all 6 slides.
4. **Simple post (15:1x-16:2x, IG+FB) + TikTok copy:** photo post (`post`).
Get the wording from the scheduled post's caption and alt text (alt text lists slide/tip titles); keep the same message. Tips: title <= 15 chars per line, sub lines <= 26 chars.
Photos per day: about 2 per Reel (title/tips), 3 per carousel (cover + items), 1 for the simple post — each prompt matched to its scene. Re-use is fine (builders cycle the list).

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
