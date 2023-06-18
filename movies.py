import pandas as pd
import sqlalchemy

engine = sqlalchemy.create_engine('sqlite:///new.db')
con = engine.raw_connection()
cursor = con.cursor()

data1 = pd.read_csv("./data/cleanup/ImdbName.csv")
data2 = pd.read_csv("./data/cleanup/ImdbTitleAkas.csv")
data3 = pd.read_csv("./data/cleanup/ImdbTitleBasics.csv")

