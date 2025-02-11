import json
from eth_utils import keccak

def get_event_topic(event_signature: str) -> str:
    return "0x" + keccak(text=event_signature).hex()

def get_selector(function_signature: str) -> str:
    hash_bytes = keccak(text=function_signature)
    selector = hash_bytes[:4].hex()
    return selector

def build_erc_config(erc_name: str, function_signatures: dict, topics: list = None, events: dict = None) -> dict:
    topics = topics or []
    events = events or {}
    selectors = {}
    for sig in function_signatures:
        selectors[sig] = get_selector(sig)
    config = {
        erc_name: {
            "selectors": list(selectors.values()),
            "topics": topics,
            "functions": selectors,
            "events": events
        }
    }
    return config



# ERC-20
erc20_functions = {
    "allowance(address,address)": None,
    "approve(address,uint256)": None,
    "balanceOf(address)": None,
    "totalSupply()": None,
    "transfer(address,uint256)": None,
    "transferFrom(address,address,uint256)": None
}
erc20_event_signatures = {
    "Approval": "Approval(address,address,uint256)",
    "Transfer": "Transfer(address,address,uint256)"
}
erc20_events = {}
erc20_topics = []
for key, sig in erc20_event_signatures.items():
    topic = get_event_topic(sig)
    erc20_events[topic] = f"event {sig}"
    erc20_topics.append(topic)
erc20_config = build_erc_config("ERC20", erc20_functions, topics=erc20_topics, events=erc20_events)

# ERC-721
erc721_functions = {
    "approve(address,uint256)": None,
    "balanceOf(address)": None,
    "getApproved(uint256)": None,
    "isApprovedForAll(address,address)": None,
    "ownerOf(uint256)": None,
    "safeTransferFrom(address,address,uint256)": None,
    "safeTransferFrom(address,address,uint256,bytes)": None,
    "setApprovalForAll(address,bool)": None,
    "supportsInterface(bytes4)": None,
    "transferFrom(address,address,uint256)": None
}
erc721_event_signatures = {
    "Approval": "Approval(address,address,uint256)",
    "ApprovalForAll": "ApprovalForAll(address,address,bool)",
    "Transfer": "Transfer(address,address,uint256)"
}
erc721_events = {}
erc721_topics = []
for key, sig in erc721_event_signatures.items():
    topic = get_event_topic(sig)
    erc721_events[topic] = f"event {sig}"
    erc721_topics.append(topic)
erc721_config = build_erc_config("ERC721", erc721_functions, topics=erc721_topics, events=erc721_events)

# ERC-1155
erc1155_functions = {
    "balanceOf(address,uint256)": None,
    "balanceOfBatch(address[],uint256[])": None,
    "isApprovedForAll(address,address)": None,
    "safeBatchTransferFrom(address,address,uint256[],uint256[],bytes)": None,
    "safeTransferFrom(address,address,uint256,uint256,bytes)": None,
    "setApprovalForAll(address,bool)": None,
    "supportsInterface(bytes4)": None
}
erc1155_event_signatures = {
    "ApprovalForAll": "ApprovalForAll(address,address,bool)",
    "TransferBatch": "TransferBatch(address,address,address,uint256[],uint256[])",
    "TransferSingle": "TransferSingle(address,address,address,uint256,uint256)",
    "URI": "URI(string,uint256)"
}
erc1155_events = {}
erc1155_topics = []
for key, sig in erc1155_event_signatures.items():
    topic = get_event_topic(sig)
    erc1155_events[topic] = f"event {sig}"
    erc1155_topics.append(topic)
erc1155_config = build_erc_config("ERC1155", erc1155_functions, topics=erc1155_topics, events=erc1155_events)

# ERC-165
erc165_functions = {
    "supportsInterface(bytes4)": None
}
erc165_config = build_erc_config("ERC165", erc165_functions)

# ERC-173
erc173_functions = {
    "owner()": None,
    "supportsInterface(bytes4)": None,
    "transferOwnership(address)": None
}
erc173_event_signature = "OwnershipTransferred(address,address)"
erc173_topic = get_event_topic(erc173_event_signature)
erc173_topics = [erc173_topic]
erc173_events = {
    erc173_topic: "event OwnershipTransferred(address indexed previousOwner, address indexed newOwner)"
}
erc173_config = build_erc_config("ERC173", erc173_functions, topics=erc173_topics, events=erc173_events)




