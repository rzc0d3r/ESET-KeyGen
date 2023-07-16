# ESET-KeyGen
ESET-KeyGen - Key generator for ESET Antivirus (Only for Windows build)

# How to use

0. Download [Chrome](https://www.google.com/chrome/) and his [Stable Driver](https://chromedriver.chromium.org/downloads)

NOTE: If your version of chrome is for example 112.0.5615.87 then you need to download a driver
      with the same version (Only the first 3 digits are taken into account, for example 112)

The driver must be unpacked and moved to the folder with ESET KeyGen.py

Next, install the Python libraries, in cmd or powershell:

```
pip install selenium requests
```

1. Delete your current ESET HOME account

![](img/1.png)

2. Run ESET KeyGen.py and wait until "Press Enter..."
After that you will see in the console the key and the license expiration date.

    This information will also be written to a file named "Today date - ESET KEYS.txt".

![](img/3_1.0.3.png)

3. In ESET, click Activate full version of the product with purchased License Key and enter the key from the console in the box that appears.

![](img/2.png)

Just click "Continue" until you are told that you have successfully activated the antivirus.

# Recommendations and information

1. Do not minimize or close the browser window before the program is finished!!!
2. Do not create many license keys in a short period of time, otherwise you will be blocked in ESET HOME for a certain period of time
3. If the program crashes after many attempts and you know that the program is up to date. Try using a VPN
