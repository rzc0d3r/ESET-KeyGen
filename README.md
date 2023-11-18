# ESET-KeyGen
ESET-KeyGen - Trial-Key & Account generator for ESET Antivirus (last test was on 18.11.2023 at 02:23)

# How to use

## Installing google chrome and driver
> The project now comes bundled with automatic chrome driver installation!!!
> 
> No more fiddling with it, download only chrome and run!

### Windows
1. Download and install [Chrome](https://www.google.com/chrome/)

### Linux (Using Debian as an example)
1. Download [Chrome](https://www.google.com/chrome/) .deb package and install the downloaded package using the command in terminal:

```
apt install %path to deb%
```

## Installing python and libraries

> You can skip this step if you use the compiled .exe file from the release

1. Go to the official [Python website](https://www.python.org/downloads) and download the version for your system (the project runs starting with [Python 3.8.0](https://www.python.org/downloads/release/python-380))

2. Next, install the Python libraries, in terminal using requirements.txt:

```
pip install -r requirements.txt
```

Or without requirements.txt:

```
pip install selenium requests colorama
```

## Preparing ESET
Delete your current ESET HOME account

![](img/delete_eset_home_account.png)

## Using the repository
1. [Account Generator](wiki/AccountGenerator.md)
2. [Key Generator](wiki/KeyGenerator.md)

# Recommendations and information

1. Do not minimize or close the browser window before the program is finished!!!
2. Do not create many license keys and accounts in a short period of time, otherwise you will be blocked in ESET HOME for a certain period of time
3. If the program crashes after many attempts and you know that the program is up to date. Try using a VPN
4. If an ACT0 error occurs during activation, check whether the ESET HOME account is connected. If so, disconnect it and try again.
   If the error persists, try activating with [Account Generator](https://github.com/rzc0d3r/ESET-KeyGen/blob/main/wiki/AccountGenerator.md).
   If still getting this error reinstall ESET and try again.
