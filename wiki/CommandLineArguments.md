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
| --key                 | Generating an antivirus license key                                                                        |
| --account             | Generating an antivirus account                                                                            |

--------------------------------------------------------------------------------------------------------------------------------------

# Optional
|          Argument Command          |                                                             Description                                                              |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| --skip-webdriver-menu              | Skips installation/upgrade webdrivers through the my custom wrapper (The built-in selenium-manager will be used)                     |
| --no-headless                      | Shows the browser at runtime (The browser is hidden by default, but on Windows 7 this option is enabled by itself)                   |
| --force                            | Disables all user input, but waiting for the Enter key to be pressed before exiting the program remains                              |
| --cli                              | Disables all user input (GitHub CI Requirements)                                                                                     |
| --only-update                      | Updates/installs webdrivers and browsers without generating account and license key                                                 |
| --custom-browser-location {string} | Set path to the custom browser (to the binary file, useful when using non-standard releases, for example, Firefox Developer Edition) |