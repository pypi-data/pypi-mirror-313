
def set_dpe_mappings():
    """
    Set mappings for DPE codes in France. DPE stands for 'Diagnostic de Performance Electrique'.

    Returns:
        dict: A dictionary with DPE codes as keys and corresponding energy consumptions for 1 m2 in kWh/year as values.
    """
    return {
    "A": "70",
    "B": "110",
    "C": "180",
    "D": "250",
    "E": "330",
    "F": "420"
    }
