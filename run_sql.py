import sqlite3, pandas as pd, glob
con = sqlite3.connect("data/retail.db")
con.executescript(open("sql/01_customer_orders.sql").read())
res = {}
for f in sorted(glob.glob("sql/0[2-8]*.sql")):
    d = pd.read_sql(open(f).read(), con); res[f]=d
    d.to_csv("data/"+f.split("/")[1].replace(".sql",".csv"), index=False)
    print("=="+f); print(d.head(12).to_string(index=False) if "08" not in f else d.gap_days.describe())