# ERC-777
erc777_functions = {
    "name()": None,
    "symbol()": None,
    "totalSupply()": None,
    "balanceOf(address)": None,
    "send(address,uint256,bytes)": None,
    "transfer(address,uint256)": None,
    "authorizeOperator(address)": None,
    "revokeOperator(address)": None,
    "isOperatorFor(address,address)": None,
    "operatorSend(address,address,uint256,bytes,bytes)": None,
    "burn(uint256,bytes)": None,
    "operatorBurn(address,uint256,bytes,bytes)": None,
    "granularity()": None
}
erc777_event_signatures = {
    "Sent": "Sent(address,address,address,uint256,bytes,bytes)",
    "Minted": "Minted(address,address,uint256,bytes,bytes)",
    "Burned": "Burned(address,address,uint256,bytes,bytes)",
    "AuthorizedOperator": "AuthorizedOperator(address,address)",
    "RevokedOperator": "RevokedOperator(address,address)"
}
erc777_events = {}
erc777_topics = []
for key, sig in erc777_event_signatures.items():
    topic = get_event_topic(sig)
    erc777_events[topic] = f"event {sig}"
    erc777_topics.append(topic)
erc777_config = build_erc_config("ERC777", erc777_functions, topics=erc777_topics, events=erc777_events)

# ERC-2981
erc2981_functions = {
    "royaltyInfo(uint256,uint256)": None
}
erc2981_config = build_erc_config("ERC2981", erc2981_functions)

# ERC-223
erc223_functions = {
    "transfer(address,uint256,bytes)": None,
    "tokenReceived(address,uint256,bytes)": None
}
erc223_event_signature = "Transfer(address,address,uint256,bytes)"
erc223_topic = get_event_topic(erc223_event_signature)
erc223_topics = [erc223_topic]
erc223_events = {
    erc223_topic: "event Transfer(address indexed from, address indexed to, uint256 value, bytes data)"
}
erc223_config = build_erc_config("ERC223", erc223_functions, topics=erc223_topics, events=erc223_events)

# ERC-884
erc884_functions = {
    "getCurrentFor(address)": None,
    "isSuperseded(address)": None,
    "holderAt(uint256)": None,
    "holderCount()": None,
    "isVerified(address)": None,
    "isHolder(address)": None,
    "hasHash(address,bytes32)": None,
    "addVerified(address,bytes32)": None,
    "removeVerified(address)": None,
    "updateVerified(address,bytes32)": None,
    "cancelAndReissue(address,address)": None
}
erc884_event_signatures = {
    "VerifiedAddressAdded": "VerifiedAddressAdded(address,bytes32)",
    "VerifiedAddressRemoved": "VerifiedAddressRemoved(address)",
    "VerifiedAddressUpdated": "VerifiedAddressUpdated(address,bytes32)",
    "HolderAdded": "HolderAdded(address)",
    "HolderRemoved": "HolderRemoved(address)"
}
erc884_events = {}
erc884_topics = []
for key, sig in erc884_event_signatures.items():
    topic = get_event_topic(sig)
    erc884_events[topic] = f"event {sig}"
    erc884_topics.append(topic)
erc884_config = build_erc_config("ERC884", erc884_functions, topics=erc884_topics, events=erc884_events)

# ERC-998
erc998_functions = {
    "transferChild(uint256,address,uint256)": None,
    "safeTransferChild(uint256,address,uint256,bytes)": None,
    "transferChildToParent(address,uint256,address,uint256,uint256,bytes)": None,
    "getChild(address,uint256,address,uint256)": None,
    "safeTransferChild(uint256,address,address,uint256)": None,
    "onERC721Received(address,address,uint256,bytes)": None,
    "ownerOfChild(address,uint256)": None,
    "childContractByIndex(uint256,uint256)": None,
    "childTokenByIndex(uint256,uint256)": None,
    "rootOwnerOfChild(address,uint256)": None,
    "rootOwnerOf(uint256)": None
}
erc998_event_signatures = {
    "TransferChild": "TransferChild(uint256,address,uint256)",
    "ReceivedChild": "ReceivedChild(address,uint256,address,uint256)"
}
erc998_events = {}
erc998_topics = []
for key, sig in erc998_event_signatures.items():
    topic = get_event_topic(sig)
    erc998_events[topic] = f"event {sig}"
    erc998_topics.append(topic)
