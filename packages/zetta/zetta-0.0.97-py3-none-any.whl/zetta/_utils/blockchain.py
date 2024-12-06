# Copyright ZettaBlock Labs 2024
import configparser
from eth_account import Account
import json
import os
from typing import List
import web3
from web3 import Web3

from zetta._utils.abi.zetta import ZETTA_ABI

# Local
# CHAIN_ENDPOINT = os.environ.get('CHAIN_ENDPOINT', "http://localhost:8545")
# ZETTA_CONTRACT_ADDR = os.environ.get("ZETTA_CONTRACT_ADDR", "0x9fE46736679d2D9a65F0992F2272dE9f3c7fa6e0")
# private_key = os.environ.get("PRIVATE_KEY", '0x5de4111afa1a4b94908f83103eb1f1706367c2e68ca870fc3fb9a804cdab365a')

# Base Sepolia
CHAIN_ENDPOINT = "https://sepolia.base.org"
ZETTA_CONTRACT_ADDR = "0x47A07fCfB35F9c5aA49a17df88e2002CF4754e8F"

NULL_ADDRESS = "0x0000000000000000000000000000000000000000"
UINT256_MAX = 2**256 - 1

w3 = Web3(provider=Web3.HTTPProvider(CHAIN_ENDPOINT))

def send_fine_tune_request(
    parent_model_addr: str = NULL_ADDRESS,
    dataset_addrs: List[str] = [],
    tuning_code_hash: bytes = bytes.fromhex('0' * 64),
    fine_tune_fee: int = 0,
    expired_at: int = UINT256_MAX,
    private_key: str = None,
    chain_id: int = 1,
    zetta_contract_addr: str = ZETTA_CONTRACT_ADDR,
):
    private_key = private_key or get_wallet_private_key_from_profile()
    assert private_key is not None, "Wallet private key not found"

    account = Account.from_key(private_key)
    # register account to web3 node
    w3.middleware_onion.add(web3.middleware.construct_sign_and_send_raw_middleware(account))

    zetta_abi = json.loads(ZETTA_ABI)
    zetta_contract = w3.eth.contract(address=zetta_contract_addr, abi=zetta_abi)

    userAfterRegister = zetta_contract.functions.users(account.address).call()
    assert userAfterRegister[0], "Please register your wallet first at https://base-sepolia.blockscout.com/address/0x47A07fCfB35F9c5aA49a17df88e2002CF4754e8F?tab=write_contract"
    print(f"Using wallet {account.address}. Your Zetta balance is {userAfterRegister[1]}")
    # TODO: auto register user if not registered

    # ABI encoding
    fine_tune_fee_data = (
        [
            parent_model_addr, # parentModelId
            dataset_addrs, # datasetIds
            tuning_code_hash, # tuningCodeHash
        ], # fineTuneRequest
        expired_at, # expiredAt
        fine_tune_fee, # fineTuneFee
    )

    packed = encode_fine_tune_fee_data(fine_tune_fee_data)
    hash_bytes = Web3.keccak(packed)
    prefix = b'\x19Ethereum Signed Message:\n32'
    prefixed_hash = Web3.keccak(prefix + hash_bytes)

    oracle_private_key = os.getenv('ORACLE_PRIVATE_KEY', '5b579d7ddc6963ebe05f43005c9c89050d44b1decff25aada8ddd4d993677e59')
    if not oracle_private_key:
        raise ValueError("ORACLE_PRIVATE_KEY not set in environment variables")

    oracle_account = Account.from_key(oracle_private_key)
    fee_sig = oracle_account.signHash(prefixed_hash)

    tx_hash = zetta_contract.functions.sendFineTuneRequest(
        fine_tune_fee_data,
        fee_sig.signature,
        fine_tune_fee
    ).transact(
        {"from": account.address})
    # Wait for transaction receipt
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    # Filter and log FineTuneRequestSent events
    events = zetta_contract.events.FineTuneRequestSent().process_receipt(tx_receipt)
    return events


def get_wallet_private_key_from_profile():
    zetta_root = os.path.expanduser("~")
    secrets_path = os.path.join(zetta_root, ".zetta/secrets")
    token = None
    if os.path.exists(secrets_path):
        config = configparser.ConfigParser()
        config.read(secrets_path)
        token = config.get('default', 'wallet_private_key', fallback=None)
    if token is None:
        raise ValueError(f"Wallet private key not found at path: {secrets_path}. Please run `zetta setup` or `zetta wallet` to create a wallet first.")
    return token


def get_transaction_link(tx_hash: str):
    return f"https://base-sepolia.blockscout.com/tx/{tx_hash}"

"""
Encode utils
"""
def encode_fine_tune_fee_data(fine_tune_fee_data):
    abi = json.loads("""[
        {
        "inputs": [
        {
            "components": [
            {
                "components": [
                {
                    "internalType": "address",
                    "name": "parentModelId",
                    "type": "address"
                },
                {
                    "internalType": "address[]",
                    "name": "datasetIds",
                    "type": "address[]"
                },
                {
                    "internalType": "bytes32",
                    "name": "tuningCodeHash",
                    "type": "bytes32"
                }
                ],
                "internalType": "struct Zetta.FineTuneParams",
                "name": "fineTuneRequest",
                "type": "tuple"
            },
            {
                "internalType": "uint256",
                "name": "expiredAt",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "fineTuneFee",
                "type": "uint256"
            }
            ],
            "internalType": "struct Zetta.FineTuneFeeData",
            "name": "_fineTuneFeeData",
            "type": "tuple"
        }
        ],
        "name": "sendFineTuneRequest",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
    ]""")
    temp_contract = w3.eth.contract(address=NULL_ADDRESS, abi=abi)
    bytestr = temp_contract.encodeABI(fn_name='sendFineTuneRequest', args=(fine_tune_fee_data,))
    packed = bytes.fromhex(bytestr[2:])[4:]
    return packed
