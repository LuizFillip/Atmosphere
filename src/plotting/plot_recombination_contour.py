from settings import axes_hour_format, secondary_axis, axes_date_format
import matplotlib.pyplot as plt
import settings as s
import numpy as np
from labels import Labels
from utils import translate
import pandas as pd

def load(infile, hemisphere = "north"):

    df = pd.read_csv(infile, index_col = 0)
    
    df["dn"] = pd.to_datetime(df["dn"])
        
    df = df.loc[(df.index <= 500) & 
                (df["hem"] == hemisphere)]
    
    return pd.pivot_table(
        df, 
        values = "RT", 
        columns= "dn", 
        index = df.index
        )

def plot_recombination_contour(ax, ds, hem):
    
    vls = ds.values

    vmin, vmax = np.min(vls), np.max(vls)
    
    img = ax.contourf(
        ds.columns, 
        ds.index, 
        ds.values, 30, 
        cmap = "rainbow"
        )
    
    ticks = np.linspace(round(vmin), round(vmax, 2), 5)
    
    lbs  = Labels().infos["RT"]
    
    s.colorbar_setting(
            img, ax, ticks, 
            label = f"{lbs['symbol']} ({lbs['units']})", 
            bbox_to_anchor = (.54, 0., 1, 1), 
            ) 
    
    name = lbs["name"].replace("\n", " ")
    
    ax.set(ylabel = "Altura de Apex (km)", 
           title = f"{name} - ({translate(hem)})")
    
    
def plot_alttime_recombination(infile):
    fig, ax = plt.subplots(
        dpi = 300,
        nrows = 2,
        figsize = (10, 6),
        sharex = True
        )
    
    for row, hem in enumerate(["north", "south"]):
        ds = load(infile, hemisphere = hem)
        plot_recombination_contour(ax[row], ds, hem)
        
        
    axes_hour_format(ax[1], hour_locator = 8, tz = "UTC")
    
    ax1 = secondary_axis(ax[1])
    ax1.set(xlabel = "Hora universal")
    axes_date_format(ax1, day_locator = 1, tz = "UTC")
    
    return fig


infile = "database/RayleighTaylor/process/01.txt"
