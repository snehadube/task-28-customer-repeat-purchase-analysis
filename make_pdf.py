import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, Preformatted
NAVY=colors.HexColor("#1f3a8a"); ORG=colors.HexColor("#f97316")
ss=getSampleStyleSheet()
H1=ParagraphStyle("H1",parent=ss["Heading1"],textColor=NAVY,fontSize=16,spaceBefore=10,spaceAfter=6)
H2=ParagraphStyle("H2",parent=ss["Heading2"],textColor=NAVY,fontSize=12,spaceBefore=8,spaceAfter=4)
B=ParagraphStyle("B",parent=ss["BodyText"],fontSize=10,leading=14)
BL=ParagraphStyle("BL",parent=B,leftIndent=14,bulletIndent=4)
CODE=ParagraphStyle("C",fontName="Courier",fontSize=7.5,leading=9.5,backColor=colors.HexColor("#f1f5f9"),leftIndent=4)
def bl(items): return [Paragraph(i,BL,bulletText="•") for i in items]
def tbl(data,widths=None,hl=True):
    CS=ParagraphStyle("cs",parent=B,fontSize=9,leading=11)
    HS=ParagraphStyle("hs",parent=CS,textColor=colors.white,fontName="Helvetica-Bold")
    data=[[Paragraph(str(c),HS if i==0 else CS) if isinstance(c,str) else c for c in r] for i,r in enumerate(data)]
    t=Table(data,colWidths=widths,repeatRows=1)
    t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),NAVY),("TEXTCOLOR",(0,0),(-1,0),colors.white),
      ("FONTSIZE",(0,0),(-1,-1),9),("GRID",(0,0),(-1,-1),0.4,colors.HexColor("#cbd5e1")),
      ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white,colors.HexColor("#f8fafc")]),("ALIGN",(1,0),(-1,-1),"CENTER"),
      ("VALIGN",(0,0),(-1,-1),"MIDDLE")])); return t
def img(p,w=15.5): 
    from PIL import Image as PI; iw,ih=PI.open(p).size; return Image(p,width=w*cm,height=w*cm*ih/iw)
seg=pd.read_csv("data/03_segment_table.csv"); a=pd.read_csv("data/04_aov_compare.csv"); b=pd.read_csv("data/05_first_vs_later_aov.csv")
co=pd.read_csv("data/06_monthly_retention.csv")
S=[]
S+= [Spacer(1,3*cm),Paragraph("Customer Repeat Purchase Analysis",ParagraphStyle("T",parent=ss["Title"],textColor=NAVY,fontSize=26,leading=32)),
 Paragraph("Measuring repeat purchase behaviour and identifying repeat-customer segments",ParagraphStyle("st",parent=B,fontSize=13,textColor=ORG)),
 Spacer(1,1*cm),Paragraph("<b>Prepared by:</b> Sneha<br/><b>Track:</b> Data Analytics Intern, Veda Technology<br/><b>Tools:</b> Python (pandas, matplotlib), SQL (SQLite)<br/><b>Dataset:</b> Online Retail (UK online gift retailer), 1 Dec 2010 to 9 Dec 2011",B),
 Spacer(1,1*cm),Paragraph("<b>Headline result:</b> 65.6% of customers bought more than once, and they generated 93.1% of revenue.",ParagraphStyle("hl",parent=B,fontSize=12,backColor=colors.HexColor("#eff6ff"),borderPadding=8)),PageBreak()]
S+= [Paragraph("1. Objective and Approach",H1),
 Paragraph("The goal is to understand loyalty by measuring how many customers come back to buy again, grouping them into segments, and comparing the value of first-time and repeat buyers. The work was done in two layers: Python for cleaning and charts, and SQL (window functions, CTEs, views) for every metric.",B),
 Paragraph("Definitions used",H2)]
S+= bl(["<b>Order:</b> one unique Invoice number (all line items of a basket).","<b>Repeat customer:</b> a customer with <b>2 or more distinct orders</b> in the data period. One-time customer = exactly 1 order.",
 "<b>Repeat rate:</b> repeat customers / total identified customers x 100.","<b>AOV (Average Order Value):</b> total revenue / number of orders, where revenue = Quantity x Unit Price.",
 "<b>Segments:</b> One-time (1 order), Occasional (2-3), Regular (4-9), Loyal (10+)."])
S+= [Paragraph("2. Data and Cleaning",H1),Paragraph("The raw file has 541,910 transaction lines. Only rows that can support a customer-level analysis were kept.",B)]
log=pd.read_csv("data/cleaning_log.csv",index_col=0).iloc[:,0]
S+= [tbl([["Step","Rows affected"],["Raw rows",f"{int(log.raw_rows):,}"],["Removed: missing Customer ID (cannot be tracked)",f"{int(log.missing_customer):,}"],
 ["Removed: cancellations (invoice starts with 'C')",f"{int(log.cancel_rows):,}"],["Removed: zero/negative quantity or price",f"{int(log.bad_qty_price):,}"],
 ["Removed: exact duplicate rows",f"{int(log.dups):,}"],["<b>Clean rows used</b>",f"<b>{int(log.clean_rows):,}</b>"],
 ["Unique customers / orders",f"{int(log.customers):,} / {int(log.orders):,}"]],[11*cm,4.5*cm]),
 Spacer(1,6),Paragraph("<b>Note:</b> the file is named 'online_retail_II' but its contents (541,910 rows, Dec 2010 to Dec 2011) match the original Online Retail dataset. The method is unchanged.",B),PageBreak()]