erc998_config = build_erc_config("ERC998", erc998_functions, topics=erc998_topics, events=erc998_events)

# ERC-1363
erc1363_functions = {
    "transferAndCall(address,uint256)": None,
    "transferAndCall(address,uint256,bytes)": None,
    "transferFromAndCall(address,address,uint256)": None,
    "transferFromAndCall(address,address,uint256,bytes)": None,
    "approveAndCall(address,uint256)": None,
    "approveAndCall(address,uint256,bytes)": None,
    "onTransferReceived(address,address,uint256,bytes)": None,
    "onApprovalReceived(address,uint256,bytes)": None
}
erc1363_event_signatures = {
    "Transfer": "Transfer(address,address,uint256)",
    "Approval": "Approval(address,address,uint256)"
}
erc1363_events = {}
erc1363_topics = []
for key, sig in erc1363_event_signatures.items():
    topic = get_event_topic(sig)
    erc1363_events[topic] = f"event {sig}"
    erc1363_topics.append(topic)
erc1363_config = build_erc_config("ERC1363", erc1363_functions, topics=erc1363_topics, events=erc1363_events)

# ERC-875
erc875_functions = {
    "name()": None,
    "symbol()": None,
    "balanceOf(address)": None,
    "transfer(address,uint256[])": None,
    "transferFrom(address,address,uint256[])": None,
    "totalSupply()": None,
    "ownerOf(uint256)": None,
    "trade(uint256,uint256[],uint8,bytes32,bytes32)": None
}
erc875_event_signatures = {
    "Transfer": "Transfer(address,address,uint256[])",
    "Trade": "Trade(uint256,uint256[],uint8,bytes32,bytes32)"
}
erc875_events = {}
erc875_topics = []
for key, sig in erc875_event_signatures.items():
    topic = get_event_topic(sig)
    erc875_events[topic] = f"event {sig}"
    erc875_topics.append(topic)
erc875_config = build_erc_config("ERC875", erc875_functions, topics=erc875_topics, events=erc875_events)

# ERC-1046
erc1046_functions = {
    "tokenURI()": None
}
erc1046_config = build_erc_config("ERC1046", erc1046_functions)

# ERC-2612
erc2612_functions = {
    "permit(address,address,uint256,uint256,uint8,bytes32,bytes32)": None,
    "nonces(address)": None,
    "DOMAIN_SEPARATOR()": None
}
erc2612_event_signature = "Permit(address,address,uint256,uint256,uint8,bytes32,bytes32)"
erc2612_topic = get_event_topic(erc2612_event_signature)
erc2612_topics = [erc2612_topic]
erc2612_events = {
    erc2612_topic: "event Permit(address indexed owner, address indexed spender, uint256 value, uint256 deadline, uint8 v, bytes32 r, bytes32 s)"
}
erc2612_config = build_erc_config("ERC2612", erc2612_functions, topics=erc2612_topics, events=erc2612_events)

# ERC-1948
erc1948_functions = {
    "readData(uint256)": None,
    "writeData(uint256,bytes)": None
}
erc1948_event_signature = "DataUpdated(uint256,bytes)"
erc1948_topic = get_event_topic(erc1948_event_signature)
erc1948_topics = [erc1948_topic]
erc1948_events = {
    erc1948_topic: "event DataUpdated(uint256 indexed tokenId, bytes data)"
}
erc1948_config = build_erc_config("ERC1948", erc1948_functions, topics=erc1948_topics, events=erc1948_events)

# ERC-1261
erc1261_functions = {
    "addMember(address,uint256[])": None,
    "revokeMembership(address)": None,
    "getMemberRoles(address)": None,
    "isMember(address)": None,
    "name()": None,
    "symbol()": None
}
erc1261_event_signatures = {
    "MemberAdded": "MemberAdded(address,uint256[])",
    "MembershipRevoked": "MembershipRevoked(address)"
}
erc1261_events = {}
erc1261_topics = []
for key, sig in erc1261_event_signatures.items():
    topic = get_event_topic(sig)
    erc1261_events[topic] = f"event {sig}"
    erc1261_topics.append(topic)
erc1261_config = build_erc_config("ERC1261", erc1261_functions, topics=erc1261_topics, events=erc1261_events)

