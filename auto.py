import os
from cryptography.fernet import Fernet
import yaml
from netmiko import ConnectHandler



#FUNCTIONS:
#-------------------------------------------------------------------------------------
# Check if secret.key exists and creates one if it doesn't
#-------------------------------------------------------------------------------------
def genKey(key_file_path = "secret.key"):
    if not os.path.exists(key_file_path):
        key = Fernet.generate_key()
        with open(key_file_path, "wb") as key_file:
            key_file.write(key)
        print("New encryption key generated and saved to secret.key. Keep it safe!")
    else:
        print("Encryption key already exists.")
#-------------------------------------------------------------------------------------
# Encrypt Passwords using secret.key:
#-------------------------------------------------------------------------------------       
def encrypt_passwords(key_file_path = "secret.key", config_file_path = "config.yaml"):
    # Load encryption key
    with open(key_file_path, "rb") as key_file:
        key = key_file.read()
    cipher = Fernet(key)

    # Encrypt passwords and update the YAML file
    with open(config_file_path, "r") as file:
        devices_data = yaml.safe_load(file)

    for device in devices_data["devices"].values():
        encrypted_password = cipher.encrypt(device["password"].encode()).decode()
        encrypted_secret = cipher.encrypt(device["secret"].encode()).decode()
        device["password"] = encrypted_password
        device["secret"] = encrypted_secret

    # Save encrypted passwords back to YAML
    with open(config_file_path, "w") as file:
        yaml.dump(devices_data, file, default_flow_style=False)

    print("Passwords encrypted and saved in config.yaml!")
#-------------------------------------------------------------------------------------
# Configure Cisco devices with Netmiko
#-------------------------------------------------------------------------------------
def config_syslog_cisco(key_file_path = "secret.key", config_file_path = "config.yaml"):
    # Load encryption key
    with open(key_file_path, "rb") as key_file:
        key = key_file.read()
    cipher = Fernet(key)

    # Load device details from YAML
    with open(config_file_path, "r") as file:
        devices_data = yaml.safe_load(file)

    # Decrypt passwords before use
    for device in devices_data["devices"].values():
        device["password"] = cipher.decrypt(device["password"].encode()).decode()
        #print(device["password"])
        device["secret"] = cipher.decrypt(device["secret"].encode()).decode()
        #print(device["secret"])

    syslog_server_ip = devices_data['syslog_server']['ip']
    

    # Iterate through each device and print it as a dictionary
    for device_name, device_info in devices_data["devices"].items():
        #print(f"{device_info}")  # Prints each device's name and its dictionary
        if device_info['device_type'] == 'cisco_ios':
            logging_command = [
                f"logging {syslog_server_ip}",
                ]
            print(f"Configuring syslog on: {device_name}")
            net_connect = ConnectHandler(**device_info)
            net_connect.enable()
            net_connect.send_config_set(logging_command)
            output = net_connect.send_command("write memory", expect_string=r"#")

            #output = net_connect.send_command("show logging")
            print(output)

            net_connect.disconnect()
        else:
            print(f"{device_info['device_type']} - Vendor is not Cisco, Skipping device")

if __name__ == "__main__":
    #genKey()
    #encrypt_passwords()
    config_syslog_cisco()