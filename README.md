# ESET-KeyGen
ESET-KeyGen - Trial-Key & Account generator for ESET Antivirus (last test was on 13.11.2024 at 03:49 UTC+3)

# Project Preview
![](img/project_preview.png)

## Disclaimer 
### Important: This tool is for educational purposes only.
- Using this tool may violate ESET's terms of service and could have legal implications. The authors and contributors are not responsible for any misuse or damage caused by this project. Use at your own risk and only on systems you own or have explicit permission to test.
---
# If my page or project will be blocked, please refer to these links
* My personal [Telegram](https://t.me/rzc0d3r)
* My [public channel with archives of my projects](https://t.me/rzc0d3r_official)

---
## Project Status 
- Current Status: Active development

## Known Errors
- **Mailticking** added **cloudflare** captcha
- **ACT0** error may occur during activation in some cases
- **ecp4125** activation error has been reported by some users
- **ESET ProtectHub** has an aggressive policy for temporary email addresses!

## Planned Features
- Improved error handling/reporting
- Support

---
### Project files are detected as viruses by ESET, this is not true!
To stop my project from being blocked by antivirus, add the project folder to the exclusion list:

ESET -> Settings -> Advanced Setup -> Detection Engine -> Exclusions -> Detection Exclusions -> add ```full path to ESET-KeyGen-main folder```

That's it!
---

---
### My github page is currently blocked by ESET Antivirus, so you will not be able to access the project.
### Before you can access my github page, you need to disable internet protection in Eset Antivirus. You now have access to this release! After you have done everything you want to do, turn internet protection back on.
### [The second way around this](wiki/GithubWorkaround.md)
---

# Getting Started

## Using GitHub Actions CI
You can simply use the GitHub actions workflow given [here](https://github.com/rzc0d3r/ESET-KeyGen/blob/main/.github/workflows/eset.yml) in your GitHub repo.

Make a fork of my project. Go to it.
Then goto the **Actions** tab, choose **Generator** actions and then run the workflow.

It will ask the number of accounts, keys to be generated.

---

## Using your device

### Prerequisites 
 Choose one of the following supported browsers
 
#### Google Chrome (fully supports)

1. [How to install Chrome on Windows](https://support.google.com/chrome/answer/95346?hl=en&co=GENIE.Platform%3DDesktop#zippy=%2Cwindows)
2. [How to install Chrome on Linux](https://support.google.com/chrome/answer/95346?hl=en&co=GENIE.Platform%3DDesktop#zippy=%2Clinux)
3. [How to install Chrome on Mac](https://support.google.com/chrome/answer/95346?hl=en&co=GENIE.Platform%3DDesktop#zippy=%2Clinux%2Cmac)

#### Mozilla Firefox (fully supports)
1. [How to install Firefox on Windows](https://support.mozilla.org/en-US/kb/how-install-firefox-windows)
2. [How to Install Firefox on Linux](https://support.mozilla.org/en-US/kb/install-firefox-linux)
3. [How to Install Firefox on Mac](https://support.mozilla.org/en-US/kb/how-download-and-install-firefox-mac)

#### Microsoft Edge (fully supports)
1. [Download](https://www.microsoft.com/en-us/edge/download?form=MA13L8)

---

### Installing python and libraries

> You can skip this step if you use the compiled executable file from the release

1. Go to the official [Python website](https://www.python.org/downloads) and download the version for your system (the project runs starting with [Python 3.8.0](https://www.python.org/downloads/release/python-380))

2. Next, install/upgrade the Python libraries, in terminal using requirements.txt:

```
pip install -r requirements.txt
```

---

## Preparing ESET
Delete your current ESET HOME account

![](img/delete_eset_home_account.png)

---

## How to use (Part 2)
1. [Account Generator](wiki/AccountGenerator.md)
2. [Key Generator](wiki/KeyGenerator.md)
3. [Command Line Arguments](wiki/CommandLineArguments.md)
4. [Updater](wiki/Updater.md)
---

# Additional information

1. Do not minimize or close the browser window before the program is finished!!!
2. Do not create many license keys and accounts in a short period of time, otherwise you will be blocked in ESET HOME for a certain period of time
3. If the program crashes after many attempts and you know that the program is up to date. Try using a VPN
4. If an **ACT0** error occurs during activation, check whether the ESET HOME account is connected. If so, disconnect it and try again.
   If the error persists, try activating with [Account Generator](https://github.com/rzc0d3r/ESET-KeyGen/blob/main/wiki/AccountGenerator.md).
   If still getting this error reinstall ESET and try again.
5. The **ecp4125** error may appear when trying to activate the antivirus using an account. Solution: try again later or use keys.
6. You can use the ``--skip-webdriver-menu`` argument, which will skip my WebDriverInstaller shell (Useful for various bugs with webdriver updates, and when using a non-standard browser like Brave or some dev-build, etc).
   The program will also install the browser itself via selenium-manager if it is not present in your system!
7. If you are having trouble initializing any web driver, I recommend manually specifying the path to the browser .exe file via ``--custom-browser-location``
--- 

# Contributing 
## Reporting Issues:
   - Use the GitHub Issues tab to report bugs or suggest features.
   - Provide detailed information about your environment and the steps to reproduce any bugs.

## Code Contributions 
   - Fork the repository and create a new branch for your feature or bug fix.
   - Follow the existing code style and conventions.
   - Submit a pull request with a clear description of your changes.

## Documentation
   - Help improve our documentation by submitting updates or clarifications.

## This project exists in its current state thanks to all the people who have contributed and to all who create issues, which we solve together!

