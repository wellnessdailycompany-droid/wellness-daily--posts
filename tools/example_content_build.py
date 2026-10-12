import os,sys,importlib.util
HERE=os.path.dirname(os.path.abspath(__file__))
os.makedirs("/tmp/junk5",exist_ok=True); os.chdir("/tmp/junk5")
sys.path.insert(0,HERE)
import wd_lib as B
from wd_lib import *
OUT=os.environ.get("WD_OUT","/tmp/wd_out"); os.makedirs(OUT,exist_ok=True); os.chdir(OUT)
def reel(title_small,title_big,pts,cta,colors,bgt=G):
    sc=[dict(bg=bgt,fg=CREAM,dur=3.0,elems=[(t([title_small],90,720,66,MINT,600),0.1),(t(title_big,90,850,130,CREAM,800,lh=1.05),0.3)])]
    for i,(ti,su) in enumerate(pts):
        bg,fg,acc=colors[i]; sc.append(num_scene(bg,fg,acc,i+1,ti,su))
    sc.append(dict(bg=CORAL,fg=G,dur=3.0,elems=[(t(cta,90,700,120,G,800,lh=1.1),0),(t(["General info only, not medical advice."],94,1090,34,G,500,op=.75),0.7)]))
    return sc
C3=[(CREAM,G,CORAL),(G,CREAM,Y),(MINT,G,CORAL)]
R={
"reel-f-meal-prep":reel("Meal prep made simple:",["3 steps"],[(["Pick a protein"],["Chicken, beans, eggs","or tofu."]),(["Cook a grain"],["Rice, quinoa or oats","in one big batch."]),(["Chop veggies"],["Ready-to-eat veggies make","healthy meals easy."])],["Prep once.","Eat all week."],C3),
"reel-g-fiber":reel("3 easy ways to",["eat more","fiber"],[(["Go whole grain"],["Swap white bread or rice","for whole-grain."]),(["Add beans"],["Toss them into soups,","salads and bowls."]),(["Snack on fruit"],["Apples, pears and berries","are fiber-friendly."])],["Add fiber","slowly."],C3,NIGHT),
"reel-h-posture":reel("Quick posture check:",["3 steps"],[(["Feet flat"],["Plant both feet on","the floor."]),(["Shoulders back"],["Relax them down","and away from your ears."]),(["Screen at eye level"],["Raise your screen so you","are not looking down."])],["Check in.","Reset."],C3),
"reel-i-habits":reel("How to build a habit:",["3 tips"],[(["Start small"],["Make it so easy","you can not skip it."]),(["Same time daily"],["Attach it to something","you already do."]),(["Track it"],["Mark a calendar each","time you do it."])],["Small steps","add up."],C3,NIGHT),
"reel-j-breakfast":reel("3 quick",["breakfast","ideas"],[(["Overnight oats"],["Oats, milk and fruit","prepped the night before."]),(["Veggie omelet"],["Eggs with peppers","and spinach."]),(["Yogurt parfait"],["Greek yogurt, berries","and a little granola."])],["Save for","tomorrow."],C3),
}
def simple(name,folder,bg,fg,acc,small,big,sub,deco):
    b=deco+t([small],90,640,54,acc,700)+t(big,90,780,104,fg,800,lh=1.1)+t(sub,90,1150,44,fg,500,lh=1.35)
    save(name,page(1080,1350,bg,b,fg),1080,1350,folder)
