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

## Step 0: pick the path (do this BEFORE generating anything)
1. **Mac path (first choice, free photos):** get_device_info works AND device_list_dir /Users/brad.prime/Downloads works AND the built-in browser opens Flow. Then use the Flow steps below.
2. **OpenArt backup (Mac off/asleep/unreachable):** Brad approved Nov 9, 2026: photos only, NO video. Use the steps in "OpenArt backup" below.
3. If both fail, keep the original posts and tell Brad. Never use the Gemini API path (not approved).

## OpenArt backup (Mac unreachable) — photos only
Account: Brad's OpenArt Plus account via the OpenArt connector (tools mcp__OpenArt__*). Model **nano-banana-2-1**, mode text2image, params {"aspectRatio":"9:16","resolution":"1K","imageCount":1}: 27 credits per photo (30 list, 10% MCP discount, Nov 2026), about 460 credits for a full day of ~17 photos. No video in this path: the morning Reel gets the photo reel without a hook.
1. openart_account_get first; if the balance is under 1,000 credits, do photos for the carousel and simple post only and tell Brad.
2. Generate one different photo per scene/slide (same prompts style as the Flow path, append "no text, no logos, no brand names, no identifiable faces"). Use openart_generate_image_batch for the set, then openart_creation_wait / openart_creation_get until each is COMPLETED and collect each resource `url` (https://cdn.openart.ai/...).
3. The cloud workspace can NOT download cdn.openart.ai (proxy 403), so the build runs on GitHub: write `jobs/YYYY-MM-DD.json` in the cloud_media.py format with each "photos" value set to the OpenArt URL (not a prompt). Commit and push to main; .github/workflows/cloud-media.yml downloads the photos, builds with flow_upgrade.py and pushes the media plus `jobs/done/YYYY-MM-DD.json` (about 1-3 min; poll https://raw.githubusercontent.com/wellnessdailycompany-droid/wellness-daily--posts/main/jobs/done/YYYY-MM-DD.json).
4. git pull, look at the built images/frames, then swap them into Metricool as in "Swap in Metricool".
5. Summary to Brad: "OpenArt backup ran", photos made, credits used and balance left.

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
- 2026-11-09 OpenArt backup (for Nov 10): morning Reel hook + simple post were already Flow-upgraded (Nov 8); OpenArt made 11 photos (evening brain-dump Reel 5 + frozen-veggies carousel 6), 297 credits, 12,844 left. Built via jobs/2026-11-10.json, all 4 posts swapped and verified. Plus plan runs max 8 images at once: batch of 11 submitted 9, resubmit the rest after the first finish.
- 2026-11-10 run (for Nov 11): Flow opened fine in the built-in browser, but ~/Downloads is still NOT a connected folder for this task (get_device_info connectedFolders empty; device_list_dir needs a grant). Stopped before generating (0 credits spent); all 8 Nov 11 posts keep their original media. OpenArt connector not available in the session either.
- 2026-11-10 OpenArt backup (for Nov 11, 21:15 CST): Mac upgrade hadn't happened; OpenArt made 17 photos (leftovers Reel 5, nature Reel 5, eggs carousel 6, lunch post 1), 459 credits, 12,157 left. Built via jobs/2026-11-11.json (GitHub build ~2 min), all 8 posts swapped and verified (morning Reel has no hook: photos-only path).
- 2026-11-11 run (for Nov 12, 19:24 CST): ~/Downloads still NOT reachable (get_device_info connectedFolders empty; device_list_dir /Users/brad.prime/Downloads "can't be listed without a grant") even though the task says it is attached. Stopped before opening Flow (0 credits spent); all 8 Nov 12 posts (sing-along Reels, sandwich carousels, small-joys posts, thank-you Reels) keep their original media. OpenArt connector not in this session.
- 2026-11-11 OpenArt backup (for Nov 12, 21:30 CST): Mac upgrade hadn't happened; OpenArt made 17 photos (sing-along Reel 5, thank-you Reel 5, sandwich carousel 6, small-joys post 1), 391 credits (~23/photo), 11,766 left. Batches of 8+8+1. Built via jobs/2026-11-12.json (GitHub build ~2.5 min), all 8 posts swapped and verified (morning Reel has no hook: photos-only path).
- 2026-11-12 OpenArt backup (for Nov 13, 21:30 CST): Mac upgrade hadn't happened; OpenArt made 17 photos (inbox Reel 5, pantry Reel 5, theme-night carousel 6, gentle wake-up post 1), 391 credits (~23/photo), 11,112 left. Batches of 8+8+1. Built via jobs/2026-11-13.json (GitHub build ~2 min), all 8 posts swapped and verified (morning Reel has no hook: photos-only path). Tip title "Check twice a day" shortened to "Check 2x a day" (15-char limit).
- 2026-11-13 run (for Nov 14, 00:29 CST): ~/Downloads still NOT reachable (get_device_info connectedFolders empty; Downloads "requiresGrantBeforeListing"; device_list_dir needs a grant) even though the task says it is attached. Stopped before opening Flow (0 credits spent); Nov 14 posts keep their original media. OpenArt connector not in this session.
- 2026-11-13 run #2 (for Nov 14, 19:24 CST): ~/Downloads still NOT reachable (connectedFolders empty; Downloads requiresGrantBeforeListing; device_list_dir needs a grant). Stopped before opening Flow (0 credits spent); Nov 14 posts keep their current media. OpenArt connector not in this session.
