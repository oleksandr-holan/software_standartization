"""CryptoWallet variant 13 preset values."""

CRYPTOWALLET_PRESET = {
    "system": "CryptoWallet",
    "variant": 13,
    "lorenz": {
        "nm_base": 7,
        "noo": 3,
        "noa": 4,
        "nv": 1,
        "parent_class": "CryptoAsset",
        "child_class": "StableCoin",
    },
    "ck": {
        "class_name": "WalletSecurity",
        "wmc": 12,
        "dit": 2,
        "cbo": 5,
        "lcom": 0.10,
        "rfc": 18,
    },
    "mood_encap": {
        "m_tot": 160,
        "m_pub": 16,
        "a_tot": 95,
        "a_pub": 0,
    },
    "mood_inherit": {
        "m_tot": 220,
        "m_inh": 25,
        "a_tot": 100,
        "a_inh": 10,
    },
    "mood_flex": {
        "m_over": 40,
        "m_max_ov": 100,
        "c_act": 15,
        "c_max": 130,
    },
    "op": {
        "screens_s": 8,
        "screens_m": 4,
        "screens_h": 5,
        "reports_s": 4,
        "reports_m": 3,
        "reports_h": 4,
        "gl3": 12,
        "prod": 12,
        "reuse": 20,
    },
    "ucp": {
        "actors_s": 12,
        "actors_m": 5,
        "actors_h": 3,
        "uc_s": 8,
        "uc_m": 4,
        "uc_h": 5,
        "tcf": 1.25,
        "ecf": 0.80,
        "hours_per_ucp": 20,
        "rate": 35,
    },
    "pert": {
        "o": 65,
        "m": 90,
        "p": 160,
    },
}

LR5_DEMO_CODE = """def process_bulk_orders(items_list, base_tax, loyalty_years, region):
    # Metadata for logging (Trash - T)
    internal_batch_id = "LOG_2026_V1"

    total_sum = 0.0  # Modified (M)
    processed_count = 0

    for item in items_list:
        price = item['price']  # Input (P)
        qty = item['qty']

        if qty > 100:
            if price > 500:
                discount = 0.20  # Control (C)
            else:
                discount = 0.10
        else:
            discount = 0.05

        total_sum += (price * qty) * (1 - discount)
        processed_count += 1

    bonus_multiplier = 1.0
    counter = loyalty_years
    while counter > 0:
        bonus_multiplier += 0.02
        counter -= 1
        if bonus_multiplier >= 1.5:
            break

    if region == "EU":
        final_price = total_sum * base_tax
    elif region == "US":
        final_price = total_sum + 50.0
    else:
        final_price = total_sum

    return final_price * bonus_multiplier
"""
