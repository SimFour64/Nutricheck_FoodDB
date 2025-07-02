import pandas as pd


def get_compound_names():
    compound_input = input("Enter a comma-separated list of compounds you want to retrieve foods with most concentration (expected format : Sodium,Omega-3,Protein): ")
    return compound_input.split(",")

def load_data():
    foods = pd.read_csv("data/foods.csv")
    compounds = pd.read_csv("data/compounds.csv")
    contents = pd.read_csv("data/contents.csv")
    return foods, compounds, contents

def filter_compound_only(contents):
    return contents[contents["source_type"]=="Compound"]

def merge_tables(contents_with_compounds, compounds, foods):
    contents_and_compounds = contents_with_compounds.merge(compounds, how="inner", left_on="source_id", right_on="id")
    merged_tables = contents_and_compounds.merge(foods, how="inner", left_on="food_id", right_on="id",suffixes=("_compounds","_foods"))
    return merged_tables

def filter_compounds(merge_tables, compound_input):
    filtered_compounds = merge_tables[merge_tables["name_compounds"].isin(compound_input)]
    return filtered_compounds

def rank_food(filtered_compounds):
    ranked_compounds = filtered_compounds.sort_values(by=["name_compounds","orig_content"], ascending=[True,False])
    ranked_compounds["food_rank"] = ranked_compounds.groupby("name_compounds")["orig_content"].rank(ascending=False)
    return ranked_compounds

def format_output(ranked_compounds):
    output_df = ranked_compounds[["name_compounds","food_rank","name_foods","orig_content"]]
    output_df = output_df.rename(columns={
        "name_compounds": "compound_name",
        "name_foods": "food_name",
        "orig_content": "concentration"
    })
    output_df = output_df[output_df["food_rank"]<6]
    output_df = output_df.reset_index(drop=True)
    return output_df


def main():
    # Getting list of compounds to analyse
    compound_input = get_compound_names()
    print("🔁 Working")

    # Load required data
    foods, compounds, contents = load_data()

    # Filtering only contents with "Compound" type
    contents_with_compounds = filter_compound_only(contents)

    # Merging the three tables
    merged_tables = merge_tables(contents_with_compounds, compounds, foods)

    # Filtering on compounds of interest only
    filtered_compounds = filter_compounds(merged_tables, compound_input)

    # Rank food for each compound
    ranked_compounds = rank_food(filtered_compounds)

    # Format the ouput dataframe
    output_df = format_output(ranked_compounds)

    # Saving output df
    compound_names = "-".join(compound_input)
    output_df.to_csv(f"output_files/compound_food_source_report_{compound_names}.csv", index=False)
    print("🆗 File saved")



if __name__ == "__main__":
    main()
