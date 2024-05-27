# PAT Install PodNet A Configuration
# stdlib
import ipaddress
import json
import os
import subprocess
# lib
import curses
# local
from primitives import firewall_podnet, net


SYS_NET_DIR = '/sys/class/net/'


def read_json_file(json_filepath):
    with open(json_filepath, 'r') as json_file:
        config = json.load(json_file)
    return config


def write_json_file(json_data, json_filepath):
    with open(json_filepath, 'w') as json_file:
        json.dump(json_data, json_file, indent=4)


def update_json_file(key, value, json_filepath):
    # read
    json_data = read_json_file(json_filepath)
    json_data[key] = value
    # write
    write_json_file(json_data, json_filepath)


def get_netplan_iflname(netplan_data, target_interface):
    # Navigate through the dictionary to find the 'ethernets' key
    iflname = ''
    if 'network' in netplan_data and 'ethernets' in netplan_data['network']:
        ethernets = netplan_data['network']['ethernets']
        # Iterate through each ethernet interface
        for interface_lname, interface_data in ethernets.items():
            # Check if 'set-name' is in the interface data
            if 'set-name' in interface_data and interface_data['set-name'] == target_interface:
                iflname = interface_lname
                break
    return iflname


def get_iface_operstate(name):
    with open(f'{SYS_NET_DIR}{name}/operstate') as operstate_file:
        state = operstate_file.read().strip()
    return state == 'up'


def get_iface_carrier(name):
    with open(f'{SYS_NET_DIR}{name}/carrier') as carrier_file:
        carrier = carrier_file.read().strip()
    return carrier == '1'


def get_iface_mac(name):
    with open(f'{SYS_NET_DIR}{name}/address') as file:
        mac = file.read()
    return mac


def scan_for_new_iface(excluded_ifaces):
    """
    Scan /sys/class/net/ directory for new network interface.
    Returns an new active interface name.
    """
    all_new_ifaces = [interface for interface in os.listdir(SYS_NET_DIR) if interface not in excluded_ifaces]

    new_active_iface, mac = '', None
    for name in all_new_ifaces:
        if get_iface_operstate(name) and get_iface_carrier(name):
            new_active_iface = name
            mac = get_iface_mac(name)
            break
    return new_active_iface, mac


