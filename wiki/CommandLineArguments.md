# All command line arguments
------------------------------------------------------------------------------------------------------------------------------------

# Required
### Browsers
> Need to enter only one argument from this group!!!

| Argument Command      |                                           Description                                                      |
| --------------------- | ---------------------------------------------------------------------------------------------------------- |
| --chrome              | Launching the project via Google Chrome browser                                                            |
| --firefox             | Launching the project via Mozilla Firefox browser                                                          |
| --edge                | Launching the project via Microsoft Edge browser                                                           |

### Modes of operation
> Need to enter only one argument from this group!!!

| Argument Command      |                                           Description                                                      |
| --------------------- | ---------------------------------------------------------------------------------------------------------- |
| --key | Creating a license key for ESET Smart Security Premium                                                                     |
| --small-business-key  | Creating a license key for ESET Small Business Security (1 key - 5 devices)                                |
| --advanced-key        | Creating a license key for ESET PROTECT Advanced (1 key - 25 devices) - works only with ```mailticking```, ```fakemail``` and ```--custom-email-api``` |
| --vpn-codes           | Creating 10 codes for ESET VPN + 1 ESET Small Business Security key                                        |
| --account             | Creating an ESET HOME Account (To activate the free trial version)                                         |
| --protecthub-account  | Creating a ESET ProtectHub Account (To activate the free trial version) - works only with ```mailticking```, ```fakemail``` and ```--custom-email-api``` |
| --only-webdriver-update | Updates/installs webdrivers and browsers without generating accounts and license keys                    |
| --update         | Switching to program update mode - **Overrides all arguments that are available**                               |
| --reset-eset-vpn | Trying to reset the license in the ESET VPN application (Windows & macOS only) - **Overrides all arguments that are available** |
--------------------------------------------------------------------------------------------------------------------------------------

# Optional
|          Argument Command          |                                                             Description                                                              |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| --skip-update-check                | Skips checking for program updates                                                                                                   |
| --skip-webdriver-menu              | Skips installation/upgrade webdrivers through the my custom wrapper (The built-in selenium-manager will be used)                     |
| --no-headless                      | Shows the browser at runtime (The browser is hidden by default, but on (Windows 7) and (enabled --business-key or --business-account options) this option is enabled by itself) |
| --custom-browser-location {string} | Set path to the custom browser (to the binary file, useful when using non-standard releases, for example: Firefox Developer Edition, Brave) |
| --email-api {1secmail, guerrillamail, developermail, mailticking, fakemail} | Specify which api to use for mail, default - ```developermail``` |
| --custom-email-api | Allows you to manually specify any email, and all work will go through it - **Requires manually read inbox and do what is described in the documentation for this argument!!!**, **Also use this argument if you are unable to generate anything using all the implemented email APIs above** |
| --no-logo              | Replaces ASCII-Art with plain text |
| --disable-progress-bar | Disables the webdriver download progress bar |
| --disable-output-file  | Disables the output txt file generation |
| --repeat {number}      | Specifies how many times to repeat generation (**Accepts numbers from 1 to 10**)|