![TotpApp Logo](https://mauricelambert.github.io/info/python/security/TotpApp_small.png "TotpApp logo")

# TotpApp

## Description

This little app generates your TOTP from your secret (you can use
secret as password in a password manager), you don't need any phone or
other device

## Requirements

This package require:
 - python3
 - python3 Standard Library

## Installation

### Pip

```bash
python3 -m pip install TotpApp
```

### Git

```bash
git clone "https://github.com/mauricelambert/TotpApp.git"
cd "TotpApp"
python3 -m pip install .
```

### Wget

```bash
wget https://github.com/mauricelambert/TotpApp/archive/refs/heads/main.zip
unzip main.zip
cd TotpApp-main
python3 -m pip install .
```

## Usages

### Command line

```bash
TotpApp              # Using CLI package executable
python3 -m TotpApp   # Using python module
python3 TotpApp.pyz  # Using python executable
TotpApp.exe          # Using python Windows executable
```

### Python script

```python
from TotpApp import *

root = Tk()
app = TotpApp(root)
root.mainloop()
```

## Links

 - [Pypi](https://pypi.org/project/TotpApp)
 - [Github](https://github.com/mauricelambert/TotpApp)
 - [Documentation](https://mauricelambert.github.io/info/python/security/TotpApp.html)
 - [Python executable](https://mauricelambert.github.io/info/python/security/TotpApp.pyz)
 - [Python Windows executable](https://mauricelambert.github.io/info/python/security/TotpApp.exe)

## License

Licensed under the [GPL, version 3](https://www.gnu.org/licenses/).
