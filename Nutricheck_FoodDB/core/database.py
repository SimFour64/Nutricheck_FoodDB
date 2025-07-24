import pandas as pd
from ..config import DATA_RAW_PATH, DATABASE_PATH


def load_data():
    """
    Load all csv files required to create database

    Args:
        None

    Returns:
        foods, compounds, contents (tuple of 3 pd.DataFrame)
    """
    try:
        foods = pd.read_csv(DATA_RAW_PATH / "foods.csv")
        compounds = pd.read_csv(DATA_RAW_PATH / "compounds.csv")
        contents = pd.read_csv(DATA_RAW_PATH / "contents.csv")
        return foods, compounds, contents
    except FileNotFoundError as e:
        print(f"Error: file not found - {e}")
        raise

def filter_compound_only(contents):
    """
    Filter the content dataframe on "source_type" column to keep only "Compound" rows

    Args:
        contents (pd.DataFrame): DataFrame with 'source_type' row

    Returns:
        contents_with_compounds (pd.DataFrame): filtered dataframe
    """
    contents_with_compounds = contents[contents["source_type"]=="Compound"]
    if contents_with_compounds.empty:
        raise ValueError("No compound found after filtering")
    return contents_with_compounds


def merge_tables(foods, compounds, contents_with_compounds):
    """
    Merge three pd.DataFrame based on following keys:
        - foods dataframe -> key = "id"
        - compounds dataframe -> key = "id"
        - contents_with_compounds -> key = "source_id"

    Args:
        foods, compounds, contents_with_compounds (pd.DataFrame): DataFrames with necessary ID rows

    Returns:
        merged_tables (pd.DataFrame): merged dataframe
    """
    contents_and_compounds = contents_with_compounds.merge(compounds, how="inner", left_on="source_id", right_on="id")
    merged_tables = contents_and_compounds.merge(foods, how="inner", left_on="food_id", right_on="id",suffixes=("_compounds","_foods"))
    return merged_tables

def rank_food(merged_tables):
    """
    Rank dataframe in descending order based on the compound's concentration

    Args:
        merged_tables (pd.DataFrame): DataFrame with "orig_content" row

    Returns:
        ranked_compounds (pd.DataFrame): ranked dataframe
    """
    ranked_compounds = merged_tables.sort_values(by=["name_compounds","orig_content"], ascending=[True,False])
    ranked_compounds["food_rank"] = ranked_compounds.groupby("name_compounds")["orig_content"].rank(ascending=False)
    return ranked_compounds

def format_output(ranked_compounds):
    """
    Format dataframe in expected shape, column names :
        - compound_names
        - food_rank
        - food_name
        - concentration

    Args:
        ranked_compounds (pd.DataFrame): DataFrame

    Returns:
        output_df (pd.DataFrame): formatted dataframe
    """
    output_df = ranked_compounds[["name_compounds","food_rank","name_foods","orig_content"]]
    output_df = output_df.rename(columns={
        "name_compounds": "compound_name",
        "name_foods": "food_name",
        "orig_content": "concentration"
    })
    output_df = output_df.reset_index(drop=True)
    return output_df



def create_db():
    """
    Creates and saves database by merging 3 source csv files (foods, compounds,
    contents) and ranking compounds according the their highest concentrations
    in resepective foods.

    Args:
        None

    Returns:
        None, save databse under "data/database/ranked_compounds.csv"

    """

    print("⏳ Creating database...")

    # Load raw data from csv files
    foods, compounds, contents = load_data()

    # Filtering only contents with "Compound" type
    contents_with_compounds = filter_compound_only(contents)

    # Merge different files
    merged_tables = merge_tables(foods, compounds, contents_with_compounds)

    # Rank food for each compound
    ranked_compounds = rank_food(merged_tables)

    # Format the ouput dataframe
    output_df = format_output(ranked_compounds)

    # Saving
    DATABASE_PATH.mkdir(parents=True, exist_ok=True)
    output_df.to_csv(DATABASE_PATH / "ranked_compounds.csv", index=False)

    print("📂 Database created!")


if __name__ == "__main__":
    create_db()
