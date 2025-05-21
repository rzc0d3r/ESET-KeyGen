# MBCI (Menu-based Сonsole Interface)

### If you start the project without specifying arguments it will start in MBCI mode. In this mode you can interact with the startup settings

---

## The first thing that greets you is the Main Menu, which currently has 3 items:

![Windows](https://github.com/rzc0d3r/ESET-KeyGen/blob/main/img/main_menu.png)

1. Settings
2. Start
3. Exit

* **Settings** - this is under the startup settings menu
* **Start** - launches the program 
* **Exit** - obviously closes the program

> To select the desired item, enter its number from the list after and press Enter.

> The default setting is ```--auto-detect-browser --key --email-api guerrillamail --proxy-file proxies.txt``` so that when you start the program you can immediately select **Start** and you will generate your ESET HOME key through the chrome browser

---

## Description of the Settings menu:

![Windows](https://github.com/rzc0d3r/ESET-KeyGen/blob/main/img/default_settings_menu.png)

Here you are greeted by a menu consisting of items (they're from [CommandLineArguments.md](https://github.com/rzc0d3r/ESET-KeyGen/blob/main/wiki/CommandLineArguments.md)):

* Arguments that have a signature **(selected: ___)** expect you to select from a list that opens when you select the corresponding item
* Arguments with a caption **(saved: ___)** expect you to enter data, the input field will be available when the corresponding item is selected (If you enter a **file path**, remove the **quotation marks!!!**)
* Arguments that have a signature **(disabled/enabled)** expect you to simply select them by pressing Enter. They will change their state when you reselect them.

* Obviously, **Back** is going to take you back to the past menu...

#### Menu Demonstration

![Windows](https://github.com/rzc0d3r/ESET-KeyGen/blob/main/img/custom_settings_menu.png)

### After customization you should go back to the _Main Menu_ and click on _Start_

---

# MBCI Config

* Starting with ```v1.5.4.0```, the settings are stored in the ```eset-keygen-config.json``` file (it is always located in the folder where the program is located)
* They will be loaded each time you run the program in ```MBCI mode```
* If the config is corrupted in any way, the program will notify you and the config will be reset for recovery, so follow all the rules described in [CommandLineArguments.md](https://github.com/rzc0d3r/ESET-KeyGen/blob/main/wiki/CommandLineArguments.md)