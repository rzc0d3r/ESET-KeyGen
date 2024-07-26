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
| --key | Generating an ESET-HOME license key (example as AGNV-XA2V-EA89-U546-UVJP) |
| --account             | Generating an ESET HOME Account (To activate the free trial version)                              |
| --business-account | Generating an ESET BUSINESS Account (To huge businesses) - **Requires manual captcha input!!!**   |
| --business-key | Generating an ESET BUSINESS Account and creating a universal license key for ESET products (1 key - 75 devices) - **Requires manual captcha input!!!** |
| --only-webdriver-update         | Updates/installs webdrivers and browsers without generating accounts and license keys |
| --update         | Switching to program update mode - **Overrides all arguments that are available** |
--------------------------------------------------------------------------------------------------------------------------------------

# Optional
|          Argument Command          |                                                             Description                                                              |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| --skip-update-check                | Skips checking for program updates                                                                                                   |
| --skip-webdriver-menu              | Skips installation/upgrade webdrivers through the my custom wrapper (The built-in selenium-manager will be used)                     |
| --no-headless                      | Shows the browser at runtime (The browser is hidden by default, but on (Windows 7) and (enabled --business-key or --business-account options) this option is enabled by itself) |
| --custom-browser-location {string} | Set path to the custom browser (to the binary file, useful when using non-standard releases, for example: Firefox Developer Edition, Brave) |
| --email-api {1secmail, hi2in, 10minutemail, tempmail, guerrillamail, developermail} | Specify which api to use for mail, default - developermail |
| --custom-email-api | Allows you to manually specify any email, and all work will go through it - **Requires manually read inbox and do what is described in the documentation for this argument!!!**, **Also use this argument if you are unable to generate anything using all the implemented email APIs above** |
| --no-logo          | Replaces ASCII-Art with plain text |