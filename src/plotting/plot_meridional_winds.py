import matplotlib.pyplot as plt
import pandas as pd
import settings as s
import datetime as dt


def set_data(hem = 'south'):
    infile = 'wind_perp.txt'
    
    df = pd.read_csv(infile, index_col=0)
    
    
    df = df.loc[(df.index ==  300) & 
                (df['hem']== hem)]
    
    df = df.set_index('dn')


    df.index = pd.to_datetime(df.index)
    
    return df


def set_data_2(hem):
    infile = 'database/RayleighTaylor/reduced/300.txt'
    
    ds = pd.read_csv(infile, index_col = 0)
    
    ds.index = pd.to_datetime(ds.index)
    
    ds = ds.loc[(ds.index >= dt.datetime(2013, 3, 16)) &
                (ds.index < dt.datetime(2013, 3, 20)) & 
                (ds['hem'] == hem)]
    
    return ds


    
def sum_hems():
    perp = pd.concat(
        [set_data('south')['mer_ef'], 
         set_data('north')['mer_ef']], 
        axis = 1
        ).sum(axis = 1)
    
    
    paralel = pd.concat(
        [set_data_2('south')['mer_ef'], 
         set_data_2('north')['mer_ef']], 
        axis = 1
        ).sum(axis = 1)
    
    return pd.concat([perp, paralel], axis = 1)

def plot_meridional_winds():

    s.config_labels()
    
    fig, ax = plt.subplots(
        figsize = (10, 8), 
        nrows = 3, 
        dpi = 300,
        sharey = True, 
        sharex = True
        )
    
    plt.subplots_adjust(hspace = 0.1)
    hems = ['south', 'north']
    
    
    for i, hem in enumerate(hems):
        
        df = set_data(hem)
        ds = set_data_2(hem)
        ax[i].plot(df['mer_ef'], label = "Perpendicular a B")
        ax[i].plot(ds['mer_ef'], label = 'Paralelo a B')
        
        
        ax[i].set( 
                  ylim = [-70, 70], 
                  xlim = [df.index[0], df.index[-1]]
                  )
        
    ax[2].plot(sum_hems(), 
               label = ["Perpendicular a B", 
                        'Paralelo a B'])
    ax[0].legend( 
        bbox_to_anchor = (0.5, 1.3), 
        ncol = 2, 
        loc = 'upper center'
        )
    
    
    s.format_time_axes(ax[2])
    
    fig.text(0.06, 0.35, 
             'Velocidade meridional (m/s)', 
             rotation = 'vertical')
    
    names = ['Sul', 'Norte', 'Total']
    for i, ax in enumerate(ax.flat):
        ax.axhline(0, linestyle = '--')

        letter = s.chars()[i]
        ax.text(
            0.02, 0.85, f"({letter}) {names[i]}", 
            transform = ax.transAxes
            )
        
    return fig


fig = plot_meridional_winds()

# fig.savefig("atmosphere/figures/meridional_winds_integrated.png", dpi = 300)