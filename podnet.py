!#/usr/bin/python3
import ipaddress
import json
import os
import subprocess
from jinja2 import Template
from tabulate import tabulate

# Netplan ethernet defination template string
template_str = """
    # {{ iface['name'] }} Interface
    {{ iface['ifname'] }}:
      match:
        macaddress: {{ iface['mac'] }}
      set-name: {{ iface['name'] }}
      dhcp4: false
      dhcp6: false
      accept-ra: no
{%- if iface['ips']|length >0 %}
      addresses:
{%- for ip in iface['ips'] %}
        - {{ ip }}
{%- endfor %}
{%- endif %}
{%- if iface['routes']|length >0 %}
      routes:
{%- for route in iface['routes'] %}
        - to: {{ route['to'] }}
          via: {{ route['via'] }}
{%- endfor %}
{% endif %}

"""

# Create a Jinja template
template = Template(template_str)


def read_config_file():
    # Load Config json file
    with open('/etc/cloudcix/pod/configs/config.json', 'r') as config_file:
        config_data = json.load(config_file)
    return config_data


def write_config_file(config_data):
    # Load Config json file
    with open('/etc/cloudcix/pod/configs/config.json', 'w') as config_file:
        json.dump(config_data, config_file, indent=4)


def update_config_file(key, value):
    # read
    config_data = read_config_file()
    config_data[key] = value
    # write
    write_config_file(config_data)


def get_iface_altname(name):
    cmd = f"ip link show {name} | grep 'altname' | awk '{{print $2}}'"
    return os.popen(cmd).read().strip()


def get_iface_operstate(name):
    with open(f'/sys/class/net/{name}/operstate') as operstate_file:
        state = operstate_file.read().strip()
    return state == 'up'


def get_iface_carrier(name):
    with open(f'/sys/class/net/{name}/carrier') as carrier_file:
        carrier = carrier_file.read().strip()
    return carrier == '1'


def render_and_apply_netplan_config(iface):
    rendered_config = template.render(iface=iface)
    print('--------------------------------------')
    print(rendered_config)

    # Write rendered configuration to the file
    with open('/etc/netplan/00-installer-config.yaml', 'a') as config_file:
        config_file.write(rendered_config)
    # Run the 'sudo netplan generate' command
    try:
        subprocess.run(['sudo', 'netplan', 'generate'], check=True)
        subprocess.run(['sudo', 'netplan', 'apply'], check=True)
        print("Netplan configuration applied successfully.")
        print('--------------------------------------')
        return True
    except subprocess.CalledProcessError as e:
        print("Error generating Netplan configuration:", e)
        return False


def add_new_interface(iface):
    """
    Add a new interface to the all_ifaces list.
    """
    success = False
    # get the macaddress
    with open(f'/sys/class/net/{iface["ifname"]}/address') as file:
        iface['mac'] = file.read()
    print(f'New interface {iface["name"]} with ifname {iface["ifname"]} adding to Network...')
    # configure the interface
    if render_and_apply_netplan_config(iface) is True:
        success = True
    return success


def print_table(all_ifaces_config):
    """
    Print the tabular data for all interfaces.
    """
    # Define table headers
    headers = ["Interface Name", "Interface IF Name", "Configured"]
    # Extract relevant data for each interface
    table_data = [[iface['name'], iface['ifname'], iface['configured']] for iface in all_ifaces_config]
    print(tabulate(table_data, headers=headers))


def scan_for_new_iface(all_ifaces_names, except_ifaces):
    """
    Scan /sys/class/net/ directory for new network interface.
    Returns an new active interface name.
    """
    configured_ifaces = all_ifaces_names + except_ifaces
    all_new_ifaces = [interface for interface in os.listdir('/sys/class/net/') if interface not in configured_ifaces]
    new_active_iface = ''
    for name in all_new_ifaces:
        if get_iface_operstate(name) and get_iface_carrier(name):
            new_active_iface = name
            break
    return new_active_iface


def request_for_iface(name, all_ifaces_names, except_ifaces):
    print(f'\nPlease connect the `{name}` interface')
    while True:
        input(f'\nPress ENTER when `{name}` interface is connected...')
        new_iface = scan_for_new_iface(all_ifaces_names, except_ifaces)
        if new_iface != '':
            print(f'\n`{name}` interface detected', new_iface)
            return new_iface
        else:
            print(f'\n`{name}` interface NOT detected. Try again.')


