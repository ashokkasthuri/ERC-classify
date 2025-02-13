import pandas as pd
import json

def match_erc_type(bytecode, selectors):
    """
    Check if all selectors in the list appear in the bytecode.
    
    Args:
        bytecode (str): The contract's bytecode.
        selectors (list): A list of selector strings.
    
    Returns:
        bool: True if every selector is found in the bytecode.
    """
    bc = bytecode.lower()
    for sel in selectors:
        if sel.lower() not in bc:
            return False
    return True

def main():
    # Load the ERC configuration JSON.
    with open("erc_config.json", "r") as f:
        erc_config = json.load(f)
    
    # List of common ERC types that we do not want to check
    common_types = ["ERC20", "ERC721", "ERC1155", "ERC165", "ERC173", "ERC2981", "ERC3754","ERC4494", "ERC1363","ERC777", "ERC1046", "ERC223", "ERC884", "ERC4524", "ERC2021", "ERC1996", "ERC3643", "ERC4910", "ERC4955", "ERC5192", "ERC4400", "ERC5615", "ERC4906", "ERC4626"  ]
    
    # Read the CSV file (only the first 100 rows)
    # df = pd.read_csv("/Users/ashokk/Documents/bytecodeContracts.csv")
    df = pd.read_csv("/Users/ashokk/Downloads/deduplicated_results.csv")
    
    df_subset = df.head(100000).copy()  # using 100 rows
    
    matched_erc_types = []
    for idx, row in df_subset.iterrows():
        bytecode = row["bytecode"]
        current_matches = []
        for erc_type, config in erc_config.items():
            # Skip common ERC types
            if erc_type in common_types:
                continue
            selectors = config.get("selectors", [])
            if match_erc_type(bytecode, selectors):
                current_matches.append(erc_type)
        matched_erc_types.append(current_matches)
    
    df_subset.loc[:, "matched_erc"] = matched_erc_types
    df_subset.loc[:, "bytecode_short"] = df_subset["bytecode"].str[:40]
    
    # Filter the DataFrame to only include rows where "matched_erc" is non-empty.
    filtered_df = df_subset[df_subset["matched_erc"].apply(lambda x: len(x) > 0)]
    
    # Print only the first 10 characters of bytecode and matched ERC types for the filtered rows.
    print(filtered_df[["address","bytecode_short", "matched_erc"]])
    
    # Optionally, save the results to a CSV file.
    filtered_df.to_csv("erc_classification_results.csv", index=False)

if __name__ == "__main__":
    main()
