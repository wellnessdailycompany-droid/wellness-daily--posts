# Wellness Daily: autonomous posting playbook

Owner: Brad. Brand: Wellness Daily. IG @wellnessdaily4u, FB Page, TikTok @wellnessdailynow.
Metricool blogId/brandId **7195815**, timezone **America/Chicago**. Posting must be CONTINUOUS and indefinite, no gaps, regardless of other tasks.
Brad pre-approved: schedule the standard daily mix WITHOUT asking. Only NEW formats/material (e.g. brand-name ingredient carousels) need his approval before posting.

## Every run
1. `getScheduledPosts` (brandId 7195815, fromDate today 00:00-05:00, toDate +7 days, timezone America/Chicago).
2. Goal: queue always covers at least the next **4 full days**. Build + schedule every missing day.
3. Daily mix per day: **2 Reels (9:16, 1080x1920) + 1 carousel (6 slides, 1080x1350) + 1 simple post (1080x1350)**. Each goes to IG+FB together; TikTok copy posted 1-3 hours later as a separate post.
4. Never repeat a topic (list below). Invent new, general, uncontroversial healthy-living tips. No medical claims. Footer on tip content: "General info only, not medical advice."
5. Push media to this repo (main), schedule with raw.githubusercontent.com URLs, then re-check with getScheduledPosts that every post exists.
6. If anything fails, retry once, then still schedule what you can. Never leave a day empty. Report problems to the user.

## Build
- `python3` + cairosvg + Pillow + ffmpeg (all installed). Font Poppins is a system font. Library: `tools/wd_lib.py` (t, pill, svgwrap, save, page, num_scene, make_reel). Copy `tools/example_content_build.py`, change the content, run with `WD_OUT=/tmp/out python3 your_build.py`.
- Palette: G #0E3B37, CREAM #FFF3DC, Y #FFD84D, CORAL #FF5E7E, OR #FF8A4C, MINT #9FE0B8, NIGHT #0A2A2E.
- Reel: 5 scenes ~16s (title, 3 numbered tips, CTA). The first frame must show the title (wd_lib already does) so thumbnails are never blank. NO music (Brad rejected the synth track; never add it). 
- LOOK at the contact sheet before pushing (clipped text? empty icons?). Titles must stay inside 1080px.
- Copy to repo: `images/YYYY-MM-DD-name/slideN.png|post.png`, `videos/YYYY-MM-DD/name.mp4` (new unique filenames, never overwrite), `git pull --rebase`, commit, push.

## Schedule slots (IG+FB at odd minutes, TikTok 1-3 h later at different odd/even minutes)
Reel 07:4x, carousel 11:3x, simple post 15:1x-16:2x, Reel 20:0x-20:1x. Vary minutes day to day. Never schedule in the past.
TikTok: videos `autoAddMusic:false`, photo/carousel posts `autoAddMusic:true`, ~5 hashtags incl. #fyp, privacyOption PUBLIC_TO_EVERYONE, title short.

## Hashtags (Instagram/Facebook)
Vary the count per post between ~11 and 30 (never always 30), relevant, no hyphens/spaces, no duplicates. Examples: #wellness #healthylifestyle #healthyliving #wellnesstips #healthyhabits #selfcare #dailyhabits #healthtips #wellnessdaily plus topical tags.

## createScheduledPost shapes (blogId "7195815", date ISO with -05:00)
Common info keys: autoPublish true, draft false, descendants [], firstCommentText "", hasNotReadNotes false, media [urls], mediaAltText [..] (alt text for images), providers, publicationDate {dateTime "YYYY-MM-DDTHH:mm:ss", timezone "America/Chicago"}, shortener false, smartLinkData {ids:[]}, text.
- IG+FB Reel: providers instagram+facebook, instagramData {type:"REEL",showReelOnFeed:true,isAiGenerated:false}, facebookData {type:"REEL",title}.
- IG+FB post or carousel: instagramData {type:"POST",isAiGenerated:false}, facebookData {type:"POST"}.
- TikTok: providers [{network:"tiktok"}], tiktokData {title,privacyOption:"PUBLIC_TO_EVERYONE",autoAddMusic,photoCoverIndex:0}.
- Updating a post changes its id (uuid stays); updateScheduledPost needs the full original content.

## Topics already used (do not repeat)
sleep habits, protein+fiber breakfast, gut-friendly grocery list, walk after a meal, fibermaxxing, myth vs fact, that's so wellness, wind-down routine, welcome reel, stand up and stretch hourly, drink more water, 5-minute morning reset, snacks that satisfy, 3 colors on your plate, stress resets (breathing), meal prep in 3 steps, eat more fiber, easy food swaps, 20-20-20 eye rule, gratitude, posture check, build a habit, weekly wellness checklist, call a friend, 3 quick breakfast ideas.
Ideas not yet used: sunlight/vitamin D basics, protein sources, healthy fats, mindful eating, screen-free hour, strength basics at home, walking meeting, lunch-break reset, sleep-friendly evening snack, hydration myths, reading before bed, declutter your space, cooking at home, plant-based swaps, label reading basics (generic, no brand names), cold-weather wellness, seasonal produce, travel wellness, desk snacks, gentle yoga stretches.

## Do NOT
- Post brand-name ingredient/"what's inside" content without Brad's approval (draft exists in Canva; see chat).
- Fabricate data or sources. Do not use Instagram music (Metricool audio catalog not connected).
- Use the rejected synth music, wide-angle/letterboxed formats, or repeat topics.