def build(win, config_data, netplan_data):
    # 1.1 Find the `public0` interface's logical name from netplan data
    iflname = get_netplan_iflname(netplan_data, 'public0')

    # 1.2 Update config.json with `public0` interface's logical name
    config_filepath = '/etc/cloudcix/pod/configs/config.json'
    update_json_file('podnet_a_public_ifname', iflname, config_filepath)
    excluded_ifaces = ['lo', 'docker', 'public0']

    # 2 Network setup
    # 2.1.1 Connect Mgmt interface
    mgmt_iflname, mgmt_mac = '', None
    win.addstr(1, 1, '2.1.1 Connect Management interface:            ', curses.color_pair(2))
    while mgmt_iflname == '':
        # interact with user to connect new interfaces
        win.addstr(11, 1, f'Please connect the `mgmt0` interface and press ENTER.         ', curses.color_pair(2))
        win.refresh()
        user_input = win.getkey()
        while user_input != '\n':
            user_input = win.getkey()

        mgmt_iflname, mgmt_mac = scan_for_new_iface(excluded_ifaces)
        if mgmt_iflname != '':
            win.addstr(1, 1, '2.1.1 Connect Mgmt interface:         CONNECTED', curses.color_pair(4))
            win.addstr(11, 1, f'`mgmt0`:{mgmt_iflname} interface detected.                    ', curses.color_pair(4))
            win.refresh()
            break
        else:
            win.addstr(11, 1, f'`mgmt0` interface NOT detected. Try again please.....         ', curses.color_pair(3))
            win.refresh()

    # 2.1.2 Configure Mgmt interface
    # sort ipaddresses
    primary_ipv4_subnet_items = config_data['primary_ipv4_subnet'].split('/')
    ipv6_subnet_items = config_data['ipv6_subnet'].split('/')
    mgmt_ipv4 = f'{next(ipaddress.IPv4Network(config_data["primary_ipv4_subnet"]).hosts())}/{primary_ipv4_subnet_items[1]}'
    mgmt_ipv6_1 = f'{ipv6_subnet_items[0]}10:0:1/64'
    mgmt_ipv6_2 = f'{ipv6_subnet_items[0]}10:0:2/64'
    mgmt_ipv6_3 = f'{ipv6_subnet_items[0]}10:0:3/64'
    mgmt_route_to = f'{ipv6_subnet_items[0][:ipv6_subnet_items[0].rfind(":")]}d0c6::/64'
    mgmt_route_via = f'{ipv6_subnet_items[0]}4000:1'

    win.addstr(1, 1, '2.1.2 Configuring Mgmt interface:              ', curses.color_pair(2))
    win.refresh()
    configured, error = net.build(
        host='localhost',
        identifier=mgmt_iflname,
        ips=[mgmt_ipv4, mgmt_ipv6_2],
        mac=mgmt_mac,
        name='mgmt0',
        routes=[{'to': mgmt_route_to, 'via': mgmt_route_via}],
    )
    if configured is False:
        win.addstr(1, 1, '2.1.2 Configuring Mgmt interface:  FAILED      ', curses.color_pair(3))
        win.addstr(11, 1, f'Error: {error}', curses.color_pair(3))
        win.refresh()
        return
    win.addstr(1, 1, '2.1.2 Configuring Mgmt interface:  SUCCESS      ', curses.color_pair(4))
    win.refresh()

    # 2.1.3 Update the config.json file
    update_json_file('podnet_a_mgmt_ifname', mgmt_iflname, config_filepath)
    excluded_ifaces.append('mgmt0')

    # 2.2.1 Connect oob interface
    oob_iflname, oob_mac = '', None
    win.addstr(2, 1, '2.2.1 Connect OOB interface:                   ', curses.color_pair(2))
    while oob_iflname == '':
        # interact with user to connect new interfaces
        win.addstr(11, 1, f'Please connect the `oob0` interface and press ENTER.          ', curses.color_pair(2))
        win.refresh()
        user_input = win.getkey()
        while user_input != '\n':
            user_input = win.getkey()

        oob_iflname, oob_mac = scan_for_new_iface(excluded_ifaces)
        if oob_iflname != '':
            win.addstr(2, 1, '2.2.1 Connect OOB interface:         CONNECTED ', curses.color_pair(4))
            win.addstr(11, 1, f'`oob0`:{oob_iflname} interface detected.                      ', curses.color_pair(4))
            win.refresh()
            break
        else:
            win.addstr(11, 1, f'`oob0` interface NOT detected. Try again please.....          ', curses.color_pair(3))
            win.refresh()

    # 2.2.2 Configure oob interface
    # sort ipaddresses
    oob_ip = f'10.0.0.254/16'
    win.addstr(2, 1, '2.2.2 Configuring OOB interface:               ', curses.color_pair(2))
    win.refresh()
    configured, error = net.build(
        host='localhost',
        identifier=oob_iflname,
        ips=[oob_ip],
        mac=oob_mac,
        name='oob0',
        routes=[{'to': '10.0.0.0/8', 'via': '10.0.0.1'}],
    )
    if configured is False:
        win.addstr(2, 1, '2.2.2 Configuring OOB interface:  FAILED       ', curses.color_pair(3))
        win.addstr(11, 1, f'Error: {error}', curses.color_pair(3))
        win.refresh()
        return
    win.addstr(2, 1, '2.2.2 Configuring OOB interface:  SUCCESS       ', curses.color_pair(4))
    win.refresh()

    # 2.2.3 Update the config.json file
    update_json_file('podnet_a_oob_ifname', oob_iflname, config_filepath)
    excluded_ifaces.append('oob0')

    # 2.3.1 Configure private interface
    private_iflname, private_mac = '', None
    win.addstr(3, 1, '2.3.1 Connect Private interface:               ', curses.color_pair(2))
    while private_iflname == '':
        # interact with user to connect new interfaces
        win.addstr(11, 1, f'Please connect the `private0` interface and press ENTER.      ', curses.color_pair(2))
        win.refresh()
        user_input = win.getkey()
        while user_input != '\n':
            user_input = win.getkey()

        private_iflname, private_mac = scan_for_new_iface(excluded_ifaces)
        if private_iflname != '':
            win.addstr(3, 1, '2.3.1 Connect Private interface:     CONNECTED ', curses.color_pair(4))
            win.addstr(11, 1, f'`private0`:{private_iflname} interface detected.              ', curses.color_pair(4))
            win.refresh()
            break
        else:
            win.addstr(11, 1, f'`private0` interface NOT detected. Try again please.....      ', curses.color_pair(3))
            win.refresh()

    # 2.3.2 Configure Private interface
    win.addstr(3, 1, '2.3.2 Configuring Private interface:           ', curses.color_pair(2))
    win.refresh()
    configured, error = net.build(
        host='localhost',
        identifier=private_iflname,
        ips=None,
        mac=private_mac,
        name='private0',
        routes=None,
    )
    if configured is False:
        win.addstr(3, 1, '2.3.2 Configuring Private interface:  FAILED   ', curses.color_pair(3))
        win.addstr(11, 1, f'Error: {error}', curses.color_pair(3))
        win.refresh()
        return
    win.addstr(3, 1, '2.3.2 Configuring Private interface:  SUCCESS   ', curses.color_pair(4))
    win.refresh()

    # 2.3.3 Update the config.json file
    update_json_file('podnet_a_private_ifname', private_iflname, config_filepath)
    excluded_ifaces.append('private0')

    # 2.4.1 Configure inter interface
    inter_iflname, inter_mac = '', None
    win.addstr(4, 1, '2.4.1 Connect Inter interface:                 ', curses.color_pair(2))
    while inter_iflname == '':
        # interact with user to connect new interfaces
        win.addstr(11, 1, f'Please connect the `inter0` interface and press ENTER.        ', curses.color_pair(2))
        win.refresh()
        user_input = win.getkey()
        while user_input != '\n':
            user_input = win.getkey()

        inter_iflname, inter_mac = scan_for_new_iface(excluded_ifaces)
        if inter_iflname != '':
            win.addstr(4, 1, '2.4.1 Connect Inter interface:     CONNECTED   ', curses.color_pair(4))
            win.addstr(11, 1, f'`inter0`:{inter_iflname} interface detected.                  ', curses.color_pair(4))
            win.refresh()
            break
        else:
            win.addstr(11, 1, f'`inter0` interface NOT detected. Try again please.....        ', curses.color_pair(3))
            win.refresh()

    # 2.4.2 Configure Inter interface
    win.addstr(4, 1, '2.4.2 Configuring Inter interface:             ', curses.color_pair(2))
    win.refresh()
    configured, error = net.build(
        host='localhost',
        identifier=inter_iflname,
        ips=None,
        mac=inter_mac,
        name='inter0',
        routes=None,
    )
    if configured is False:
        win.addstr(4, 1, '2.4.2 Configuring Inter interface:  FAILED     ', curses.color_pair(3))
        win.addstr(11, 1, f'Error: {error}', curses.color_pair(3))
        win.refresh()
        return
    win.addstr(4, 1, '2.4.2 Configuring Inter interface:  SUCCESS     ', curses.color_pair(4))
    win.refresh()

    # 2.4.3 Update the config.json file
    update_json_file('podnet_a_inter_ifname', inter_iflname, config_filepath)
    excluded_ifaces.append('inter0')

    # 3. Firewall
    cop_nginxcop_ipv4 = f'{ipaddress.ip_address(primary_ipv4_subnet_items[0]) + 4}'
    cop_portal_ipv4 = f'{ipaddress.ip_address(primary_ipv4_subnet_items[0]) + 5}'
    cop_nginxcop_ipv6 = f'{ipv6_subnet_items[0][:-1]}d0c6::4004:a'
    cop_portal_ipv6 = f'{ipv6_subnet_items[0][:-1]}d0c6::5002:4'
    firewall_rules = [
        # 1.1 Inbound
        # 1.1.1 Ping v4
        {'order': 0, 'version': '4', 'iiface': 'public0', 'oiface': '', 'protocol': 'icmp', 'action': 'accept', 'log': False, 'source': ['any'], 'destination': ['any'], 'port': []},
        # 1.1.2 Ping v6
        {'order': 1, 'version': '6', 'iiface': 'public0', 'oiface': '', 'protocol': 'icmp', 'action': 'accept', 'log': False, 'source': ['any'], 'destination': ['any'], 'port': []},
        # 1.1.3 DNS v4
        {'order': 2, 'version': '4', 'iiface': 'public0', 'oiface': '', 'protocol': 'dns', 'action': 'accept', 'log': False, 'source': ['any'], 'destination': ['any'], 'port': []},
        # 1.1.4 DNS v6
        {'order': 3, 'version': '6', 'iiface': 'public0', 'oiface': '', 'protocol': 'dns', 'action': 'accept', 'log': False, 'source': ['any'], 'destination': ['any'], 'port': []},
        # 1.1.5 SSH to Mgmt Interface by Robot
        {'order': 4, 'version': '6', 'iiface': 'mgmt0', 'oiface': '', 'protocol': 'tcp', 'action': 'accept', 'log': True, 'source': [mgmt_ipv6_1, mgmt_ipv6_2, mgmt_ipv6_3], 'destination': ['any'], 'port': ['22']},
        # 1.1.6 SSH to OOB Interface by PAT
        {'order': 5, 'version': '4', 'iiface': 'oob0', 'oiface': '', 'protocol': 'tcp', 'action': 'accept', 'log': True, 'source': ['192.168.2.0/23'], 'destination': ['any'], 'port': ['22']},
        # 1.1.7 VPN on Public interface since it has Region in blend
        {'order': 6, 'version': '4', 'iiface': 'public0', 'oiface': '', 'protocol': 'vpn', 'action': 'accept', 'log': True, 'source': ['any'], 'destination': ['any'], 'port': []},

        # 2.1 Forward
        # 2.1.1 DNS v4 TCP/UDP port 53 From Public to Mgmt
        {'order': 7, 'version': '4', 'iiface': 'public0', 'oiface': 'mgmt0', 'protocol': 'dns', 'action': 'accept', 'log': False, 'source': ['any'], 'destination': ['any'], 'port': []},
        # 2.1.2 DNS v6 TCP/UDP port 53 From Public to Mgmt
        {'order': 8, 'version': '6', 'iiface': 'public0', 'oiface': 'mgmt0', 'protocol': 'dns', 'action': 'accept', 'log': False, 'source': ['any'], 'destination': ['any'], 'port': []},
        # 2.1.3 DNS v4 TCP/UDP port 53 From Public to Private
        {'order': 9, 'version': '4', 'iiface': 'public0', 'oiface': 'private0', 'protocol': 'dns', 'action': 'accept', 'log': False, 'source': ['any'], 'destination': ['any'], 'port': []},
        # 2.1.4 DNS v6 TCP/UDP port 53 From Public to Private
        {'order': 10, 'version': '6', 'iiface': 'public0', 'oiface': 'private0', 'protocol': 'dns', 'action': 'accept', 'log': False, 'source': ['any'], 'destination': ['any'], 'port': []},
        # 2.1.5 VPN Public to Private since it has Region in blend
        {'order': 11, 'version': '4', 'iiface': 'public0', 'oiface': 'private0', 'protocol': 'vpn', 'action': 'accept', 'log': True, 'source': ['any'], 'destination': ['any'], 'port': []},
        # 2.1.6 Mgmt Outbound v4
        {'order': 12, 'version': '4', 'iiface': 'mgmt0', 'oiface': 'public0', 'protocol': 'any', 'action': 'accept', 'log': True, 'source': ['any'], 'destination': ['any'], 'port': []},
        # 2.1.7 Mgmt Outbound v6
        {'order': 13, 'version': '6', 'iiface': 'mgmt0', 'oiface': 'public0', 'protocol': 'any', 'action': 'accept', 'log': True, 'source': ['any'], 'destination': ['any'], 'port': []},
        # 2.1.8 Private Outbound v4
        {'order': 14, 'version': '4', 'iiface': 'private0', 'oiface': 'public0', 'protocol': 'any', 'action': 'accept', 'log': True, 'source': ['any'], 'destination': ['any'], 'port': []},
        # 2.1.9 Private Outbound v6
        {'order': 15, 'version': '6', 'iiface': 'private0', 'oiface': 'public0', 'protocol': 'any', 'action': 'accept', 'log': True, 'source': ['any'], 'destination': ['any'], 'port': []},

        # 2.2 Mgmt Specific Forward
        # 2.2.1 Ping v4
        {'order': 16, 'version': '4', 'iiface': 'public0', 'oiface': 'mgmt0', 'protocol': 'icmp', 'action': 'accept', 'log': False, 'source': ['any'], 'destination': ['any'], 'port': []},
        # 2.2.2 Ping v6
        {'order': 17, 'version': '6', 'iiface': 'public0', 'oiface': 'mgmt0', 'protocol': 'icmp', 'action': 'accept', 'log': False, 'source': ['any'], 'destination': ['any'], 'port': []},
        # 2.2.3 COP nginx and portal v4 443
        {'order': 18, 'version': '4', 'iiface': 'public0', 'oiface': 'mgmt0', 'protocol': 'tcp', 'action': 'accept', 'log': False, 'source': ['any'], 'destination': [cop_nginxcop_ipv4, cop_portal_ipv4], 'port': ['443']},
        # 2.2.4 COP nginx and portal v6 443
        {'order': 19, 'version': '6', 'iiface': 'public0', 'oiface': 'mgmt0', 'protocol': 'tcp', 'action': 'accept', 'log': False, 'source': ['any'], 'destination': [cop_nginxcop_ipv6, cop_portal_ipv6], 'port': ['443']},

        # 3.1.1 Outbound allow all v4
        {'order': 20, 'version': '4', 'iiface': '', 'oiface': 'public0', 'protocol': 'any', 'action': 'accept', 'log': False, 'source': ['any'], 'destination': ['any'], 'port': []},
        # 3.1.2 Outbound allow all v4
        {'order': 21, 'version': '6', 'iiface': '', 'oiface': 'public0', 'protocol': 'any', 'action': 'accept', 'log': False, 'source': ['any'], 'destination': ['any'], 'port': []},

    ]
    win.addstr(5, 1, '3.1 Configuring Firewall Rules:                ', curses.color_pair(2))
    win.refresh()
    configured, error = firewall_podnet.build(
        firewall_rules=firewall_rules,
        log_setup=None,
    )
    if configured is False:
        win.addstr(5, 1, '3.1 Configuring Firewall Rules:  FAILED        ', curses.color_pair(3))
        win.addstr(11, 1, f'Error: {error}', curses.color_pair(3))
        win.refresh()
        return
    win.addstr(5, 1, '3.1 Configuring Firewall Rules:  SUCCESS       ', curses.color_pair(4))
    win.refresh()

    # RoboSOC setup
    win.addstr(6, 1, '4.1 RoboSOC Setup:                                 ', curses.color_pair(2))
    # set the /etc/cloudcix/pod/pod_installer/robosoc.py file to executable ie to +x
    try:
        subprocess.run(['sudo', 'chmod', '+x', '/etc/cloudcix/pod/pod_installer/robosoc.py'], check=True)
    except subprocess.CalledProcessError as error:
        win.addstr(6, 1, '4.1 RoboSOC Setup:  FAILED                         ', curses.color_pair(3))
        win.addstr(11, 1, f'Error: {error}', curses.color_pair(3))
        win.refresh()
        return

    # creating robosoc cron job file
    with open('/etc/cron.d/robosoc', 'w') as file:
        file.write('*/15 * * * * root /etc/cloudcix/pod/pod_installer/robosoc.py > /dev/null 2>&1 \n')
    # for cron job file, file must be executable so set to +x
    try:
        subprocess.run(['sudo', 'chmod', '+x', '/etc/cron.d/robosoc'], check=True)
    except subprocess.CalledProcessError as error:
        win.addstr(6, 1, '4.1 RoboSOC Setup:  FAILED                         ', curses.color_pair(3))
        win.addstr(11, 1, f'Error: {error}', curses.color_pair(3))
        win.refresh()
    win.addstr(6, 1, '4.1 RoboSOC Setup:  SUCCESS                        ', curses.color_pair(2))
    win.refresh()

    # Finish
    return
