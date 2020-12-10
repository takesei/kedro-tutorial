import pandas as pd


def is_true(ary: pd.Series) -> pd.Series:
    assert ary.dtype == "object"
    return ary == "t"


def percent2float(ary: pd.Series) -> pd.Series:
    assert ary.dtype == "object"
    return ary.str.replace("%", "").astype(float) / 100


def money2float(ary: pd.Series) -> pd.Series:
    assert ary.dtype == "object"
    temp = ary.str.replace("$", "")
    temp = temp.str.replace(",", "")
    return temp.astype(float) / 100


def preprocess_companies(companies: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocess the data for companies

    Args:
        companies: Source data
    Returns:
        PreProcess data
    """

    temp = is_true(companies["iata_approved"])
    companies["iata_approved"] = temp

    temp = percent2float(companies["company_rating"])
    companies["company_rating"] = temp

    return companies


def preprocess_shuttles(shuttles: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocess the data for shuttles

    Args:
        shuttles: Source data
    Returns:
        Preprocessed data
    """
    temp = is_true(shuttles["d_check_complete"])
    shuttles["d_check_complete"] = temp

    temp = is_true(shuttles["moon_clearance_complete"])
    shuttles["moon_clearance_complete"] = temp

    temp = money2float(shuttles["price"])
    shuttles["price"] = temp

    return shuttles


def create_master_table(
        shuttles: pd.DataFrame, companies: pd.DataFrame, reviews: pd.DataFrame
) -> pd.DataFrame:
    """
    Combines All data to create master table

    Args:
        shuttles: Preprocessed data for shuttles
        companies: Preprocessed data for companies
        reviews: Source data for shuttles
    Returns:
        Master table
    """
    rated_shuttles = shuttles.merge(
        reviews, left_on="id", right_on="shuttle_id"
    )

    with_companies = rated_shuttles.merge(
        companies, left_on="id", right_on="company_id"
    )

    master_table = with_companies.drop(["shuttle_id", "company_id"], axis=1)
    return master_table.dropna()
