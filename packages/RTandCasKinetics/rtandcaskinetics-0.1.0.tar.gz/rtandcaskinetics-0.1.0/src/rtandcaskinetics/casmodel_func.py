import numpy as np
import tellurium as te
import matplotlib.pyplot as plt
from probability_func import calculate_dNTP_probability

def compute_fluorescence(forwardDNA, TemplateConc_nM, PrimerConc_nM, dNTPConc_nM, Kaff):
    """
    Computes the fluorescence kinetics based on the input parameters.

    Parameters:
        forwardDNA (str): The DNA sequence to be simulated.
        TemplateConc_nM (float): Template concentration in nanomolar.
        PrimerConc_nM (float): Primer concentration in nanomolar.
        dNTPConc_nM (float): dNTP concentration in nanomolar.
        Kaff (float): Affinity constant for the drug.

    Returns:
        List of (time_mins, fluorescence) for each NRTI concentration.
    """
    # Validate inputs
    if TemplateConc_nM < 0 or PrimerConc_nM < 0 or dNTPConc_nM < 0 or Kaff < 0:
        raise ValueError("Concentrations must be non-negative.")
    if not all(base in "ATCG" for base in forwardDNA.upper()):
        raise ValueError("DNA sequence contains invalid characters.")
    
    # Input conversions
    DNAstrand = forwardDNA[::-1]  # Reverse the DNA sequence
    casregionforward = 'ATGATGTGAAGGTGTTGTCG'
    casregion = casregionforward[::-1]
    PrimerConc = PrimerConc_nM * 1e-9  # Primer concentration (M)
    dNTP_Conc = dNTPConc_nM * 1e-9  # dNTP concentration (M)
    TemplateConc = TemplateConc_nM * 1e-9  # Template concentration (M)

    # Constants
    TemplateCopies = TemplateConc * 6.022e23 * 1000  # copies in 1uL reaction
    NRTI_Conc = np.logspace(-10, -5, 6)  # varying NRTI concentrations
    nucleotide_addition_rate = 5  # Basepairs per second
    kcat = 0.55  # Turnover number (1/s)
    Km = 663e-9  # Michaelis constant (M)
    E = 5e-9  # Enzyme concentration (M)
    time_total = 7200  # Total simulation time (seconds) corresponds to 120 minutes
    k_diff = 1e5  # Diffusion-limited rate constant (M^-1 s^-1)

    # Estimate primer binding time
    t_bind = 1 / (k_diff * PrimerConc) if PrimerConc > 0 else float('inf')
   
    results = []

    # Iterate over NRTI concentrations
    for nrti_conc in NRTI_Conc:
        cumulative_time = t_bind
        cumulative_probability = 1.0
        reached_casregion = False
        nucleotides_added = 23  # Start synthesis at the 24th nucleotide

        while cumulative_time <= time_total and not reached_casregion:
            if nucleotides_added < len(DNAstrand):
                # Calculate probability for nucleotide addition
                prob = calculate_dNTP_probability(
                    base=DNAstrand[nucleotides_added],
                    dNTP_Conc=dNTP_Conc,
                    NRTI_Conc=nrti_conc,
                    Kaff=Kaff,
                )
                prob = max(prob, 1e-6)  # Prevent division by zero or unrealistic values
                cumulative_probability *= prob

                # Calculate nucleotide addition time delay
                nucleotide_delay = (1 / nucleotide_addition_rate) / prob
                cumulative_time += nucleotide_delay

                # Check if Cas region is reached
                if DNAstrand[nucleotides_added:nucleotides_added + len(casregion)] == casregion:
                    reached_casregion = True

                nucleotides_added += 1
            else:
                break  # No more nucleotides to process

        # Simulate Michaelis-Menten fluorescence
        if reached_casregion:
            scaled_kcat = kcat * cumulative_probability  # Scale by probability
            model = f"""
            model MichaelisMentenFluorescence
                kcat = {scaled_kcat};
                Km = {Km};
                E = {E};
                S = 5e-9;
                P = 0.0;

                v: S -> P; (kcat * E * S) / (Km + S);

                S = 5e-9;
                P = 0.0;
            end
            """
            rr = te.loadAntimonyModel(model)
            result = rr.simulate(0, time_total - cumulative_time, 1000)

            time = result[:, 0] + cumulative_time  # Adjust time offset
            fluorescence = result[:, 2]  # Product concentration (fluorescence)
            fluorescence *= TemplateCopies  # Scale for template copies
        else:
            # Generate flat zero fluorescence curve
            time = np.linspace(0, time_total, 1000)
            fluorescence = np.zeros_like(time)

        time_mins = time / 60  # Convert to minutes
        results.append((time_mins, fluorescence))
        #plt.plot(time_mins, fluorescence, label=f"NRTI_Conc = {nrti_conc:.1e}")
    return results

def plot_fluorescence(results):
    """
    Generate a fluorescence plot using the computed results.

    Parameters:
        results (list): List of (time_mins, fluorescence) for each NRTI concentration.
    """
    plt.figure(figsize=(10, 6))
    for time_mins, fluorescence in results:
        plt.plot(time_mins, fluorescence, label=f"NRTI_Conc")

    plt.title("Combined Kinetics of RT Incorporation and Cas12a Cleavage")
    plt.xlabel("Time (minutes)")
    plt.ylabel("Fluorescence (RFU)")
    plt.xlim(0, 120)
    plt.legend()
    plt.grid(True)
    plt.show()