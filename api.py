from netmiko import ConnectHandler


ROUTER_DEVICE = {
    "device_type": "cisco_ios_telnet",
    "ip": "192.168.10.114",
    "port": 32770,
    "username": "",
    "password": "",
    "secret": "",
}

COMMANDS_TO_RUN = [
    "show version",
    "show ip interface brief",
    "show running-config",
]


def collect_router_data():
    net_connect = None
    results = {}

    try:
        print("Connecting to the router...")
        net_connect = ConnectHandler(**ROUTER_DEVICE)
        net_connect.enable()

        for command in COMMANDS_TO_RUN:
            print(f"\n--- Output of '{command}': ---")
            results[command] = net_connect.send_command(command)
            print(results[command])
    except Exception as exc:
        print(f"An error occurred: {exc}")
    finally:
        if net_connect is not None:
            net_connect.disconnect()

    return results


if __name__ == "__main__":
    collect_router_data()