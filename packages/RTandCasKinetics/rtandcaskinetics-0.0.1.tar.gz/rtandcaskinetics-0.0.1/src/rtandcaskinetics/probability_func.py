def calculate_dNTP_probability(base, dNTP_Conc, NRTI_Conc, Kaff):
    """
    Calculate the probability P_dNTP of incorporating a single dNTP.

    Parameters:
    - base (str): The nucleotide base ('A', 'T', 'C', 'G')
    - dNTP_Conc (float): Uniform concentration of dNTP
    - NRTI_Conc (float): Concentration of NRTI (only affects T)
    - Kaff (float): Affinity factor of NRTI

    Returns:
    - Probability P_dNTP
    """
    valid_bases = {'A', 'T', 'C', 'G'}
    if base not in valid_bases:
        raise ValueError(f"Invalid base '{base}'. Valid options are {valid_bases}.")
    
    # Adjust fraction if the base is T
    if base == "T":
        fraction = dNTP_Conc / (dNTP_Conc + Kaff * NRTI_Conc)
    else:
        fraction = 1.0  # No competition for non-T bases
    return fraction