S+= [Paragraph("3. Results",H1),Paragraph("3.1 Repeat rate",H2),
 Paragraph("Out of <b>4,338</b> customers, <b>2,845</b> placed two or more orders, giving a <b>repeat rate of 65.58%</b>. UK and non-UK customers behave almost identically (65.6% vs 65.8%).",B),img("charts/c1_repeat_rate.png",7),
 Paragraph("3.2 Segment table",H2)]
rows=[["Segment","Count","% Cust.","Orders","Revenue (£)","% Rev.","AOV (£)","Avg orders"]]
for _,r in seg.iterrows(): rows.append([r.segment.split(". ")[1],f"{r.customers:,}",f"{r.pct_customers}%",f"{r.orders:,}",f"{r.revenue:,.0f}",f"{r.pct_revenue}%",f"{r.aov:,.0f}",f"{r.avg_orders_per_cust}"])
rows.append(["<b>Total</b>","4,338","100%","18,532","8,887,227","100%","480","4.27"])
S+= [tbl(rows,[3.6*cm,1.9*cm,1.6*cm,1.7*cm,2.4*cm,1.5*cm,1.6*cm,1.8*cm]),Spacer(1,6),img("charts/c2_segments.png",14),PageBreak()]
S+= [Paragraph("3.3 First-time vs repeat AOV",H2),
 Paragraph(f"Two comparisons were made. (A) By customer type: one-time customers have an AOV of <b>£{a.aov[a.customer_type=='One-time'].iloc[0]:,.0f}</b> against <b>£{a.aov[a.customer_type=='Repeat'].iloc[0]:,.0f}</b> for repeat customers (+18%). (B) Within repeat customers: their first order averages <b>£{b.aov.iloc[0]:,.0f}</b> and later orders <b>£{b.aov.iloc[1]:,.0f}</b> (+15%), so customers spend more once they trust the shop.",B),img("charts/c3_aov.png",14),
 Paragraph("3.4 Cohort return rate",H2),
 Paragraph("Customers were grouped by the month of their first order, and we measured how many came back in any later month. The December 2010 cohort returned 86.6% of the time. Later cohorts show lower rates mainly because they had less time to return before the data ended, so only mature cohorts should be compared.",B),img("charts/c4_cohort.png",13.5),PageBreak()]
S+= [Paragraph("3.5 Time between orders",H2),
 Paragraph("The median gap between consecutive orders of repeat customers is <b>22 days</b>; 59% of repeat orders arrive within 30 days and 79% within 60 days. This suggests a natural re-engagement window of about 4 to 8 weeks.",B),img("charts/c5_gap.png",13.5),
 Paragraph("4. Key Insights",H1)]
S+= bl(["<b>Two out of three customers come back.</b> Repeat rate is 65.6%, which is high for retail and reflects a B2B-style wholesale customer base.",
 "<b>Repeat customers drive the business.</b> They are 65.6% of customers but 93.1% of revenue and 91.9% of orders.",
 "<b>Loyal customers are a small but powerful group.</b> Only 9% of customers (10+ orders) produce 51.3% of revenue, with the highest AOV (£596).",
 "<b>Spend grows with trust.</b> Repeat customers' later orders are about 15% larger than their first order.",
 "<b>One-time buyers are a third of the base (34.4%)</b> yet only 6.9% of revenue, so the upside lies in converting them to a second order.",
 "<b>Timing matters.</b> Most second purchases happen within 30 to 60 days, so follow-ups should land in that window.",
 "<b>Geography does not change loyalty.</b> UK and non-UK repeat rates are within 0.2 points."])
S+= [Paragraph("5. Recommendations",H1)]
S+= bl(["Send a second-purchase nudge (email or offer) 3 to 4 weeks after a first order to convert one-time buyers.","Create a VIP / wholesale programme for the 391 Loyal customers (early access, volume pricing) to protect 51% of revenue.",
 "Run win-back campaigns on customers who pass about 60 days without ordering.","Track repeat rate and cohort return rate monthly as core loyalty KPIs."])
S+= [Paragraph("6. Interview Questions",H1),
 Paragraph("<b>How do you define a repeat customer?</b> A customer with two or more distinct orders (unique invoices) in the analysis window. I count orders, not line items, and exclude cancellations and rows with no Customer ID.",B),Spacer(1,4),
 Paragraph("<b>Why track repeat rate?</b> Retaining customers is cheaper than acquiring new ones, repeat buyers spend more and generate most revenue, and repeat rate shows whether product, price and service actually build loyalty.",B),
 Paragraph("7. Limitations",H1)]
S+= bl(["Customers without an ID (25% of rows, mostly guest checkouts) cannot be tracked, so the rate applies to identified customers only.","The window is about 12 months: customers whose first order was late in the period had little time to repeat, which slightly understates the true repeat rate.","Revenue is gross of returns that are not linked to the original invoice."])
S+= [PageBreak(),Paragraph("Appendix: Core SQL",H1),Paragraph("Customer-level view (repeat flag and segment)",H2),Preformatted(open("sql/01_customer_orders.sql").read(),CODE),
 Paragraph("First vs later order AOV (window function)",H2),Preformatted(open("sql/05_first_vs_later_aov.sql").read(),CODE)]
def foot(c,d):
    c.setFont("Helvetica",8); c.setFillColor(colors.grey); c.drawString(2*cm,1.2*cm,"Customer Repeat Purchase Analysis | Sneha | Veda Technology"); c.drawRightString(A4[0]-2*cm,1.2*cm,str(d.page))
SimpleDocTemplate("/mnt/user-data/outputs/Customer_Repeat_Purchase_Analysis_Report.pdf",pagesize=A4,leftMargin=2*cm,rightMargin=2*cm,topMargin=1.8*cm,bottomMargin=2*cm,title="Customer Repeat Purchase Analysis",author="Sneha").build(S,onFirstPage=foot,onLaterPages=foot)
