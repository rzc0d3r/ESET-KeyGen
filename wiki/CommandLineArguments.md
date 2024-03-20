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
| --key | Generating an ESET-HOME license key (example as AGNV-XA2V-EA89-U546-UVJP)|
| --account             | Generating an ESET HOME Account (To activate the free trial version)                              |
| --small-business-account                 | Generating an ESET Small Business Security Account (example as TRIAL-0420483498 : pta3b2e3h8) - **NOW DISABLED** |
| --business-account | Generating an ESET BUSINESS Account (To huge businesses) - **Requires manual captcha input!!!**   |
| --business-key | Generating an ESET BUSINESS Account and creating a universal license key for ESET products (1 key - 75 devices) - **Requires manual captcha input!!!** |
| --only-update         | Updates/installs webdrivers and browsers without generating accounts and license keys    
--------------------------------------------------------------------------------------------------------------------------------------

# Optional
|          Argument Command          |                                                             Description                                                              |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| --skip-webdriver-menu              | Skips installation/upgrade webdrivers through the my custom wrapper (The built-in selenium-manager will be used)                     |
| --no-headless                      | Shows the browser at runtime (The browser is hidden by default, but on (Windows 7) and (enabled --business-key or --business-account options) this option is enabled by itself)                   |
| --custom-browser-location {string} | Set path to the custom browser (to the binary file, useful when using non-standard releases, for example, Firefox Developer Edition) |
| --debug | Enables debugging mode, thus saving everything the developer needs to the log file (esetkg-js.log, esetkg-email.log) |
| --email-api {1secmail, hi2in, 10minutemail} | Specify which api to use for mail, default - 1secmail |
| --custom-email-api | Allows you to manually specify any email, and all work will go through it - **Requires manually read inbox and do what is described in the documentation for this argument!!!**, **Also use this argument if you are unable to generate anything using all the implemented email APIs above**|