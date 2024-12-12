# Updater

<details>
<summary>Up-to-date documentation</summary>

Each time you run the program, it checks for updates, if there is a newer version than the current one, the update system will notify you by offering to update the program: enter ```Y``` to accept and ```N``` to decline (to disable this check, use the ```--skip-update-check``` argument)

You can also update the program with the ```--update``` argument, the logic is identical, except that you don't have to type anything.

---

### At this moment, the update system can run in several modes:
1. **[NEW]** Run from under the executable - the update system will replace the current executable with the updated executable.
2. Run from source code on a system for which there are executables - the logic is the same as in the first case, but the updated executable is placed next to the source code.
3. Run from source code on a system for which there are no executables - the update system will download and unpack the source code of the latest version.

---

# NOTES
1. Make sure you run the program with elevated permissions, and also do not abort the update if you are running it, as this will corrupt the executable and you will have to manually load the executable!!!
2. In 3 method, critical errors may occur due to the existence of folders with the same name. You can ignore this error, the update program will continue its work. You will just get a folder with a different name (it will not be as nice as the one the update system wanted to make)

---
## The new version is a modification of the old one made by [rzc0d3r](https://github.com/rzc0d3r) and [AdityaGarg8](https://github.com/AdityaGarg8)
</details>

<details>
<summary>Old version of documentation</summary>

# How to use

You can update the program to the latest version by calling it with the command line argument ```--update```:

### Update when a binary file is available
![Windows](https://github.com/rzc0d3r/ESET-KeyGen/blob/main/img/updater_binary_update.png)

### Update when no binary file is available
![Windows](https://github.com/rzc0d3r/ESET-KeyGen/blob/main/img/updater_src_update.png)

Then the program itself will find the latest version and load it into the project folder.

> The upgrade program doesn't replace the files itself, because it's all in your hands!!!

> You can just copy the new folder or binary file to the right place and delete the old one!!!

---

### Also added to all this is the ```--skip-update-check``` command line argument, which disables checking for updates when you start the program
#### Without this argument, the program will always notify you when an update is available

#### Notification when an update is available
![Windows](https://github.com/rzc0d3r/ESET-KeyGen/blob/main/img/updater_available.png)

#### Notification when a project is updated to the latest version
![Windows](https://github.com/rzc0d3r/ESET-KeyGen/blob/main/img/updater_uptodate.png)

---

# NOTES
1. If you see an **[ ERROR ] Your IP address has been blocked. try again later or use a VPN!**, you have run the program very often. If you don't want to update yet use the ```--skip-update-check``` argument. This way you will disable this error!
2. If you are using a system not supported by the project. The updater will always download the source code (You use it anyway, since there are no binaries for your system **:)** )
3. Also, the command line argument ```--update``` disables all other arguments. So just running the project with one ```--update``` argument will be enough for the update!

---
## This technology exists in its current form because of [Xoncia](https://github.com/Xoncia)
</details>
