# Syslog Server and Device Configuration Project

This repository provides a solution for configuring Cisco devices to send syslog messages to a central server, storing them in a database, and offering a web interface for viewing logs. It includes encryption functionality to secure sensitive information such as device passwords.

## Files Overview

### `auto.py`
This Python script automates the encryption of device passwords and configures Cisco devices to send syslog messages to a server.

#### Key Functions:
- **`genKey()`**: Generates and saves an encryption key (`secret.key`) if one doesn't already exist.
- **`encrypt_passwords()`**: Encrypts device passwords and secrets stored in a YAML configuration file.
- **`config_syslog_cisco()`**: Configures Cisco devices to send syslog messages to a specified syslog server IP address, using the encrypted passwords for authentication.

### `config.yaml`
A configuration file that stores device connection details (IP, username, password, etc.) and the syslog server's IP address. The passwords and secrets in this file are encrypted by `auto.py`.

Example content:
```yaml
devices:
  R1:
    device_type: cisco_ios
    host: 192.168.100.2
    password: <encrypted_password>
    port: 22
    secret: <encrypted_secret>
    username: admin

syslog_server:
  ip: 192.168.100.10
```

### `syslog_server.py`
A simple syslog server that listens for syslog messages from network devices and stores them in a SQLite database. It parses incoming log messages, extracts useful information, and saves it for later viewing.

#### Key Functions:
- **`create_db()`**: Creates an SQLite database (`syslogs.db`) and a table for storing logs if they don't already exist.
- **`insert_log()`**: Inserts parsed syslog log entries into the database.
- **`parse_log()`**: Parses syslog messages to extract timestamp, severity, identifier, and message content.
- **`syslog_server()`**: Main function to run the syslog server, receive log messages, and save them in the database.

### `verify_logs.py`
This script queries the SQLite database to verify and display the logs stored by the syslog server. It fetches all logs from the `logs` table and prints them in a readable format.

### `app.py`
A Flask web application to display logs stored in the SQLite database through a web interface.

#### Key Features:
- **`get_logs()`**: Retrieves logs from the SQLite database, ordered by the latest entries.
- **`home()`**: Renders a template (`logs.html`) to display the logs on the web page.

---

## Prerequisites

- Python 3.x
- Flask (`pip install Flask`)
- SQLite3 (usually pre-installed with Python)
- `cryptography` library (`pip install cryptography`)
- `pyyaml` library (`pip install pyyaml`)
- `netmiko` library (`pip install netmiko`)

## Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/syslog-server.git
   cd syslog-server
   ```

2. **Generate the Encryption Key**:
   Run `auto.py` to generate a new encryption key if one doesn't already exist:
   ```bash
   python auto.py
   ```

3. **Encrypt Passwords**:
   Run `auto.py` to encrypt the passwords and secrets in `config.yaml`:
   ```bash
   python auto.py
   ```

4. **Start the Syslog Server**:
   Run `syslog_server.py` to start listening for syslog messages:
   ```bash
   python syslog_server.py
   ```

5. **Start the Web Application**:
   Run `app.py` to launch the web application:
   ```bash
   python app.py
   ```
   The web app will be available at `http://localhost:5000`.

## Usage

- **Configuring Cisco Devices**: Ensure your devices are set to send syslog messages to the specified IP address in the `config.yaml` file.
- **Viewing Logs**: Visit the web interface at `http://localhost:5000` to view logs received by the syslog server.
- **Verifying Logs**: Use `verify_logs.py` to check the logs stored in the SQLite database.