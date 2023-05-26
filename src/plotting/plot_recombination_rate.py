from models import altrange_msis
import matplotlib.pyplot as plt
import settings as s
import datetime as dt
from GEO import sites
import atmosphere as atm

dn = dt.datetime(2013, 1, 1)
lat, lon = sites["saa"]["coords"]

ds = altrange_msis(dn, glat = lat, glon = lon)



fig, ax = plt.subplots()

r = atm.recombination_rate(ds["O2"], ds["N2"])

ax.plot(r, r.index)

r1 = atm.recombination2(ds["O2"], ds["N2"])

ax.plot(r1, r.index)

import pandas as pd
import FluxTube as ft

infile = "database/RayleighTaylor/process/01.txt"
df = pd.read_csv(infile, index_col = 0)
dates = df["dn"].unique()

hem = "north"

df = df.loc[(df["dn"] == dates[0]) & 
            (df["hem"] ==  hem)]




infile = "D:\\FluxTube\\01\\201301010000.txt"

ds = ft.IntegratedParameters(infile)



def plot_recombination_profiles(ds, df):
    fig, ax = plt.subplots(dpi = 300)
    
    ax.plot(df["RT"], df.index, label = "Carrasco")
    
    ax.set(xscale = "log")
    
    ds = ds.loc[ds["hem"] == "north"]
    
    ax.plot(ds["R"], ds.index, label = "Sekar")
    
    ax.legend()
