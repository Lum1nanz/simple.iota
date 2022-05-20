# simple.iota
Simple implementation of a client that communicates with the IOTA-network.

This implementation of a client (not a wallet) is made for the Blockchain-course @ FHOOE (Hagenberg) by Matthias Lauß & Thomas Lumesberger

## Getting ready
To get started, the IOTA foundation builds python wheels on [github](https://github.com/iotaledger/wallet.rs/actions/workflows/python_binding_publish.yml), which have to be installed manually - currently there no up-to-date library that can be installed via `pip`.

To reproduce the installation, download the correct wheel for your OS and python-version, put it into the folder `iota-wheel`. Then execute the following commands:
```zsh
cd iota-wheel
pip install <wheel-file>
```

After the install check if it worked with the command:
```zsh
pip list
```

Inside the whole list, there should be some package called `iota-wallet-python` with the version according to the wheel that was downloaded.

*NOTE: This implementation was done with the wheel `iota_wallet_python-0.2.0-cp36-abi3-macosx_10_7_x86_64.whl`*


## Capabilities

This simple wallet has an integrated user-management-system, meaning you can create multiple users, which can then create an account on the IOTA-Blockchain. This functionality would also been provided by the IOTA-library, but we were pretty lost in the beginning and didn't look close enough...🙄

Other than the user-management, the client can communicate with the IOTA blockchain (TestNet) and do the following things:
 - Create a new Account on the IOTA-Blockchain
 - Check Balance of an Account
 - Generate a new address for the account
 - Send funds to another account
 - List all transactions of the past and their confirmation-status

Additionally the created users of the client are persistently stored and encrypted (but might not be enough) - the storage of the stronghold-password inside the .env-file is just a workaround to make the client work. This should be secured far better.
