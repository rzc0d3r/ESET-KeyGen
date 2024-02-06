# All command line arguments

| Argument Command      | Default  |                                          Description                                                    |
| --------------------- | -------- | ------------------------------------------------------------------------------------------------------  |
| --account             | disabled | Generates an account instead of a key                                                                   |
| --firefox             | disabled | Launching the project via Firefox browser (Runs through the Google Chrome browser by default)           |
| --edge                | disabled | Launching the project via Microsoft Edge browser (Runs through the Google Chrome browser by default)    |
| --skip-webdriver-menu | disabled | Skips installation/upgrade webdrivers through the my custom wrapper (By default, everything should be done automatically through selenium-manager) |
| --no-headless         | disabled | Shows the browser at runtime (by default hides the browser at runtime)                                  |
| --force               | disabled | Disables all user input, but waiting for the Enter key to be pressed before exiting the program remains |
| --cli                 | disabled | Disables all user input (GitHub CI Requirements)                                                        |
| --only-update         | disabled | Updates / installs webdrivers and browsers without generating account and keys
