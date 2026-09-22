"""Render fictional interface illustrations for the README. Requires Pillow.

These assets illustrate the sample run; they are not connected account captures.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ASSETS = Path(__file__).resolve().parents[1] / "assets"
ASSETS.mkdir(exist_ok=True)
FONT = "/usr/share/fonts/opentype/urw-base35/NimbusSans-Regular.otf"
BOLD = "/usr/share/fonts/opentype/urw-base35/NimbusSans-Bold.otf"
PAPER, WHITE, INK = "#F6F7F3", "#FFFFFF", "#172A26"
MUTED, FAINT, LINE = "#64736D", "#8B9992", "#DCE5DF"
GREEN, PALE, SOFT = "#146B55", "#E5F3EC", "#F0F4EF"

class Art:
    def __init__(self, w, h, bg=PAPER):
        self.w, self.h = w, h
        self.im = Image.new("RGB", (w*2, h*2), bg)
        self.d = ImageDraw.Draw(self.im)
    def box(self, x, y, w, h, fill, r=0, outline=None):
        self.d.rounded_rectangle((x*2,y*2,(x+w)*2,(y+h)*2),r*2,fill,outline,2)
    def line(self,x1,y1,x2,y2,color=LINE,weight=1):
        self.d.line((x1*2,y1*2,x2*2,y2*2),fill=color,width=weight*2)
    def text(self,x,y,s,size=18,color=INK,bold=False,anchor=None):
        f=ImageFont.truetype(BOLD if bold else FONT,size*2)
        self.d.text((x*2,y*2),s,font=f,fill=color,anchor=anchor)
    def dot(self,x,y,r,color):
        self.box(x-r,y-r,2*r,2*r,color,r)
    def image(self):
        return self.im.resize((self.w,self.h),Image.Resampling.LANCZOS)
    def save(self,name):
        self.image().save(ASSETS/name,optimize=True)

def mark(a,x,y,s=36):
    a.box(x,y,s,s,GREEN,9)
    for yy in (11,17): a.line(x+9,y+yy,x+s-9,y+yy,WHITE,2)
    a.box(x+9,y+23,s-18,4,"#F2BC69",2)

def brand(a,right):
    mark(a,58,38)
    a.text(105,42,"JOB SEARCH COLLECTOR",17,INK,True)
    a.text(right,48,"ILLUSTRATIVE / FICTIONAL DATA",12,MUTED,True,"ra")

def chrome(a,x,y,w,name):
    a.box(x,y,w,42,SOFT,9)
    a.box(x,y+28,w,14,SOFT)
    for dx in (17,28,39): a.dot(x+dx,y+21,3,"#B3C1B7")
    a.text(x+58,y+12,name,15,MUTED,True)

def badge(a,x,y,label,applied=False,small=False):
    width=89 if small else 103
    a.box(x,y,width,27,"#E8F0FA" if applied else PALE,14)
    a.text(x+12,y+5,label,14,"#285C88" if applied else GREEN,True)

def table(a,x,y,w,compact=False,state="reply",include_example=True):
    h=266 if compact else 412
    a.box(x+3,y+7,w,h,"#E7EBE5",12)
    a.box(x,y,w,h,WHITE,12,LINE)
    chrome(a,x+1,y+1,w-2,"Job_Search_Collector  /  Tracker")
    a.box(x+1,y+42,w-2,37,WHITE)
    a.text(x+22,y+52,"Tracker",16,INK,True)
    a.text(x+w-22,y+54,"14 columns  ·  selected fields shown",13,FAINT,anchor="ra")
    top=y+79
    a.box(x+1,top,w-2,39,SOFT)
    edges=[x+int(w*f) for f in (0,.105,.245,.472,.635,.79,.895,1)]
    labels=("Status","Company","Title","Notes","ReceivedAt","AppliedAt","RespondedAt")
    for i,label in enumerate(labels):
        a.text(edges[i]+12,top+12,label,13 if compact else 16,MUTED,True)
    a.line(x,top+39,x+w,top+39)
    if compact:
        rows=[("Candidate","Northstar Labs","Product Designer","Consumer onboarding","Sep 8","","")]
        if include_example:
            rows.append(("Candidate" if state=="candidate" else "Applied","ExampleCo",
                         "Senior Product Designer","B2C funnel + design systems","Sep 7",
                         "Sep 9" if state in ("applied","reply") else "",
                         "Sep 12" if state=="reply" else ""))
        rowheight=69
    else:
        rows=[
            ("Candidate","Northstar Labs","Product Designer","Consumer onboarding","Sep 8","",""),
            ("Applied","SampleWorks","Product Designer","Application confirmed","Sep 6","Sep 9",""),
            ("Applied","ExampleCo","Senior Product Designer","B2C funnel + design systems","Sep 7","Sep 9","Sep 12")]
        rowheight=92
    yy=top+39
    for index,row in enumerate(rows):
        if row[1]=="ExampleCo":
            a.box(x+1,yy,w-2,rowheight,"#F4FAF6")
            a.box(x+1,yy,4,rowheight,GREEN)
        for i,value in enumerate(row):
            cx=edges[i]+12
            if i==0:
                badge(a,cx,yy+(16 if compact else 22),value,value=="Applied",compact)
            else:
                a.text(cx,yy+(24 if compact else 29),value or "·",
                       13 if compact else 16,
                       INK if i in (1,2) else MUTED, i==1 and row[1]=="ExampleCo")
        yy+=rowheight
        a.line(x,yy,x+w,yy)
    if not compact:
        a.box(x+1,y+h-22,w-2,21,WHITE)
        a.box(x+17,y+h-27,98,27,PALE,8)
        a.text(x+33,y+h-22,"Tracker",14,GREEN,True)

def mail(a,step):
    x,y,w=58,237,450
    a.box(x,y,w,339,WHITE,12,LINE)
    chrome(a,x+1,y+1,w-2,"Gmail  /  Job alerts")
    if step<3:
        sender,subject,date="LinkedIn Job Alerts","Senior Product Designer at ExampleCo","SEP 7"
        lines=("ExampleCo is hiring in Toronto (hybrid).",
               "Improve the consumer application funnel",
               "and extend a design system across teams.")
    elif step==3:
        sender,subject,date="ExampleCo Careers","We received your application","SEP 9"
        lines=("Your application for Senior Product Designer",
               "at ExampleCo has been received.","")
    else:
        sender,subject,date="ExampleCo Recruiting","Re: Senior Product Designer","SEP 12"
        lines=("Thank you for applying. Could we schedule",
               "a conversation next week?","")
    a.dot(x+39,y+87,18,PALE)
    a.text(x+39,y+78,sender[0],18,GREEN,True,"ma")
    a.text(x+72,y+65,sender,18,INK,True)
    a.text(x+w-23,y+69,date,12,MUTED,True,"ra")
    a.line(x+23,y+113,x+w-23,y+113)
    a.text(x+24,y+139,subject,20,INK,True)
    for i,line in enumerate(lines):
        if line: a.text(x+24,y+190+i*31,line,17,MUTED)
    a.box(x+24,y+298,115,24,SOFT,5)
    a.text(x+34,y+302,"Inbox / Jobs",13,GREEN,True)

def review(a,step):
    x,y,w=528,237,1542
    a.box(x,y,w-x,339,WHITE,12,LINE)
    chrome(a,x+1,y+1,w-x-2,"ChatGPT  /  Daily review")
    if step==0:
        a.text(x+26,y+76,"PROFILE MATCHING",13,GREEN,True)
        a.text(x+26,y+119,"Reading your job alert…",27,INK,True)
        a.text(x+26,y+170,"Comparing the posting against your private profile",17,MUTED)
        a.text(x+26,y+201,"and checking the tracker for duplicates.",17,MUTED)
        a.box(x+26,y+273,374,7,SOFT,4)
        a.box(x+26,y+273,156,7,GREEN,4)
    else:
        a.box(x+26,y+69,132,28,PALE,14)
        a.text(x+39,y+74,"Strong match",15,GREEN,True)
        a.text(x+26,y+111,"ExampleCo · Senior Product Designer",24,INK,True)
        a.line(x+26,y+157,w-25,y+157)
        for i,line in enumerate(("B2C application funnel ownership",
                                 "Design system work across product teams",
                                 "Toronto hybrid matches your location")):
            a.dot(x+34,y+185+i*34,3,GREEN)
            a.text(x+48,y+172+i*34,line,17,MUTED)
        a.text(x+26,y+291,"One role  ·  duplicate alert ignored",14,GREEN,True)

# Still: visible record names and dates match examples/sample-run.md.
a=Art(1600,830)
brand(a,1542)
a.text(58,115,"THE OUTPUT",13,GREEN,True)
a.text(58,143,"A tracker that stays current.",43,INK,True)
a.text(58,201,"Relevant roles arrive as rows. Clear confirmations update the same row.",20,MUTED)
table(a,58,263,1484)
a.text(60,718,"ExampleCo: discovered Sep 7  →  applied Sep 9  →  reply Sep 12",19,GREEN,True)
a.text(60,755,"Matching reasons live in Notes. Status stays Applied after a reply; no numeric fit score is added.",17,MUTED)
a.save("tracker-preview.png")

# Five held scenes, 14.5 seconds, with actual changes to the mail and row.
frames=[]
labels=("Alert received","Fit evaluated","Candidate row created",
        "Application confirmation found","Recruiter reply found")
for step in range(5):
    a=Art(1600,960)
    brand(a,1542)
    a.text(58,106,"From job alert to tracked reply.",42,INK,True)
    a.text(58,160,"A role is reviewed, added once, then updated when clear email evidence arrives.",19,MUTED)
    mail(a,step)
    review(a,step)
    a.text(58,613,"Tracker",21,INK,True)
    a.text(1542,616,"SELECTED FIELDS  /  14 TOTAL",12,MUTED,True,"ra")
    state="candidate" if step<3 else ("applied" if step==3 else "reply")
    table(a,58,646,1484,True,state,step>=2)
    a.box(58,915,1484,4,LINE,2)
    a.box(58,915,int(1484*(step+1)/5),4,GREEN,2)
    a.text(58,926,f"{step+1} / 5   {labels[step]}",16,GREEN,True)
    a.text(1542,928,"The user applies before the confirmation arrives. No auto-apply.",
           13,MUTED,anchor="ra")
    frames.append(a.image())
frames[0].save(ASSETS/"sample-workflow.gif",save_all=True,append_images=frames[1:],
               duration=[2600,2900,2900,2900,3200],loop=0,optimize=True,disposal=2)

# The share card keeps the same type, mark, palette and fictional record.
a=Art(1280,640,INK)
mark(a,60,58,42)
a.text(116,67,"JOB SEARCH COLLECTOR",18,WHITE,True)
a.text(60,153,"A CHATGPT JOB SEARCH WORKFLOW",13,"#F2BC69",True)
a.text(60,204,"From job alerts",55,WHITE,True)
a.text(60,270,"to one clear tracker.",55,WHITE,True)
a.text(60,365,"Review the fit. Remove duplicates.",24,"#C9D9CF")
a.text(60,400,"Track applications and replies.",24,"#C9D9CF")
a.box(60,516,446,44,"#264539",22)
a.text(80,528,"Gmail  +  ChatGPT  +  Google Sheets",18,WHITE,True)
a.box(710,124,510,383,WHITE,14)
chrome(a,711,125,508,"Job_Search_Collector / Tracker")
a.box(711,167,508,45,SOFT)
for s,x in (("Status",731),("Company",848),("Role",1000)):
    a.text(x,184,s,16,MUTED,True)
a.line(711,212,1219,212)
a.text(733,234,"Candidate",16,GREEN,True)
a.text(848,234,"Northstar Labs",16,INK)
a.text(1000,234,"Product Designer",16,INK)
a.line(711,278,1219,278)
a.box(711,279,508,78,"#F4FAF6")
a.box(711,279,5,78,GREEN)
a.text(733,301,"Applied",16,"#285C88",True)
a.text(848,301,"ExampleCo",17,INK,True)
a.text(1000,301,"Senior Product",16,INK)
a.text(1000,324,"Designer",16,INK)
a.line(711,357,1219,357)
a.text(733,390,"Application confirmed",17,MUTED)
a.text(733,423,"Recruiter reply detected",17,MUTED)
a.box(733,468,177,25,PALE,12)
a.text(746,472,"FICTIONAL PREVIEW",13,GREEN,True)
a.save("social-preview.png")
print("Rendered the three README assets")