# ERC-1337
erc1337_functions = {
    "modifyStatus(uint256,uint8,bytes)": None,
    "executeSubscription(address,uint256,bytes,uint8,uint256,uint256,uint256,address,bytes,bytes)": None,
    "isValidSubscription(uint256)": None,
    "getSubscriptionStatus(uint256)": None,
    "getSubscriptionHash(address,uint256,bytes,uint8,uint256,uint256,uint256,address,bytes)": None,
    "getModifyStatusHash(bytes32,uint8)": None
}
erc1337_event_signatures = {
    "SubscriptionExecuted": "SubscriptionExecuted(address,uint256,bytes,uint8,uint256,uint256,uint256,address,bytes,bytes)",
    "StatusModified": "StatusModified(uint256,uint8,bytes)"
}
erc1337_events = {}
erc1337_topics = []
for key, sig in erc1337_event_signatures.items():
    topic = get_event_topic(sig)
    erc1337_events[topic] = f"event {sig}"
    erc1337_topics.append(topic)
erc1337_config = build_erc_config("ERC1337", erc1337_functions, topics=erc1337_topics, events=erc1337_events)

# ERC-2021
erc2021_functions = {
    "orderPayoutFrom(string,address,uint256,string)": None,
    "orderPayout(string,uint256,string)": None,
    "authorizePayoutOperator(address)": None,
    "revokePayoutOperator(address)": None,
    "cancelPayout(string)": None,
    "processPayout(string)": None,
    "putFundsInSuspenseInPayout(string)": None,
    "executePayout(string)": None,
    "rejectPayout(string,string)": None,
    "isPayoutOperatorFor(address,address)": None,
    "retrievePayoutData(string)": None
}
erc2021_event_signatures = {
    "PayoutOrdered": "PayoutOrdered(string,address,uint256,string)",
    "PayoutProcessed": "PayoutProcessed(string)",
    "PayoutExecuted": "PayoutExecuted(string)",
    "PayoutRejected": "PayoutRejected(string,string)"
}
erc2021_events = {}
erc2021_topics = []
for key, sig in erc2021_event_signatures.items():
    topic = get_event_topic(sig)
    erc2021_events[topic] = f"event {sig}"
    erc2021_topics.append(topic)
erc2021_config = build_erc_config("ERC2021", erc2021_functions, topics=erc2021_topics, events=erc2021_events)

# ERC-2018
erc2018_functions = {
    "orderTransfer(string,address,uint256)": None,
    "orderTransferFrom(string,address,address,uint256)": None,
    "authorizeClearableTransferOperator(address)": None,
    "revokeClearableTransferOperator(address)": None,
    "cancelTransfer(string)": None,
    "processClearableTransfer(string)": None,
    "executeClearableTransfer(string)": None,
    "rejectClearableTransfer(string,string)": None,
    "retrieveClearableTransferData(string)": None,
    "isClearableTransferOperatorFor(address,address)": None
}
erc2018_event_signatures = {
    "TransferOrdered": "TransferOrdered(string,address,uint256)",
    "TransferProcessed": "TransferProcessed(string)",
    "TransferExecuted": "TransferExecuted(string)",
    "TransferRejected": "TransferRejected(string,string)"
}
erc2018_events = {}
erc2018_topics = []
for key, sig in erc2018_event_signatures.items():
    topic = get_event_topic(sig)
    erc2018_events[topic] = f"event {sig}"
    erc2018_topics.append(topic)
erc2018_config = build_erc_config("ERC2018", erc2018_functions, topics=erc2018_topics, events=erc2018_events)

# ERC-2019
erc2019_functions = {
    "authorizeFundOperator(address)": None,
    "revokeFundOperator(address)": None,
    "orderFund(string,uint256,string)": None,
    "orderFundFrom(string,address,uint256,string)": None,
    "cancelFund(string)": None,
    "processFund(string)": None,
    "executeFund(string)": None,
    "rejectFund(string,string)": None,
    "isFundOperatorFor(address,address)": None,
    "retrieveFundData(address,string)": None
}
erc2019_event_signatures = {
    "FundOrdered": "FundOrdered(string,uint256,string)",
    "FundProcessed": "FundProcessed(string)",
    "FundExecuted": "FundExecuted(string)",
    "FundRejected": "FundRejected(string,string)"
}
erc2019_events = {}
erc2019_topics = []
for key, sig in erc2019_event_signatures.items():
    topic = get_event_topic(sig)
    erc2019_events[topic] = f"event {sig}"
    erc2019_topics.append(topic)
