# simple.iota
Simple implementation of a client that communicates with the IOTA-network.

This implementation of a client (not a wallet) is made for the Blockchain-course @ FHOOE (Hagenberg)

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



