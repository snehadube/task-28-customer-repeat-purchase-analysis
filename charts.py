import pandas as pd, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"font.size":10,"axes.spines.top":False,"axes.spines.right":False})
NAVY="#1f3a8a"; ORG="#f97316"; GR="#94a3b8"
seg=pd.read_csv("data/03_segment_table.csv"); lab=[s.split(". ")[1] for s in seg.segment]
lab=[l.replace(" (","\n(") for l in lab]
# 1 repeat vs one-time donut
rr=pd.read_csv("data/02_repeat_rate.csv").iloc[0]
fig,ax=plt.subplots(figsize=(4.2,4.2))
ax.pie([rr.repeat_customers,rr.total_customers-rr.repeat_customers],labels=["Repeat","One-time"],colors=[NAVY,GR],
  autopct="%1.1f%%",startangle=90,wedgeprops=dict(width=0.45),textprops={"color":"black"},pctdistance=0.78)
for t in ax.texts:
    if "%" in t.get_text(): t.set_color("white"); t.set_fontweight("bold")
ax.set_title("Repeat vs One-time Customers"); plt.tight_layout(); plt.savefig("charts/c1_repeat_rate.png",dpi=200); plt.close()
# 2 customers vs revenue share
import numpy as np
x=np.arange(len(seg)); fig,ax=plt.subplots(figsize=(7,3.8))
ax.bar(x-0.2,seg.pct_customers,0.4,label="% of customers",color=GR)
ax.bar(x+0.2,seg.pct_revenue,0.4,label="% of revenue",color=NAVY)
for i,(a,b) in enumerate(zip(seg.pct_customers,seg.pct_revenue)):
    ax.text(i-0.2,a+0.8,f"{a}%",ha="center",fontsize=9); ax.text(i+0.2,b+0.8,f"{b}%",ha="center",fontsize=9)
ax.set_xticks(x); ax.set_xticklabels(lab); ax.legend(frameon=False); ax.set_title("Customer Share vs Revenue Share by Segment")
plt.tight_layout(); plt.savefig("charts/c2_segments.png",dpi=200); plt.close()
# 3 AOV
a=pd.read_csv("data/04_aov_compare.csv"); b=pd.read_csv("data/05_first_vs_later_aov.csv")
fig,axs=plt.subplots(1,2,figsize=(7.5,3.6))
axs[0].bar(a.customer_type,a.aov,color=[GR,NAVY]); axs[0].set_title("AOV: One-time vs Repeat customers")
for i,v in enumerate(a.aov): axs[0].text(i,v+8,f"£{v:,.0f}",ha="center")
axs[1].bar(["First order","Repeat orders\n(2nd+)"],b.aov.values,color=[GR,ORG]); axs[1].set_title("AOV: 1st vs later orders\n(repeat customers)")
for i,v in enumerate(b.aov.values): axs[1].text(i,v+8,f"£{v:,.0f}",ha="center")
for ax in axs: ax.set_ylim(0,600)
plt.tight_layout(); plt.savefig("charts/c3_aov.png",dpi=200); plt.close()
# 4 cohort
c=pd.read_csv("data/06_monthly_retention.csv")
fig,ax=plt.subplots(figsize=(7,3.6)); ax.plot(c.cohort,c.pct_returned,marker="o",color=NAVY)
ax.set_title("% of Cohort Who Ordered Again (by first-purchase month)"); ax.set_ylabel("%"); plt.xticks(rotation=45)
ax.annotate("Recent cohorts had\nless time to return",xy=(11,11),xytext=(7.2,15),arrowprops=dict(arrowstyle="->"),fontsize=9)
plt.tight_layout(); plt.savefig("charts/c4_cohort.png",dpi=200); plt.close()
# 5 gap
g=pd.read_csv("data/08_gap_days.csv"); fig,ax=plt.subplots(figsize=(7,3.4))
ax.hist(g.gap_days.clip(upper=180),bins=36,color=NAVY); ax.axvline(g.gap_days.median(),color=ORG,ls="--")
ax.text(g.gap_days.median()+3,ax.get_ylim()[1]*0.85,f"Median = {g.gap_days.median():.0f} days",color=ORG)
ax.set_title("Days Between Consecutive Orders (capped at 180)"); ax.set_xlabel("days")
plt.tight_layout(); plt.savefig("charts/c5_gap.png",dpi=200); plt.close()
print("ok")
