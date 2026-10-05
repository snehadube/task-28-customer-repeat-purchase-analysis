"""Customer Repeat Purchase Analysis - Python + SQL (SQLite)"""
import pandas as pd, sqlite3, os
RAW = "/mnt/user-data/uploads/online_retail_II.csv"
df = pd.read_csv(RAW, encoding="latin1")
df.columns = ["invoice","stock_code","description","quantity","invoice_date","price","customer_id","country"]
df["invoice_date"] = pd.to_datetime(df["invoice_date"], format="%m/%d/%y %H:%M")
raw_rows = len(df)
log = {"raw_rows": raw_rows}
log["missing_customer"] = int(df.customer_id.isna().sum())
df = df.dropna(subset=["customer_id"])
df["customer_id"] = df.customer_id.astype(int)
log["cancel_rows"] = int(df.invoice.astype(str).str.startswith("C").sum())
df = df[~df.invoice.astype(str).str.startswith("C")]
log["bad_qty_price"] = int(((df.quantity<=0)|(df.price<=0)).sum())
df = df[(df.quantity>0)&(df.price>0)]
df["revenue"] = df.quantity*df.price
log["dups"] = int(df.duplicated().sum())
df = df.drop_duplicates()
log["clean_rows"] = len(df)
log["customers"] = df.customer_id.nunique(); log["orders"]=df.invoice.nunique()
log["date_min"]=str(df.invoice_date.min()); log["date_max"]=str(df.invoice_date.max())
df["invoice_date"]=df.invoice_date.dt.strftime("%Y-%m-%d %H:%M:%S")
df.to_csv("data/clean_transactions.csv", index=False)
con = sqlite3.connect("data/retail.db")
df.to_sql("transactions", con, if_exists="replace", index=False)
con.close()
pd.Series(log).to_csv("data/cleaning_log.csv")
print(log)
