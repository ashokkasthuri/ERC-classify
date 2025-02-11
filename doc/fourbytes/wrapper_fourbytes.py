'''
Author: ashokkasthuri ashokk@smu.edu.sg
Date: 2025-01-23 18:49:17
LastEditors: ashokkasthuri ashokk@smu.edu.sg
LastEditTime: 2025-01-26 13:30:18
FilePath: /ethutils/doc/fourbytes/wrapper_fourbytes.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
# import sys
# sys.path.append("../..")
# from ethutils import fourbytes

# def drop0x(hex):
#     return (None if hex is None else
#             hex[2:] if hex[0:2] == "0x" else
#             hex
#            )

# for line in sys.stdin:
#     row = line.rstrip('\n').split(';')
#     codeid = row[0]
#     if codeid == 'codeid':
#         print('codeid;signatures')
#         continue
#     address = row[1]
#     code = bytes.fromhex(drop0x(row[2]))
#     sigs = fourbytes.signatures(code)
#     sigsHex = [ s.hex() for s in sigs ]
#     print(f"{codeid};{sigsHex}")


# import sys
# sys.path.append("../..")
# from ethutils import fourbytes

# # Define the known selectors for ERC20 and ERC721
# ERC20_SELECTORS = {
#     "06fdde03",  # name()
#     "95d89b41",  # symbol()
#     "313ce567",  # decimals()
#     "70a08231",  # balanceOf(address)
#     "a9059cbb",  # transfer(address,uint256)
#     "dd62ed3e",  # allowance(address,address)
#     "095ea7b3",  # approve(address,uint256)
#     "23b872dd"   # transferFrom(address,address,uint256)
# }

# ERC721_SELECTORS = {
#     "70a08231",  # balanceOf(address)
#     "6352211e",  # ownerOf(uint256)
#     "095ea7b3",  # approve(address,uint256)
#     "081812fc",  # getApproved(uint256)
#     "a22cb465",  # setApprovalForAll(address,bool)
#     "e985e9c5",  # isApprovedForAll(address,address)
#     "42842e0e",  # safeTransferFrom(address,address,uint256)
#     "b88d4fde",  # safeTransferFrom(address,address,uint256,bytes)
#     "23b872dd"   # transferFrom(address,address,uint256)
# }

# def drop0x(hex):
#     return (None if hex is None else
#             hex[2:] if hex[0:2] == "0x" else
#             hex
#            )

# def determine_contract_type(signatures):
#     # Convert to set for easy comparison
#     sig_set = set(signatures)
#     is_erc20 = any(sig in ERC20_SELECTORS for sig in sig_set)
#     is_erc721 = any(sig in ERC721_SELECTORS for sig in sig_set)

#     if is_erc20 and is_erc721:
#         return "ERC20+ERC721"
#     elif is_erc20:
#         return "ERC20"
#     elif is_erc721:
#         return "ERC721"
#     else:
#         return "Unknown"

# # Process the input file line by line
# for line in sys.stdin:
    # row = line.rstrip('\n').split(';')
    # codeid = row[0]
    # if codeid == 'codeid':
    #     print('codeid;signatures;contract_type')
    #     continue
    # address = row[1]
    # code = bytes.fromhex(drop0x(row[2]))
    # sigs = fourbytes.signatures(code)
    # sigsHex = [s.hex() for s in sigs]
    # contract_type = determine_contract_type(sigsHex)
    # print(f"{codeid};{sigsHex};{contract_type}")



import sys
sys.path.append("../..")
from ethutils import fourbytes

# Define known selectors for various ERC standards with corresponding function signatures
ERC_SELECTORS = {
    "ERC20": {
        "06fdde03",  # name()
        "95d89b41",  # symbol()
        "313ce567",  # decimals()
        "70a08231",  # balanceOf(address)
        "a9059cbb",  # transfer(address,uint256)
        "dd62ed3e",  # allowance(address,address)
        "095ea7b3",  # approve(address,uint256)
        "23b872dd",  # transferFrom(address,address,uint256)
    },
    "ERC721": {
        "70a08231",  # balanceOf(address)
        "6352211e",  # ownerOf(uint256)
        "095ea7b3",  # approve(address,uint256)
        "081812fc",  # getApproved(uint256)
        "a22cb465",  # setApprovalForAll(address,bool)
        "e985e9c5",  # isApprovedForAll(address,address)
        "42842e0e",  # safeTransferFrom(address,address,uint256)
        "b88d4fde",  # safeTransferFrom(address,address,uint256,bytes)
        "23b872dd",  # transferFrom(address,address,uint256)
    },
    "ERC223": {
        "c0ee0b8a",  # transfer(address,uint256,bytes)
    },
    "ERC777": {
        "09d9ffb0",  # granularity()
        "46d52356",  # defaultOperators()
        # Includes ERC20 compatibility functions like transfer and approve
        "70a08231", "a9059cbb", "dd62ed3e",
    },
    "ERC1155": {
        "f242432a",  # safeTransferFrom(address,address,uint256,uint256,bytes)
        "2eb2c2d6",  # safeBatchTransferFrom(address,address,uint256[],uint256[],bytes)
        "d9b67a26",  # balanceOf(address,uint256)
        "00fdd58e",  # balanceOfBatch(address[],uint256[])
        "4e1273f4",  # isApprovedForAll(address,address)
    },
    "ERC1046": {
        "c87b56dd",  # tokenURI(uint256)
    },
    "ERC1363": {
        "4bbee2df",  # transferAndCall(address,uint256,bytes)
    },
    "ERC2309": {
        "18160ddd",  # ConsecutiveTransfer event
    },
    "ERC2612": {
        "f73aa3c0",  # permit(address,address,uint256,uint256,uint8,bytes32,bytes32)
    },
    "ERC2981": {
        "2a55205a",  # royaltyInfo(uint256,uint256)
    },
    "ERC3525": {
        "c82a4dd0",  # slotOf(uint256)
        # Includes ERC20 compatibility functions
        "70a08231", "a9059cbb", "dd62ed3e",
    },
    # Placeholder for additional standards:
    "ERC3643": set(),  # Provide function signatures if available
    "ERC4400": set(),  # Provide function signatures if available
    # Add more ERCs as needed
}
# Define known selectors for relevant functions
PERMIT_SELECTORS = {
    "permit": "f73aa3c0",  # permit(address,address,uint256,uint256,uint8,bytes32,bytes32)
    "DOMAIN_SEPARATOR": "d7ad3c5c",  # DOMAIN_SEPARATOR() signature
}

# Define ERC standards where these are applicable
APPLICABLE_ERCs = {"ERC2612", "ERC20"}  # Add other standards if applicable
# Define known selectors for permit and DOMAIN_SEPARATOR
PERMIT_SIGNATURE = "f73aa3c0"  # permit(address,address,uint256,uint256,uint8,bytes32,bytes32)
DOMAIN_SEPARATOR_SIGNATURE = "d7ad3c5c"  # DOMAIN_SEPARATOR()


# Drop "0x" prefix from hex strings
def drop0x(hex):
    return (None if hex is None else
            hex[2:] if hex[0:2] == "0x" else
            hex
           )

# Determine the type of contract
def determine_contract_type(signatures):
    sig_set = set(signatures)
    matched_types = []

    for erc, selectors in ERC_SELECTORS.items():
        if any(sig in selectors for sig in sig_set):
            matched_types.append(erc)

    return "+".join(matched_types) if matched_types else "Unknown"

# Check if permit and DOMAIN_SEPARATOR are implemented correctly
def check_permit_and_domain_separator(signatures):
    sig_set = set(signatures)
    permit_present = PERMIT_SELECTORS["permit"] in sig_set
    domain_separator_present = PERMIT_SELECTORS["DOMAIN_SEPARATOR"] in sig_set
    errors = []

    if permit_present and domain_separator_present:
        return "Implemented correctly"
    else:
        if not permit_present:
            errors.append("Missing 'permit' implementation")
        if not domain_separator_present:
            errors.append("Missing 'DOMAIN_SEPARATOR'")
        return ", ".join(errors)

# Determine if permit function arguments are implemented properly
def analyze_permit_function(bytecode, signatures):
    if PERMIT_SIGNATURE not in signatures:
        return "permit function missing"

    # Analyze bytecode to validate `permit` function
    errors = []
    if DOMAIN_SEPARATOR_SIGNATURE not in signatures:
        errors.append("Missing DOMAIN_SEPARATOR")

    # Simulate bytecode parsing for critical parts of permit
    
    if "require(deadline >= block.timestamp" not in str(bytecode):
        errors.append("Missing expiry date check (require on deadline)")

    if "nonces[" not in str(bytecode):
        errors.append("Missing nonce argument for replay protection")

    if "ecrecover" not in str(bytecode):
        errors.append("Missing valid signature check")

    return "Implemented correctly" if not errors else ", ".join(errors) 

# Main loop for processing input
for line in sys.stdin:
    row = line.rstrip('\n').split(';')
    codeid = row[0]
    if codeid == 'codeid':
        print('codeid;signatures;contract_type;permit_check')
        continue
    address = row[1]
    code = bytes.fromhex(drop0x(row[2]))
    sigs = fourbytes.signatures(code)
    sigsHex = [s.hex() for s in sigs]
    contract_type = determine_contract_type(sigsHex)

    # If the contract type matches applicable ERCs, check for `permit` and `DOMAIN_SEPARATOR`
    if any(erc in contract_type for erc in APPLICABLE_ERCs):
        permit_check = check_permit_and_domain_separator(sigsHex)
    else:
        permit_check = "Not applicable"

    
    # Check for proper permit implementation
    permit_check = analyze_permit_function(code, sigsHex)
    
    print(f"{codeid};{sigsHex};{contract_type};{permit_check}")
    
    

    