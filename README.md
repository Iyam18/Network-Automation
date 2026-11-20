# Network Automation

A small Flask dashboard for running read-only diagnostics against a Cisco IOS router with Netmiko.

## Requirements

- Python 3.10 or later
- A reachable Cisco IOS Telnet console

## Run on Windows

Open PowerShell in this folder and run:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python lesson.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

The dashboard defaults to the lab console at `192.168.10.114:32770`. Update the target in the form if your EVE-NG console uses a different address or port. Leave the login fields blank when the router console does not request credentials. The app enters enable mode before running selected `show` commands.

To run the command-line collector instead:

```powershell
python api.py
```

## Safety

Do not commit router passwords, enable secrets, tokens, or other credentials. Use the dashboard fields for credentials, and keep local environment/configuration files out of version control.