erc2019_config = build_erc_config("ERC2019", erc2019_functions, topics=erc2019_topics, events=erc2019_events)

# ERC-1996
erc1996_functions = {
    "hold(string,address,address,uint256,uint256)": None,
    "holdFrom(string,address,address,address,uint256,uint256)": None,
    "releaseHold(string)": None,
    "executeHold(string,uint256)": None,
    "renewHold(string,uint256)": None,
    "retrieveHoldData(string)": None,
    "balanceOnHold(address)": None,
    "netBalanceOf(address)": None,
    "totalSupplyOnHold()": None,
    "authorizeHoldOperator(address)": None,
    "revokeHoldOperator(address)": None,
    "isHoldOperatorFor(address,address)": None
}
erc1996_event_signatures = {
    "HoldCreated": "HoldCreated(string,address,address,uint256,uint256)",
    "HoldReleased": "HoldReleased(string)",
    "HoldExecuted": "HoldExecuted(string,uint256)",
    "HoldRenewed": "HoldRenewed(string,uint256)"
}
erc1996_events = {}
erc1996_topics = []
for key, sig in erc1996_event_signatures.items():
    topic = get_event_topic(sig)
    erc1996_events[topic] = f"event {sig}"
    erc1996_topics.append(topic)
erc1996_config = build_erc_config("ERC1996", erc1996_functions)


erc2020_functions = {
    "currency()": None,
    "version()": None,
    "availableFunds(address)": None,
    "checkTransferAllowed(address,address,uint256)": None,
    "checkApproveAllowed(address,address,uint256)": None,
    "checkHoldAllowed(address,address,address,uint256)": None,
    "checkAuthorizeHoldOperatorAllowed(address,address)": None,
    "checkOrderTransferAllowed(address,address,uint256)": None,
    "checkAuthorizeClearableTransferOperatorAllowed(address,address)": None,
    "checkOrderFundAllowed(address,address,uint256)": None,
    "checkAuthorizeFundOperatorAllowed(address,address)": None,
    "checkOrderPayoutAllowed(address,address,uint256)": None,
    "checkAuthorizePayoutOperatorAllowed(address,address)": None
}
erc2020_config = build_erc_config("ERC2020", erc2020_functions)


erc3135_functions = {
    "iconUrl()": None,
    "issuer()": None,
    "claim(address,uint256,uint256,bytes)": None,
    "transferIssuer(address)": None,
    "deposit(uint256)": None,
    "withdraw(address,uint256)": None,
    "depositBalanceOf(address)": None
}
erc3135_config = build_erc_config("ERC3135", erc3135_functions)


erc3440_functions = {
    "signArtwork(uint256,bytes)": None,
    "getSignature(uint256)": None,
    "verifySignature(uint256,bytes)": None,
    "setEditionLimit(uint256,uint256)": None,
    "getEditionLimit(uint256)": None,
    "markAsOriginal(uint256)": None,
    "isOriginal(uint256)": None,
    "setArtist(address)": None,
    "getArtist(uint256)": None
}
erc3440_topics = [
    "artworkSigned_topic_hash"
]

erc3440_events = {
    "artworkSigned_topic_hash": "event ArtworkSigned(uint256 indexed tokenId, address indexed artist, bytes signature)"
}


erc3440_config = build_erc_config("ERC3440", erc3440_functions, topics=erc3440_topics, events=erc3440_events)


erc3589_functions = {
    "hash(uint256,address[],uint256[])": None,
    "mint(address,address[],uint256[])": None,
    "safeMint(address,address[],uint256[])": None,
    "burn(address,uint256,uint256,address[],uint256[])": None
}

erc3589_event_signature = "AssemblyTokenMinted(uint256,address,address[],uint256[])"
erc3589_event_topic = get_event_topic(erc3589_event_signature)
erc3589_topics = [erc3589_event_topic]
erc3589_events = {
    erc3589_event_topic: "event AssemblyTokenMinted(uint256 indexed tokenId, address indexed to, address[] addresses, uint256[] numbers)"
}


erc3589_config = build_erc_config("ERC3589", erc3589_functions, topics=erc3589_topics, events=erc3589_events)


