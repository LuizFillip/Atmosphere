import numpy as np 
from GEO import year_fraction
import pyIGRF

class effective_wind(object):
    
    """
    Effective wind along and perpendicular of 
    magnetic field
    
    Pag. 27 e 28 (Tese Ely, 2016)
    
    U_theta (mer) = meridional component (positiva para sul)
    U_phi (zon) = zonal component (positiva para leste)
    
    """
    
    @staticmethod
    def zonal(zon, mer, D): 
        D = np.deg2rad(D)
        # Ueff_y (positiva para leste)
        return (zon * np.cos(D) + mer * np.sin(D))
    
    @staticmethod
    def meridional(zon, mer, D, I):
        D = np.deg2rad(D)
        I = np.deg2rad(I)
        # Ueff_x (positiva para sul)
        return (
            mer * np.cos(D) + zon * np.sin(D)
                ) * np.cos(I)


def effective_wind_on_FT(df, dn):

    dec = []
    inc = []
    
    for lat, lon, alt in zip(df.glat, df.glon, df.alt):
        d, i, h, x, y, z, f = pyIGRF.igrf_value(
            lat, 
            lon, 
            alt = alt, 
            year = year_fraction(dn)
            )
        
        dec.append(d)
        inc.append(i)
        
    df["d"] = dec
    df["i"] = inc
    
    wind = effective_wind()
    
    df["zon_ef"] = wind.zonal(df["U"], df["V"], df["d"])
    df["mer_ef"] = wind.meridional(df["U"], df["V"], 
                                   df["d"], df["i"])
    
    return df