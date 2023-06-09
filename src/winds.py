import numpy as np 
from GEO import year_fraction, sites
import pyIGRF
import models as m


class effective_wind(object):
    
    """
    Effective wind along and perpendicular of 
    magnetic field
    
     (Tese Ely, 2016; Nogueira, 2013)

    U_theta (mer) = geographic meridional component (northward)
    U_phi (zon) = geographiczonal component (eastward)
    
    """
    
    @staticmethod
    def zonal(zon, mer, D): 
        D = np.deg2rad(D)
        # Ueff_y (positiva para leste)
        return (zon * np.cos(D) + mer * np.sin(D))
    
    @staticmethod
    def meridional_parl(zon, mer, D, I):
        """Componente paralela a B"""
        
        D = np.deg2rad(D)
        I = np.deg2rad(I)
        # Ueff_x (positiva para norte)
        return (
            mer * np.cos(D) + zon * np.sin(D)
                ) * np.cos(I)
    
    @staticmethod
    def meridional_perp(zon, mer, D, I):
        """Componente perpendicular a B"""
        D = np.deg2rad(D)
        I = np.deg2rad(I)
        # Ueff_x (positiva para norte)
        return (
            mer * np.cos(D) + zon * np.sin(D)
                ) * np.sin(I)



def fluxtube_eff_wind(df, dn):
    
    dec, inc, total = m.run_igrf(df, dn)
        
    df["d"] = dec
    df["i"] = inc
    df["F"] = total
    
    wind = effective_wind()
    
    df["zon_ef"] = wind.zonal(
                df["zon"], 
                df["mer"], 
                df["d"]
        )
    
    df["mer_perp"] = wind.meridional_perp(
        df["zon"], 
        df["mer"], 
        df["d"], 
        df["i"]
        )
    
    df["mer_parl"] = wind.meridional_parl(
        df["zon"], 
        df["mer"], 
        df["d"], 
        df["i"]
        )
    
    return df

def local_eff_wind(df, site = "saa"):
    lat, lon = sites[site]["coords"]
    dec = []
    inc = []
    
    for alt in df.alt:
        dn = df.index[0]
        d, i, _, _, _, _, f = pyIGRF.igrf_value(
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
    
    df["zon_ef"] = wind.zonal(
        df["zon"], df["mer"], df["d"]
        )
    df["mer_ef"] = wind.meridional_perp(
        df["zon"], df["mer"], 
        df["d"], df["i"]
        )
    
    return df