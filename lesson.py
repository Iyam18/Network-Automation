from flask import Flask, render_template, request
from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoAuthenticationException


app = Flask(__name__)

DEFAULT_DEVICE = {
    "device_type": "cisco_ios_telnet",
    "ip": "192.168.10.114",
    "port": 32770,
    "username": "",
    "password": "",
    "secret": "",
}

COMMANDS = [
    ("show_version", "show version"),
    ("interfaces", "show ip interface brief"),
    ("running_config", "show running-config"),
]


@app.route("/", methods=["GET", "POST"])
def index():
    results = {}
    error = None
    device = DEFAULT_DEVICE.copy()
    selected_commands = [command for _, command in COMMANDS]

    if request.method == "POST":
        try:
            port = int(request.form.get("port", device["port"]) or device["port"])
        except ValueError:
            error = "Port must be a valid number."
            port = device["port"]

        device.update({
            "ip": request.form.get("ip", device["ip"]).strip(),
            "port": port,
            "username": request.form.get("username", device["username"]).strip(),
            "password": request.form.get("password", device["password"]),
            "secret": request.form.get("secret", device["secret"]),
        })
        selected_commands = [
            command
            for key, command in COMMANDS
            if request.form.get(key) == "on"
        ]

        if error is not None:
            pass
        elif not selected_commands:
            error = "Select at least one command."
        else:
            net_connect = None
            try:
                net_connect = ConnectHandler(**device)
                net_connect.enable()
                for command in selected_commands:
                    results[command] = net_connect.send_command(command)
            except NetmikoAuthenticationException:
                error = "Router rejected the login. Check the username and password used in this form."
            except Exception as exc:
                error = f"Connection failed: {exc}"
            finally:
                if net_connect is not None:
                    net_connect.disconnect()

    return render_template(
        "index.html",
        device=device,
        results=results,
        error=error,
        commands=COMMANDS,
        selected_commands=selected_commands,
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)