"""Render fictional README previews. Requires Pillow; not needed to use the workflow."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
ASSETS.mkdir(exist_ok=True)
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
C = dict(bg='#101B2B', panel='#18283B', raised='#20334A', line='#33475B', white='#F4F8FA', muted='#A7BAC7', mint='#72E0B6', blue='#92C7FA', amber='#FFD38A', sheet='#F5F8FB', ink='#26394B', pale='#E7EFF4')

def f(size, bold=False): return ImageFont.truetype(BOLD if bold else FONT, size)
def rr(d, box, fill, radius=18, outline=None, width=1): d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)
def txt(d, at, s, size=20, color=None, bold=False): d.text(at, s, font=f(size,bold), fill=color or C['white'])
def pill(d, box, label, fill, fg=None, size=16):
    rr(d,box,fill,16); txt(d,(box[0]+13,box[1]+(box[3]-box[1]-size)//2-2),label,size,fg or C['ink'],True)

def logo(d,x,y):
    rr(d,(x,y,x+49,y+49),C['mint'],13)
    d.line((x+13,y+26,x+22,y+35,x+38,y+15),fill=C['bg'],width=6,joint='curve')

def base(w,h,title,subtitle):
    im=Image.new('RGB',(w,h),C['bg']);d=ImageDraw.Draw(im)
    logo(d,55,43);txt(d,(118,48),title,31,bold=True)
    txt(d,(58,111),subtitle,20,C['muted'])
    return im,d

# Tracker screenshot: selected columns from the real 14-column schema.
im,d=base(1400,710,'Job Search Collector','Illustrative Tracker preview  |  fictional data  |  selected columns')
rr(d,(55,165,1345,635),C['sheet'],18)
rr(d,(55,165,1345,226),'#DFECEB',18)
d.rectangle((55,205,1345,226),fill='#DFECEB')
txt(d,(84,180),'Tracker',23,C['ink'],True)
pill(d,(1124,178,1318,212),'SAMPLE DATA','#CDE5DD','#22634E',14)
cols=[('Status',84,145),('Company',240,170),('Title',430,264),('Location',715,163),('ReceivedAt',895,167),('AppliedAt',1085,169)]
d.rectangle((55,226,1345,284),fill='#EDF3F6')
for label,x,width in cols: txt(d,(x,242),label,16,C['ink'],True)
for y in (284,386,488):d.line((55,y,1345,y),fill='#D6E2E9',width=2)
rows=[('Candidate','Northstar Labs','Product Designer','Remote, Canada','Sep 8, 2026',''),('Applied','SampleWorks','Product Designer','Remote, Canada','Sep 6, 2026','Sep 9, 2026'),('Applied','ExampleCo','Senior Product Designer','Toronto, ON','Sep 7, 2026','Sep 9, 2026')]
for j,row in enumerate(rows):
    y=301+j*102
    pill(d,(84,y+9,206,y+44),row[0],'#DAEEE7' if row[0]=='Candidate' else '#DFE9FB','#286856' if row[0]=='Candidate' else '#2D5F9A',15)
    for val,x in zip(row[1:],[240,430,715,895,1085]):txt(d,(x,y+12),val,17,C['ink'])
    note=['Fit: consumer onboarding','Application confirmation detected','Recruiter reply detected'][j]
    txt(d,(240,y+54),note,15,'#627C8D')
txt(d,(75,653),'Full Tracker: 14 columns. Matching reasons are recorded in Notes; there is no numeric fit score.',16,C['muted'])
im.save(ASSETS/'tracker-preview.png',optimize=True)

# Animated mock interface: fictional data, never a recording of connected accounts.
frames=[]
for step in range(4):
    im,d=base(1100,615,'From job alert to tracked reply','Illustrative demo  |  fictional data  |  connected behavior varies')
    panels=[(55,165,365,510),(390,165,700,510),(725,165,1045,510)]
    for x1,y1,x2,y2 in panels: rr(d,(x1,y1,x2,y2),C['panel'],17,outline=C['line'],width=2)
    for x,label,num in [(75,'Gmail alert','01'),(410,'ChatGPT review','02'),(745,'Tracker','03')]:
        pill(d,(x,183,x+45,217),num,C['raised'],C['mint'],14)
        txt(d,(x+55,188),label,19,bold=True)
    # Email: visible from the first frame.
    rr(d,(74,239,346,451),C['raised'],13)
    txt(d,(90,256),'LinkedIn Job Alerts',15,C['muted'])
    txt(d,(90,291),'Senior Product',20,bold=True)
    txt(d,(90,321),'Designer at ExampleCo',16,C['white'])
    d.line((90,353,330,353),fill=C['line'],width=2)
    txt(d,(90,371),'Toronto  /  Hybrid',15,C['blue'])
    txt(d,(90,402),'B2C funnel, design system',13,C['muted'])
    # Match: appears in frame two, stays visible afterwards.
    if step>=1:
        pill(d,(409,245,558,281),'Strong match',C['mint'],C['bg'],16)
        txt(d,(410,311),'Why this fits',19,bold=True)
        txt(d,(410,349),'B2C funnel ownership',15,C['white'])
        txt(d,(410,381),'Design-system experience',15,C['white'])
        txt(d,(410,413),'Toronto hybrid preference',14,C['muted'])
    else:
        txt(d,(412,318),'Comparing with',18,C['muted'])
        txt(d,(412,349),'private profile ...',18,C['muted'])
    # Tracker: candidate row, then applied, then reply date.
    if step>=2:
        pill(d,(745,243,861,277),'Applied' if step>=2 else 'Candidate',C['blue'],C['bg'],16)
        txt(d,(745,304),'ExampleCo',19,bold=True)
        txt(d,(745,338),'Senior Product Designer',15,C['white'])
        d.line((745,374,1023,374),fill=C['line'],width=2)
        txt(d,(745,390),'AppliedAt  Sep 9',15,C['muted'])
        txt(d,(745,423),'RespondedAt  Sep 12' if step==3 else 'RespondedAt  —',15,C['mint'] if step==3 else C['muted'])
    else:
        txt(d,(746,312),'Candidate row',18,C['muted'])
        txt(d,(746,344),'created if permitted',15,C['muted'])
    d.line((365,335,386,335),fill=C['mint'],width=5)
    d.line((700,335,721,335),fill=C['mint'],width=5)
    labels=['Alert received','Fit evaluated','Application confirmed','Reply detected']
    txt(d,(56,541),f'{step+1}/4  {labels[step]}',16,C['mint'],True)
    for k in range(4):rr(d,(465+k*143,547,584+k*143,556),C['mint'] if k<=step else C['line'],5)
    frames.append(im)
frames[0].save(ASSETS/'sample-workflow.gif',save_all=True,append_images=frames[1:],duration=[2000]*4,loop=0,optimize=True)

# Use this PNG in GitHub Settings > Social preview; a settings change is separate from committing it.
im,d=base(1280,640,'Job Search Collector','Your job alerts, filtered and tracked with ChatGPT.')
rr(d,(55,222,1225,530),C['panel'],25,outline=C['line'],width=2)
labels=[('Gmail alerts',80,C['blue']),('Career fit',450,C['mint']),('One tracker',820,C['amber'])]
for i,(label,x,color) in enumerate(labels):
    rr(d,(x,267,x+326,454),C['raised'],20)
    d.ellipse((x+21,293,x+52,324),fill=color)
    txt(d,(x+21,351),label,27,bold=True)
    if i<2:txt(d,(x+338,341),'>',34,C['mint'],True)
txt(d,(56,557),'Illustrative workflow  •  Gmail + optional web discovery  •  Google Sheets',17,C['muted'])
im.save(ASSETS/'social-preview.png',optimize=True)
print('Rendered assets in',ASSETS)
