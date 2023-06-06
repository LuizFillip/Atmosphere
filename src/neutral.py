import numpy as np

def recombination_rate(O2, N2):
    """Recombination chemistry rate coefficient"""
    return (4.0e-11 * O2) + (1.3e-12 * N2)    
    



def recombination2(O2, N2):
    """See Sekar and Raghavarao 1987 """
    return (5.15e-13 * N2) + (1.2e-11 * O2) 


def con_from_point(
        tn, 
        o_point, 
        o2_point, 
        n2_point, 
        step,  
        base_height = 200.0 
        ):
    
    """
    Get concetrantions profiles from neutral constituints 
    from point
    """

    CO = np.zeros(len(tn))
    CO2 = np.zeros(len(tn))                
    CN2 = np.zeros(len(tn))                

    
    for i in range(0, len(tn)):
        
        Z1 = base_height + step * i
        
        GR = 1.0 / pow(1.0 + Z1 / 6370.0, 2)
        
        HO = 0.0528 * tn[i] / GR                               # scale height of O [km]
        HO2 = 0.0264 * tn[i] / GR                              # scale height of O2 [km]
        HN2 = 0.0302 * tn[i] / GR                              # scale height of N2 [km]

        p_co = o_point / 5.33 * 8.55
        p_co2 = o2_point / 1.67 * 4.44
        p_cn2 = n2_point / 9.67 * 2.26

        CO[i] = p_co * np.exp(-(Z1 - 335.0) / HO)           # atomic oxygen [cm-3]
        CO2[i] = p_co2 * np.exp(-(Z1 - 335.0) / HO2)        # molecular oxygen [cm-3]
        CN2[i] = p_cn2 * np.exp(-(Z1 - 335.0) / HN2) 
    
    return CO, CO2, CN2