# Copyright ZettaBlock Labs 2024

# Source: https://github.com/Zettablock/zetta-contracts/blob/develop/examples/abi/Zetta.json
ZETTA_ABI = """
[
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "_datasetFactory",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "_modelFactory",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "_workerNodeProxy",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "_priceOracle",
        "type": "address"
      }
    ],
    "stateMutability": "nonpayable",
    "type": "constructor"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "owner",
        "type": "address"
      }
    ],
    "name": "OwnableInvalidOwner",
    "type": "error"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "account",
        "type": "address"
      }
    ],
    "name": "OwnableUnauthorizedAccount",
    "type": "error"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "address",
        "name": "dataset",
        "type": "address"
      },
      {
        "indexed": true,
        "internalType": "address",
        "name": "owner",
        "type": "address"
      }
    ],
    "name": "DatasetCreated",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "address",
        "name": "modelOwnerAddress",
        "type": "address"
      },
      {
        "indexed": true,
        "internalType": "uint256",
        "name": "requestId",
        "type": "uint256"
      },
      {
        "components": [
          {
            "internalType": "address",
            "name": "modelOwnerAddress",
            "type": "address"
          },
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
            "name": "fineTuneParams",
            "type": "tuple"
          },
          {
            "internalType": "uint256",
            "name": "fineTuneFee",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "inferenceFee",
            "type": "uint256"
          }
        ],
        "indexed": false,
        "internalType": "struct Zetta.FineTuneRequest",
        "name": "fineTuneRequest",
        "type": "tuple"
      }
    ],
    "name": "FineTuneRequestSent",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "address",
        "name": "user",
        "type": "address"
      },
      {
        "indexed": true,
        "internalType": "address",
        "name": "model",
        "type": "address"
      },
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "inferenceFee",
        "type": "uint256"
      },
      {
        "indexed": false,
        "internalType": "bytes",
        "name": "requestData",
        "type": "bytes"
      },
      {
        "indexed": false,
        "internalType": "bytes32",
        "name": "responseHash",
        "type": "bytes32"
      },
      {
        "indexed": false,
        "internalType": "string",
        "name": "requestId",
        "type": "string"
      }
    ],
    "name": "InferenceReceiptSaved",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "address",
        "name": "model",
        "type": "address"
      },
      {
        "indexed": true,
        "internalType": "address",
        "name": "owner",
        "type": "address"
      }
    ],
    "name": "ModelCreated",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "address",
        "name": "model",
        "type": "address"
      },
      {
        "indexed": true,
        "internalType": "address",
        "name": "feePayer",
        "type": "address"
      },
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "fee",
        "type": "uint256"
      }
    ],
    "name": "ModelDeployed",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "address",
        "name": "model",
        "type": "address"
      },
      {
        "indexed": true,
        "internalType": "address",
        "name": "feePayer",
        "type": "address"
      },
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "fee",
        "type": "uint256"
      }
    ],
    "name": "ModelHosted",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "address",
        "name": "previousOwner",
        "type": "address"
      },
      {
        "indexed": true,
        "internalType": "address",
        "name": "newOwner",
        "type": "address"
      }
    ],
    "name": "OwnershipTransferred",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "address",
        "name": "user",
        "type": "address"
      },
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "amount",
        "type": "uint256"
      }
    ],
    "name": "UserDeposited",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "address",
        "name": "user",
        "type": "address"
      }
    ],
    "name": "UserRegistered",
    "type": "event"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "initialOwner",
        "type": "address"
      },
      {
        "internalType": "string",
        "name": "repoName",
        "type": "string"
      },
      {
        "internalType": "string",
        "name": "version",
        "type": "string"
      },
      {
        "internalType": "uint256",
        "name": "fee",
        "type": "uint256"
      }
    ],
    "name": "createDataset",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "initialOwner",
        "type": "address"
      },
      {
        "internalType": "string",
        "name": "repoName",
        "type": "string"
      },
      {
        "internalType": "string",
        "name": "version",
        "type": "string"
      },
      {
        "internalType": "uint256",
        "name": "fee",
        "type": "uint256"
      },
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
        "name": "fineTuneParams",
        "type": "tuple"
      },
      {
        "internalType": "bytes",
        "name": "proof",
        "type": "bytes"
      }
    ],
    "name": "createModel",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "datasetFactory",
    "outputs": [
      {
        "internalType": "contract DatasetFactory",
        "name": "",
        "type": "address"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "components": [
          {
            "internalType": "address",
            "name": "modelId",
            "type": "address"
          },
          {
            "internalType": "uint256",
            "name": "deployModelFee",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "expiredAt",
            "type": "uint256"
          }
        ],
        "internalType": "struct Zetta.DeployModelFeeData",
        "name": "_deployModelFeeData",
        "type": "tuple"
      },
      {
        "internalType": "bytes",
        "name": "_oracleSignature",
        "type": "bytes"
      }
    ],
    "name": "deployModel",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "_user",
        "type": "address"
      },
      {
        "internalType": "uint256",
        "name": "_amount",
        "type": "uint256"
      }
    ],
    "name": "depositToUser",
    "outputs": [],
    "stateMutability": "payable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "name": "fineTuneRequests",
    "outputs": [
      {
        "internalType": "address",
        "name": "modelOwnerAddress",
        "type": "address"
      },
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
        "name": "fineTuneParams",
        "type": "tuple"
      },
      {
        "internalType": "uint256",
        "name": "fineTuneFee",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "inferenceFee",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "_requestId",
        "type": "uint256"
      },
      {
        "internalType": "string",
        "name": "repoName",
        "type": "string"
      },
      {
        "internalType": "string",
        "name": "version",
        "type": "string"
      },
      {
        "internalType": "bytes",
        "name": "_fineTuneProof",
        "type": "bytes"
      }
    ],
    "name": "finishFineTuneRequest",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "components": [
          {
            "internalType": "address",
            "name": "modelId",
            "type": "address"
          },
          {
            "internalType": "uint256",
            "name": "hostModelFee",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "expiredAt",
            "type": "uint256"
          }
        ],
        "internalType": "struct Zetta.HostModelFeeData",
        "name": "_hostModelFeeData",
        "type": "tuple"
      },
      {
        "internalType": "bytes",
        "name": "_oracleSignature",
        "type": "bytes"
      }
    ],
    "name": "hostModel",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "modelFactory",
    "outputs": [
      {
        "internalType": "contract ModelFactory",
        "name": "",
        "type": "address"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "owner",
    "outputs": [
      {
        "internalType": "address",
        "name": "",
        "type": "address"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "priceOracle",
    "outputs": [
      {
        "internalType": "address",
        "name": "",
        "type": "address"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "registerFee",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "registerUser",
    "outputs": [],
    "stateMutability": "payable",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "renounceOwnership",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "string",
        "name": "_requestId",
        "type": "string"
      },
      {
        "components": [
          {
            "internalType": "address",
            "name": "user",
            "type": "address"
          },
          {
            "internalType": "address",
            "name": "model",
            "type": "address"
          },
          {
            "internalType": "bytes",
            "name": "requestData",
            "type": "bytes"
          }
        ],
        "internalType": "struct Zetta.InferenceRequest",
        "name": "_inferenceRequest",
        "type": "tuple"
      },
      {
        "internalType": "bytes",
        "name": "signature",
        "type": "bytes"
      },
      {
        "internalType": "bytes32",
        "name": "_responseHash",
        "type": "bytes32"
      }
    ],
    "name": "saveInferenceReceipt",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
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
      },
      {
        "internalType": "bytes",
        "name": "_oracleSignature",
        "type": "bytes"
      },
      {
        "internalType": "uint256",
        "name": "_inferenceFee",
        "type": "uint256"
      }
    ],
    "name": "sendFineTuneRequest",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "newOwner",
        "type": "address"
      }
    ],
    "name": "transferOwnership",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "_priceOracle",
        "type": "address"
      }
    ],
    "name": "updatePriceOracle",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "_registerFee",
        "type": "uint256"
      }
    ],
    "name": "updateRegisterFee",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "_worker",
        "type": "address"
      }
    ],
    "name": "updateWorker",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "",
        "type": "address"
      }
    ],
    "name": "users",
    "outputs": [
      {
        "internalType": "bool",
        "name": "isRegistered",
        "type": "bool"
      },
      {
        "internalType": "uint256",
        "name": "balance",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "workerNodeProxy",
    "outputs": [
      {
        "internalType": "address",
        "name": "",
        "type": "address"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "workerNodeProxyFee",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  }
]
"""
