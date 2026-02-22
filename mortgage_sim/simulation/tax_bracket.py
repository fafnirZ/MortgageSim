
def get_taxed_amount_fy_25_26(gross_income: float) -> float:
    if 0 < gross_income <= 18_200:
        return 0
    elif 18_201 <= gross_income <= 45_000:
        return gross_income * 0.16
    elif 45_001 <= gross_income <= 135_000:
        return 4_288 + 0.30*(gross_income-45_000)
    elif 135_001 <= gross_income <= 190_000:
        return 31_288 + 0.37*(gross_income-135_000)
    elif 190_001 <= gross_income:
        return 51_638 + 0.45*(gross_income-190_000)
    else:
        raise RuntimeError(f"{gross_income} not in any ranges")


def get_medicare_amount(gross_income: float)->float: 
    return gross_income*0.02