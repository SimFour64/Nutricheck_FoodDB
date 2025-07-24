import pandas as pd
from pathlib import Path
from .database import create_db
from ..config import DATABASE_PATH, RESULTS_PATH, TOP_N_FOODS



def get_compound_names():
    """
    Takes user input for a list of compound that will be used to retrieve food
    with most concentration

    Args:
        None

    Returns:
        compound_input (list of str): list of compounds
    """
    while True:
        try:
            compound_input = input("Enter compounds (comma separated):")
            compounds = [c.strip().capitalize() for c in compound_input.split(",")]
            if compounds and compounds != [""]:
                return compounds
            print("❌ Please enter at least one compound")
        except KeyboardInterrupt:
            print("👋 Bye bye")
            exit()



def filter_compounds(ranked_compounds, compound_input):
    """
    Filter only on compounds of interest listed by user input. Validation of
    compounds entered by the user

    Args:
        - ranked_compounds (pd.DataFrame): ranked compounds by food
        - compound_input (list): list of user input compournds to filter on

    Returns:
        - filtered_compounds (pd.DataFrame): filtered dataframe
    """
    available_compounds = ranked_compounds["compound_name"].unique()
    missing_compounds = [c for c in compound_input if c not in available_compounds]

    if missing_compounds:
        print(f"⚠️ Warning - Compounds not found: {','.join(missing_compounds)}")
        print(f"Available compounds: {','.join(available_compounds)}")

    filtered_compounds = ranked_compounds[ranked_compounds["compound_name"].isin(compound_input)]

    if filtered_compounds.empty:
        raise ValueError("No data found for entered compounds")

    return filtered_compounds

def get_top_compounds(filtered_compounds, top_n = TOP_N_FOODS):
    """
    Retrieve only the top top_n foods with highest concentration of compound

    Args:
        - filtered_compounds (pd.DataFrame): ranked and filtered dataframe
        - top_n (int): number of top foods to be retrieved for each compound)

    Returns:
        - output_df (pd.DataFrame): top_n rows of input dataframe based on
        food rank
    """
    output_df = filtered_compounds[filtered_compounds["food_rank"] <= top_n]
    return output_df


def get_ranked_foods():
    # Getting list of compounds to analyse
    compound_input = get_compound_names()

    # Checking if the database exists, create one if not
    database_path = Path(DATABASE_PATH / "ranked_compounds.csv")
    if not database_path.exists():
        print("🟠 Database does not exist!")
        create_db()
    # Getting database with ranked compounds
    ranked_compounds = pd.read_csv(database_path)

    print(f"🔍 Searching for: {', '.join(compound_input)}")

    # Filtering on compounds of interest only
    filtered_compounds = filter_compounds(ranked_compounds, compound_input)

    # Getting top foods
    output_df = get_top_compounds(filtered_compounds)

    # Saving output df
    compound_names = "-".join(compound_input)
    file_name = f"compound_food_source_report_{compound_names}_top_{TOP_N_FOODS}.csv"
    RESULTS_PATH.mkdir(parents=True, exist_ok=True)
    output_df.to_csv(RESULTS_PATH / file_name, index=False)

    print("🚀 Food list saved!")


if __name__ == "__main__":
    get_ranked_foods()
