'''
Author: ashokkasthuri ashokk@smu.edu.sg
Date: 2025-02-11 16:23:21
LastEditors: ashokkasthuri ashokk@smu.edu.sg
LastEditTime: 2025-02-11 16:39:03
FilePath: /ethutils/ERCclassification.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
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
    # Convert bytecode to lowercase to ensure case-insensitive search.
    bc = bytecode.lower()
    for sel in selectors:
        # Also lower-case the selector (they are stored without "0x")
        if sel.lower() not in bc:
            return False
    return True

def main():
    # Load the ERC configuration JSON.
    with open("erc_config.json", "r") as f:
        erc_config = json.load(f)
    
    # Read the CSV file (only the first 100 rows)
    df = pd.read_csv("/Users/ashokk/Documents/bytecodeContracts.csv")
    df_subset = df.head(10)
    
    # For each row (contract), check against every ERC type.
    matched_erc_types = []
    for idx, row in df_subset.iterrows():
        bytecode = row["bytecode"]
        current_matches = []
        for erc_type, config in erc_config.items():
            # Get the list of selectors from the configuration.
            selectors = config.get("selectors", [])
            # If all selectors are found in the bytecode, consider it a match.
            if match_erc_type(bytecode, selectors):
                current_matches.append(erc_type)
        matched_erc_types.append(current_matches)
    
    # Use .loc to assign new columns
    df_subset.loc[:, "matched_erc"] = matched_erc_types
    df_subset.loc[:, "bytecode_short"] = df_subset["bytecode"].str[:10]
    
    # Print the results (contract bytecode and matched ERC types)
    print(df_subset[["bytecode_short", "matched_erc"]])
    
    # Optionally, save the results to a CSV file.
    # df_subset.to_csv("erc_classification_results.csv", index=False)

if __name__ == "__main__":
    main()