eye=f'<circle cx="840" cy="320" r="130" fill="{Y}"/><circle cx="840" cy="320" r="62" fill="{G}"/><circle cx="866" cy="294" r="18" fill="{CREAM}"/>'
heart=f'<path d="M840 420 C700 320 740 200 820 215 C860 222 840 260 840 260 C840 260 820 222 860 215 C940 200 980 320 840 420Z" fill="{CORAL}"/>'
sun=''.join(f'<circle cx="840" cy="320" r="{r}" fill="{c}" opacity="{o}"/>' for r,c,o in [(150,Y,.35),(105,AM,.7),(60,OR,1)])
simple("post-2020","simple-2020",CREAM,G,CORAL,"Eye care tip",["Every 20 minutes,","look 20 feet away","for 20 seconds."],["The 20-20-20 rule gives","your eyes a break from screens."],eye)
simple("post-gratitude","simple-gratitude",G,CREAM,Y,"Daily habit",["Write down","one good thing","from today."],["It takes 30 seconds.","Try it before bed tonight."],sun)
simple("post-friend","simple-friend",MINT,G,CORAL,"Connection counts",["Call or text","a friend","today."],["A quick check-in can lift","your day and theirs."],heart)
W,H=1080,1350
def carousel(folder,cover,items,cta_big,cta_sub,bgc,fgc):
    S=[]
    h=''.join(cover[0])
    S.append(page(W,H,bgc,t([cover[0]],90,330,84,fgc,700)+t([cover[1]],90,560,190,Y if bgc==G else CORAL,800,lh=1)+t([cover[2]],90,780,190,Y if bgc==G else CORAL,800,lh=1)+t(["Swipe"],890,1120,40,fgc,700,"end")+f'<path d="M915 1105 L975 1105 M953 1082 L976 1105 L953 1128" stroke="{fgc}" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"/>',fgc,1,6))
    n=len(items)+2
    for i,(bg,fg,ico,ti,su) in enumerate(items,2):
        S.append(page(W,H,bg,t([cover[3]],90,170,44,fg,600,op=.8)+ico+t(ti,90,830,96,fg,800,lh=1.1)+t(su,94,830+len(ti)*96*1.1+30,44,fg,500,lh=1.35,op=.9),fg,i,6))
    S.append(page(W,H,G,t(cta_big,90,420,150,CREAM,800,lh=1)+t(cta_sub,94,880,52,CREAM,500,lh=1.35)+t(["General info only, not medical advice."],94,1130,34,CREAM,500,op=.75),CREAM,6,6))
    for i,s in enumerate(S,1): save(f"slide{i}",s,W,H,folder)
circ=lambda c,n=3:''.join(f'<circle cx="{450+i*100}" cy="{420-(i%2)*70}" r="62" fill="{c}"/>' for i in range(n))
bar=lambda c:''.join(f'<rect x="{440+i*90}" y="{520-h}" width="60" height="{h}" rx="30" fill="{c}"/>' for i,h in enumerate([160,260,210,300]))
drop=lambda c:f'<path d="M540 260 Q650 400 650 470 A110 110 0 0 1 430 470 Q430 400 540 260Z" fill="{c}"/>'
moon=lambda c,b:f'<circle cx="540" cy="420" r="130" fill="{c}"/><circle cx="600" cy="385" r="115" fill="{b}"/>'
carousel("carousel-swaps",("Easy swaps","that add","up","Swap idea"),[
 (CREAM,G,drop(MINT),["Swap soda for","sparkling water"],["Add lemon or berries","for flavor."]),
 (MINT,G,circ(Y),["Swap chips for","popcorn"],["Air-popped is a crunchy","whole-grain snack."]),
 (Y,G,bar(G),["Swap white rice","for brown rice"],["Or quinoa: more fiber","in every bowl."]),
 (CORAL,G,circ(CREAM),["Swap sour cream","for Greek yogurt"],["More protein, same creaminess."])],
 ["Save this","for your","next shop."],["Which swap will you try?","Tell us below."],G,CREAM)
carousel("carousel-checklist",("Your weekly","wellness","checklist","Checklist"),[
 (CREAM,G,bar(CORAL),["Move most days"],["Pick activity you enjoy."]),
 (MINT,G,circ(CORAL),["Fill half your plate","with produce"],["Fruit and veggies, any color."]),
 (Y,G,drop(G),["Drink water","through the day"],["Keep a bottle close."]),
 (CORAL,G,moon(CREAM,CORAL),["Wind down at","a steady bedtime"],["Dim lights and put screens away."])],
 ["Save this","checklist."],["How many can you check off?","Tell us below."],G,CREAM)
if __name__=="__main__":
    os.makedirs("reels",exist_ok=True)
    for n,sc in R.items(): print(make_reel(n,sc))
