import os

import requests
import json
import time
import pandas as pd

# Replace with your actual Etherscan API key.
API_KEY = "Z8IMKB1ZVRIER3Q6U66MJPAKFY1V68IT87"

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

def fetch_source_code(address: str) -> dict:
    """
    Fetch the verified source code for a contract address from Etherscan.
    """
    url = (
        f"https://api.etherscan.io/api?module=contract&action=getsourcecode"
        f"&address={address}&apikey={API_KEY}"
    )
    response = requests.get(url)
    try:
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def fetch_tx_activity(address: str) -> dict:
    """
    Fetch the transaction activity for a contract address from Etherscan.
    """
    url = (
        f"https://api.etherscan.io/api?module=account&action=txlist"
        f"&address={address}&startblock=0&endblock=99999999&sort=asc&apikey={API_KEY}"
    )
    response = requests.get(url)
    try:
        return response.json()
    except Exception as e:
        return {"error": str(e)}
def save_source_code(address: str, source_info: dict) -> None:
    """
    Save the contract source code into a file named <address>.sol in the "contracts" folder.
    The source code is extracted from the 'SourceCode' field in the result.
    """
    result = source_info.get("result")
    if not result or len(result) == 0:
        print(f"No source code data found for {address}")
        return

    # The result is a list of dictionaries.
    source_code = result[0].get("SourceCode")
    if not source_code:
        print(f"No source code available for {address}")
        return

    # Create the output directory if it doesn't exist.
    os.makedirs("contracts", exist_ok=True)
    filename = f"contracts/{address}.sol"

    # To avoid overriding an existing file, if file exists, append a counter.
    base_filename = filename[:-4]
    counter = 1
    while os.path.exists(filename):
        filename = f"{base_filename}_{counter}.sol"
        counter += 1

    with open(filename, "w", encoding="utf-8") as f:
        f.write(source_code)
    print(f"Saved source code for {address} to {filename}")
    
def should_fetch_contract(tx_list) -> bool:
    """
    Return True if the total number of transactions is > 100 and
    at least one transaction happened in the last 30 days.
    """
    if not tx_list:
        return False
    total_tx = len(tx_list)
    if total_tx <= 100:
        return False

    # Current time in seconds
    now = int(time.time())
    # 30 days in seconds
    thirty_days = 30 * 24 * 3600
    recent = any(int(tx["timeStamp"]) >= (now - thirty_days) for tx in tx_list)
    return recent

def ERC_classification():
     # Load the ERC configuration JSON.
    with open("test_erc_config.json", "r") as f:
        erc_config = json.load(f)
    
    # List of common ERC types that we do not want to check
    common_types = ["ERC20", "ERC721", "ERC1155", "ERC165", "ERC173", "ERC2981", "ERC3754","ERC4494", "ERC1363","ERC777", "ERC1046", "ERC223", "ERC884", "ERC4524", "ERC2021", "ERC1996", "ERC3643", "ERC4910", "ERC4955", "ERC5192", "ERC4400", "ERC5615", "ERC4906", "ERC4626"  ]
    # common_types = ["ERC20", "ERC721", "ERC1155"]
    # Read the CSV file (only the first 100 rows)
    # df = pd.read_csv("/Users/ashokk/Documents/bytecodeContracts.csv")
    df = pd.read_csv("/Users/ashokk/Downloads/deduplicated_results.csv")
    
    df_subset = df.head(10000).copy()  # using 100 rows
    
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
    filtered_df.to_csv("test1_erc_classification_results.csv", index=False)
   
def verify_source():
    df = pd.read_csv("test1_erc_classification_results.csv")
    df_subset = df.head(20).copy()  # using 100 rows
    
    
    # Extract unique addresses.
    addresses = df_subset["address"].dropna().unique()
    
    for address in addresses:
        print(f"\nProcessing contract: {address}")
        
        # Get transaction activity.
        tx_info = fetch_tx_activity(address)
        if tx_info.get("status") != "1":
            print(f"Error fetching tx activity for {address}: {tx_info.get('message', tx_info)}")
            continue
        
        tx_list = tx_info.get("result", [])
        if not should_fetch_contract(tx_list):
            print(f"Skipping {address}: does not meet tx activity criteria")
            continue

        # Fetch the verified source code.
        source_info = fetch_source_code(address)
        if source_info.get("status") == "1":
            save_source_code(address, source_info)
        else:
            print(f"Error fetching source code for {address}: {source_info.get('message', source_info)}")

    
   

def main():
    # ERC_classification()
    verify_source()
    

if __name__ == "__main__":
    main()
