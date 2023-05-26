
def recombination_rate(O2, N2):
    """Recombination chemistry rate coefficient"""
    return (4.0e-11 * O2) + (1.3e-12 * N2)    
    



def recombination2(O2, N2):
    """See Sekar and Raghavarao 1987 """
    return (5.15e-13 * N2) + (1.2e-11 * O2) 