def prepare_podnet_config(its_podnet_a):
    # Get the config_data
    config_data = read_config_file()

    # sort ipaddresses
    pod_number = config_data['pod_number']
    oob_ip = f'10.{pod_number}.0.{254 if its_podnet_a else 253}/16'
    primary_ipv4_subnet_items = config_data['primary_ipv4_subnet'].split('/')
    ipv6_subnet_items = config_data['ipv6_subnet'].split('/')
    mgmt_ipv4 = f'{next(ipaddress.IPv4Network(config_data["primary_ipv4_subnet"]).hosts())}/{primary_ipv4_subnet_items[1]}'
    mgmt_ipv6 = f'{ipv6_subnet_items[0]}10:0:{2 if its_podnet_a else 3}/64'
    mgmt_route_to = f'{ipv6_subnet_items[0][:ipv6_subnet_items[0].rfind(":")]}d0c6::/64'
    mgmt_route_via = f'{ipv6_subnet_items[0]}4000:1'

    # gather the list of interfaces with details
    all_ifaces = [
        {'name': 'public0', 'ifname': '', 'mac': '', 'ips': [], 'routes': [{'to': '', 'via': ''}, ],
         'configured': True},
        {'name': 'mgmt0', 'ifname': '', 'mac': '', 'ips': [mgmt_ipv4, mgmt_ipv6],
         'routes': [{'to': mgmt_route_to, 'via': mgmt_route_via}], 'configured': False},
        {'name': 'oob0', 'ifname': '', 'mac': '', 'ips': [oob_ip], 'routes': [{'to': '10.0.0.0/8', 'via': '10.0.0.1'}],
         'configured': False},
        {'name': 'private0', 'ifname': '', 'mac': '', 'ips': [], 'routes': [], 'configured': False},
        {'name': 'inter0', 'ifname': '', 'mac': '', 'ips': [], 'routes': [], 'configured': False},
    ]

    return all_ifaces


def choose_podnet_type():
    """
    Prompt the user to choose the server type.
    Returns the chosen server type.
    """
    print("Choose the PodNet type:")
    print("1. PodNet A")
    print("2. PodNet B")
    while True:
        choice = input("Enter the corresponding number: ")
        if choice == '1':
            return 'PodNet A'
        elif choice == '2':
            return 'PodNet B'
        else:
            print("Invalid choice. Please enter '1' or '2'.")


if __name__ == '__main__':
    # Define the introductory comments
    intro_comments = '''
    1. Completes all the network interface configuration other than the public0
    2. This script considers it has been run only in accordance with the procedure i.e.,
       CIDATA's user-data file triggers this script as a part of post-installation `runcmd` step.
    3. Only one interface is connected at each request.
    4. In case you commit a mistake, please repeat the Installation process from the beginning.
    5. Finally applies RoboSOC blocklist nftable
    '''

    # Calculate the width of the box
    box_width = max(len(line) for line in intro_comments.splitlines()) + 4

    # Print the box with the introductory comments
    print('*' * box_width)
    print('*{:^{width}}*'.format('', width=box_width-2))
    for line in intro_comments.splitlines():
        print('*{:<{width}}*'.format(line, width=box_width-2))
    print('*{:^{width}}*'.format('', width=box_width-2))
    print('*' * box_width)

    # Choose PodNet type
    podnet_type = choose_podnet_type()
    print("You chose:", podnet_type)

    # Load and Prepare for config
    all_ifaces_config = prepare_podnet_config(True if podnet_type == 'PodNet A' else False)

    # Extract interface names from all_ifaces
    all_ifaces_names = [iface['name'] for iface in all_ifaces_config]

    # exception interfaces
    except_ifaces = ['lo', 'docker0']

    key = 'podnet_a_%s_ifname' if podnet_type == 'PodNet A' else 'podnet_b_%s_ifname'

    # Find the public0 interface's altname and update the config.json
    public_ifname = get_iface_altname('public0')
    update_config_file(key % 'public', public_ifname)
    except_ifaces.append(public_ifname)
    for iface in all_ifaces_config:
        if iface['name'] == 'public0':
            iface['ifname'] = public_ifname
            break
    print('\nAdded `public0` ifname to config.json file')

    for iface in all_ifaces_config:
        name = iface['name']
        if name != 'public0':
            ifname = request_for_iface(name, all_ifaces_names, except_ifaces)
            iface['ifname'] = ifname
            configured = add_new_interface(iface)
            if configured is False:
                print(f'Failed to configure the {name} interface, Exiting.')
                exit(1)
            name = name[:-1] if name[-1].isdigit() else name
            update_config_file(key % str(name), ifname)
            except_ifaces.append(ifname)

        print('\nCurrent status of the Network:')
        print_table(all_ifaces_config)
        print()

    print('All interfaces are configured and updated config json.')

    # Setup robosoc functionality.
    # set the /etc/cloudcix/pod/podnet_installer/robosoc.py file to executable ie to +x
    os.system('chmod +x /etc/cloudcix/pod/podnet_installer/robosoc.py > /dev/null 2>&1')
    # creates a cron job file for robosoc
    with open('/etc/cron.d/robosoc', 'w') as file:
        file.write('*/15 * * * * root /etc/cloudcix/pod/podnet_installer/robosoc.py \n')
    # for cron job file, file must be executable so set to +x
    os.system('chmod +x /etc/cron.d/robosoc > /dev/null 2>&1')
    print('RoboSOC functionality setup successfully.')
