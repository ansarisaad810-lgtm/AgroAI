# DSA ALGORITHM: Multi-dimensional Lookup Array & Direct Mapping O(1)
# USED FOR: Soil N-P-K Fertilizer requirements calculation per acre.

NPK_RATES = {
    "wheat": {"n": 50, "p": 25, "k": 20, "urea": 110, "dap": 55},
    "rice": {"n": 40, "p": 20, "k": 20, "urea": 90, "dap": 45},
    "tomato": {"n": 60, "p": 30, "k": 30, "urea": 130, "dap": 65},
    "potato": {"n": 70, "p": 35, "k": 40, "urea": 150, "dap": 75},
}

def calculate_npk(crop_name, acres):
    """DSA: O(1) multi-variable array calculation."""
    crop_key = crop_name.lower()
    if crop_key in NPK_RATES:
        rates = NPK_RATES[crop_key]
        return {
            "urea_kg": round(rates["urea"] * acres, 1),
            "dap_kg": round(rates["dap"] * acres, 1),
            "n_element": round(rates["n"] * acres, 1),
            "p_element": round(rates["p"] * acres, 1),
            "k_element": round(rates["k"] * acres, 1)
        }
    return None
