from echobox.tool import system

def open_firewall_port(port, protocol):
    os_name = system.get_os_name()
    if os_name == 'windows':
        command = f'netsh advfirewall firewall add rule name="Open Port {port}" dir=in action=allow protocol={protocol.upper()} localport={port}'
    elif os_name == 'linux':
        command = f'firewall-cmd --permanent --add-port={port}/{protocol} && firewall-cmd --reload'
    else:
        raise Exception(f"Unsupported OS: {os_name}")

    system.shell_run(command)

def close_firewall_port(port, protocol):
    os_name = system.get_os_name()
    if os_name == 'windows':
        command = f'netsh advfirewall firewall delete rule name="Open Port {port}" protocol={protocol.upper()} localport={port}'
    elif os_name == 'linux':
        command = f'firewall-cmd --permanent --remove-port={port}/{protocol} && firewall-cmd --reload'
    else:
        raise Exception(f"Unsupported OS: {os_name}")

    system.shell_run(command)
