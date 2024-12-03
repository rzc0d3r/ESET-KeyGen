import os
import winreg as reg

def resetvpn (key_path, value_name):
    """Deletes the authHash value of VPN."""

    # Step 1: Kill the process
    os.system("taskkill /f /im esetvpn.exe")

    # Step 2: Delete the registry key

    try:
        with reg.OpenKey(reg.HKEY_CURRENT_USER, key_path, 0, reg.KEY_ALL_ACCESS) as key:
            reg.DeleteValue(key, value_name)
        print(f"Successfully deleted value: {value_name} from {key_path}")
        print(f"VPN Reset Successful!")
    except FileNotFoundError:
        print(f"The registry value or key does not exist: {key_path}\\{value_name}")
    except PermissionError:
        print(f"Permission denied while accessing: {key_path}\\{value_name}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Main script
if __name__ == "__main__":

    registry_key_path = r"SOFTWARE\ESET\ESET VPN"
    registry_value_name = "authHash"

    resetvpn(registry_key_path, registry_value_name)