erc3754_functions = {
    "balanceOf(address)": None,
    "ownerOf(uint256)": None,
    "approve(address,uint256)": None,
    "getApproved(uint256)": None,
    "setApprovalForAll(address,bool)": None,
    "isApprovedForAll(address,address)": None,
    "transferFrom(address,address,uint256)": None,
    "safeTransferFrom(address,address,uint256)": None,
    "safeTransferFrom(address,address,uint256,bytes)": None
}

erc3754_event_signatures = {
    "Transfer": "Transfer(address,address,uint256)",
    "Approval": "Approval(address,address,uint256)",
    "ApprovalForAll": "ApprovalForAll(address,address,bool)"
}

erc3754_events = {}
erc3754_topics = []
for key, sig in erc3754_event_signatures.items():
    topic = get_event_topic(sig)
    erc3754_events[topic] = f"event {sig}"
    erc3754_topics.append(topic)

erc3754_config = build_erc_config("ERC3754", erc3754_functions, topics=erc3754_topics, events=erc3754_events)

erc4494_functions = {
    "permit(address,uint256,uint256,uint8,bytes32,bytes32)": None
}

erc4494_config = build_erc_config("ERC4494", erc4494_functions)


erc4524_functions = {
    "safeTransfer(address,uint256)": None,
    "safeTransfer(address,uint256,bytes)": None,
    "safeTransferFrom(address,address,uint256)": None,
    "safeTransferFrom(address,address,uint256,bytes)": None,
    "onERC20Received(address,address,uint256,bytes)": None
}

# For ERC-4524, we include the standard ERC-20 Transfer event as an example.
erc4524_event_signature = "Transfer(address,address,uint256)"
erc4524_topic = get_event_topic(erc4524_event_signature)
erc4524_topics = [erc4524_topic]
erc4524_events = {
    erc4524_topic: "event Transfer(address indexed from, address indexed to, uint256 value)"
}

erc4524_config = build_erc_config("ERC4524", erc4524_functions, topics=erc4524_topics, events=erc4524_events)



erc4675_functions = {
    "transfer(address,uint256,uint256)": None,
    "approve(address,uint256,uint256)": None,
    "transferFrom(address,address,uint256,uint256)": None,
    "setParentNFT(address,uint256,uint256)": None,
    "totalSupply(uint256)": None,
    "balanceOf(address,uint256)": None,
    "allowance(address,address,uint256)": None,
    "isRegistered(address,uint256)": None,
    "onERC721Received(address,address,uint256,bytes)": None
}



erc4675_event_signatures = {
    "Transfer": "Transfer(address,address,uint256,uint256)",
    "Approval": "Approval(address,address,uint256,uint256)",
    "ParentNFTRegistered": "ParentNFTRegistered(address,uint256,uint256)"
}

erc4675_events = {}
erc4675_topics = []
for key, sig in erc4675_event_signatures.items():
    topic = get_event_topic(sig)
    erc4675_events[topic] = f"event {sig}"
    erc4675_topics.append(topic)

erc4675_config = build_erc_config("ERC4675", erc4675_functions, topics=erc4675_topics, events=erc4675_events)


# Combine all configurations into one final object.
final_config = {}

final_config.update(erc20_config)
final_config.update(erc721_config)
final_config.update(erc1155_config)
final_config.update(erc165_config)
final_config.update(erc173_config)

final_config.update(erc777_config)
final_config.update(erc2981_config)
final_config.update(erc223_config)
final_config.update(erc884_config)
final_config.update(erc998_config)
final_config.update(erc1363_config)
final_config.update(erc875_config)
final_config.update(erc1046_config)
final_config.update(erc2612_config)
final_config.update(erc1948_config)
final_config.update(erc1261_config)
final_config.update(erc1337_config)
final_config.update(erc2021_config)
final_config.update(erc2018_config)
final_config.update(erc2019_config)
final_config.update(erc1996_config)
final_config.update(erc2020_config)
final_config.update(erc3135_config)
final_config.update(erc3440_config)
final_config.update(erc3589_config)
final_config.update(erc3754_config)
final_config.update(erc4494_config)
final_config.update(erc4524_config)
final_config.update(erc4675_config)




# Write the configuration to a JSON file.
output_filename = "erc_config.json"
with open(output_filename, "w") as f:
    json.dump(final_config, f, indent=4)

print(f"Configuration for ERC standards has been written to {output_filename}.")
