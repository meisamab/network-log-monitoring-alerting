# 🔒 Network Log Monitoring & Alerting System

A complete Python-based solution for configuring Cisco devices to send syslog messages to a central server, storing them in a database, and offering both CLI and web-based interfaces to monitor and verify logs securely.

---

## 🧩 Features

- Automatically configures Cisco devices to send syslogs  
- Encrypts device credentials with AES key  
- Receives and parses syslog messages via UDP  
- Stores logs in SQLite database  
- Real-time web UI with Flask  
- CLI verification tool  

---

## 📁 Files Overview

### [`auto.py`](./auto.py)
Automates:
- `genKey()` – generate encryption key (`secret.key`)
- `encrypt_passwords()` – encrypts credentials in `config.yaml`
- `config_syslog_cisco()` – configures Cisco for syslog

### [`config.yaml`](./config.yaml)
Stores encrypted credentials & syslog server IP

#### 📄 Example:
```yaml
devices:
  R1:
    host: 192.168.100.2
    username: admin
    password: <encrypted>
    secret: <encrypted>

syslog_server:
  ip: 192.168.100.10
```

### [`syslog_server.py`](./syslog_server.py)
Listens to syslog messages and logs to `syslogs.db`
- `create_db()`, `parse_log()`, `insert_log()`, `syslog_server()`

### [`verify_logs.py`](./verify_logs.py)
CLI tool to query and display stored logs.

### [`app.py`](./app.py)
Flask web app showing logs in browser (`logs.html`)

---

## 📦 Prerequisites

- Python 3.x  
- Flask (`pip install flask`)  
- SQLite3  
- cryptography (`pip install cryptography`)  
- pyyaml (`pip install pyyaml`)  
- netmiko (`pip install netmiko`)  

---

## ⚙️ Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/meisamab/network-log-monitoring-alerting.git
   cd network-log-monitoring-alerting
   ```

2. **Generate the encryption key**
   ```bash
   python auto.py
   ```

3. **Encrypt the credentials**
   ```bash
   python auto.py
   ```

4. **Start the syslog server**
   ```bash
   python syslog_server.py
   ```

5. **Launch the web application**
   ```bash
   python app.py
   ```
   Access logs at: [http://localhost:5000](http://localhost:5000)

---

## 🛠️ Usage

- **Configure Cisco devices** to send syslogs to IP in `config.yaml`  
- **View logs** on web interface at `http://localhost:5000`  
- **Verify logs** in terminal using:
  ```bash
  python verify_logs.py
  ```

---

## 👤 Author

**Meisam Aboutorabian**  
📍 Toronto  
✉️ meisam.ab34@gmail.com  
🔗 [linkedin.com/in/meisamab](https://linkedin.com/in/meisamab)

> 🛡️ Developed as part of a final-year capstone project focused on real-time network log monitoring, automation, and security.
