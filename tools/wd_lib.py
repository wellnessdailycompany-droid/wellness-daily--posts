import cairosvg, os, sys, subprocess, shutil
from multiprocessing import Pool
from PIL import Image
G="#0E3B37"; CREAM="#FFF3DC"; Y="#FFD84D"; CORAL="#FF5E7E"; OR="#FF8A4C"; AM="#FFB43B"; MINT="#9FE0B8"; NIGHT="#0A2A2E"
FONT="Poppins, Helvetica, Arial, sans-serif"
def t(lines,x,y,size,fill,weight=700,anchor="start",lh=1.2,op=1):
    return "\n".join(f'<text x="{x}" y="{y+i*size*lh:.0f}" text-anchor="{anchor}" font-family="{FONT}" font-weight="{weight}" font-size="{size}" fill="{fill}" opacity="{op}">{l}</text>' for i,l in enumerate(lines))
def pill(x,y,w,h,fill,label,tc,size=44):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h//2}" fill="{fill}"/>'+t([label],x+w//2,y+h//2+size*0.35,size,tc,700,"middle")
def svgwrap(w,h,bg,body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}"><rect width="{w}" height="{h}" fill="{bg}"/>{body}</svg>'
def save(name,svg,w,h,folder):
    os.makedirs(folder,exist_ok=True)
    open(f"{folder}/{name}.svg","w").write(svg)
    cairosvg.svg2png(bytestring=svg.encode(),write_to=f"{folder}/{name}.png",output_width=w,output_height=h)

# ================= REELS (1080x1920 full-frame 9:16) =================
FPS=30
def ease(p): p=max(0,min(1,p)); return 1-(1-p)**3
def reel_frame(args):
    idx,scenes,total,outdir,t_now=args
    # find scene
    acc=0
    for sc in scenes:
        if t_now<acc+sc["dur"] or sc is scenes[-1]: break
        acc+=sc["dur"]
    lt=t_now-acc
    if sc is scenes[0]: lt+=1.4   # first scene already fully visible at frame 0 (no blank thumbnail)
    body=""
    for svg,delay in sc["elems"]:
        e=ease((lt-delay)/0.55)
        body+=f'<g opacity="{e:.3f}" transform="translate(0,{(1-e)*50+sc.get("dy",0):.1f})">{svg}</g>'
    # progress bar (safe zone, above bottom UI)
    prog=t_now/total
    body+=f'<rect x="90" y="1560" width="900" height="10" rx="5" fill="{sc["fg"]}" opacity=".2"/><rect x="90" y="1560" width="{900*prog:.1f}" height="10" rx="5" fill="{CORAL}"/>'
    svg=svgwrap(1080,1920,sc["bg"],body)
    cairosvg.svg2png(bytestring=svg.encode(),write_to=f"{outdir}/f{idx:04d}.png")
def make_reel(name,scenes):
    total=sum(s["dur"] for s in scenes)
    outdir=f"/tmp/reel_{name}"; shutil.rmtree(outdir,ignore_errors=True); os.makedirs(outdir)
    n=int(total*FPS)
    jobs=[(i,scenes,total,outdir,i/FPS) for i in range(n)]
    with Pool(8) as p: p.map(reel_frame,jobs,chunksize=8)
    os.makedirs("reels",exist_ok=True)
    # still preview of last frame of each scene
    out=f"reels/{name}.mp4"
    subprocess.run(["ffmpeg","-y","-loglevel","error","-framerate",str(FPS),"-i",f"{outdir}/f%04d.png","-f","lavfi","-i","anullsrc=channel_layout=stereo:sample_rate=44100",
        "-c:v","libx264","-preset","medium","-crf","19","-pix_fmt","yuv420p","-r",str(FPS),"-c:a","aac","-shortest","-movflags","+faststart",out],check=True)
    # contact frames
    acc=0; ims=[]
    for sc in scenes:
        k=int((acc+sc["dur"]-0.05)*FPS); k=min(k,n-1)
        ims.append(Image.open(f"{outdir}/f{k:04d}.png").resize((270,480))); acc+=sc["dur"]
    sh=Image.new("RGB",(280*len(ims),490),"#222")
    for i,im in enumerate(ims): sh.paste(im,(5+i*280,5))
    sh.save(f"reels/{name}-frames.png")
    return out

def num_scene(bg,fg,accent,num,title,sub,dur=3.2,icon=""):
    return dict(bg=bg,fg=fg,dur=dur,dy=230,elems=[
        (pill(90,330,170,170,accent,str(num),G if accent!=G else CREAM,96),0.0),
        (t(title,90,640,92,fg,800,lh=1.12),0.25),
        (t(sub,94,640+len(title)*92*1.12+40,48,fg,500,lh=1.35,op=.9),0.65),
        (icon,0.4)])


# ================= FEED helper (1080x1350, 4:5) =================
def page(w,h,bg,body,fg,n=None,total=None):
    foot=t(["Wellness Daily"],90,h-60,30,fg,600,op=.75)
    if n: foot+=t([f"{n}/{total}"],w-90,h-60,30,fg,600,"end",op=.75)
    return svgwrap(w,h,bg,body+foot)
