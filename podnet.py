import time
import subprocess
import os
import json
import ipaddress
from jinja2 import Template, Environment, FileSystemLoader
from tabulate import tabulate

JINJA_ENV = Environment(
    loader=FileSystemLoader('./'),
    trim_blocks=True,
    lstrip_blocks=True,
)

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

# exception interfaces
except_ifaces = ['lo', 'docker0']


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


def get_public_ifname():
    return os.popen("ip link show public0 | grep 'altname' | awk '{print $2}'").read().strip()


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
        {'name': 'public0', 'ifname': '', 'mac': '', 'ips': [], 'routes':[], 'configured': True},
        {'name': 'mgmt0', 'ifname': '', 'mac': '', 'ips': [mgmt_ipv4, mgmt_ipv6],
         'routes':[{'to': mgmt_route_to, 'via': mgmt_route_via}], 'configured': False},
        {'name': 'oob0', 'ifname': '', 'mac': '', 'ips': [oob_ip],
         'routes':[{'to': '10.0.0.0/8', 'via': '10.0.0.1'}], 'configured': False},
        {'name': 'private0', 'ifname': '', 'mac': '', 'ips': [], 'routes':[], 'configured':False},
        {'name': 'inter0', 'ifname': '', 'mac': '', 'ips': [], 'routes':[], 'configured':False},
    ]
    return all_ifaces


def scan_for_new_interfaces(all_ifaces_names):
    """
    Scan /sys/class/net/ directory for new network interfaces.
    Returns a list of interface names.
    """
    configured_ifaces = all_ifaces_names + except_ifaces
    return [interface for interface in os.listdir('/sys/class/net/') if interface not in configured_ifaces]


def find_non_configured_ifaces(all_ifaces_config):
    list_items = [iface for iface in all_ifaces_config if not iface['configured']]
    list_length = len(list_items)
    return list_items, list_length


def choose_interface_name(all_ifaces_config):
    """
    Prompt the user to choose a name for the new interface.
    Returns the chosen interface name.
    """
    non_configured_ifaces = find_non_configured_ifaces(all_ifaces_config)[0]
    print("Choose a name for the new interface:")
    for index, iface in enumerate(non_configured_ifaces):
        print(f"{index + 1}. {iface['name']}")
    while True:
        try:
            choice = int(input("Enter the corresponding number: "))
            if 1 <= choice <= len(non_configured_ifaces):
                return non_configured_ifaces[choice - 1]['name']
            else:
                print("Invalid choice. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")


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
        print("Netplan configuration generated successfully.")
        subprocess.run(['sudo', 'netplan', 'apply'], check=True)
        print("Netplan configuration applied successfully.")
    except subprocess.CalledProcessError as e:
        print("Error generating Netplan configuration:", e)
    print('--------------------------------------')


def add_new_interface(all_ifaces_config, name, ifname):
    """
    Add a new interface to the all_ifaces list.
    """
    for iface in all_ifaces_config:
        if iface['name'] == name:
            iface['ifname'] = ifname
            # get the macaddress
            with open(f'/sys/class/net/{ifname}/address') as file:
                iface['mac'] = file.read()
            print(f"New interface '{name}' with ifname '{ifname}' adding to Network...")
            # configure the interface
            render_and_apply_netplan_config(iface)
            iface['configured'] = True
            break


def print_table(all_ifaces_config):
    """
    Print the tabular data for all interfaces.
    """
    # Define table headers
    headers = ["Interface Name", "Interface IF Name", "Configured"]
    # Extract relevant data for each interface
    table_data = [[iface['name'], iface['ifname'], iface['configured']] for iface in all_ifaces_config]
    print(tabulate(table_data, headers=headers))


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

    # Choose PodNet type
    podnet_type = choose_podnet_type()
    print("You chose:", podnet_type)

    # Load and Prepare for config
    all_ifaces_config = prepare_podnet_config(True if podnet_type == 'PodNet A' else False)

    # Extract interface names from all_ifaces
    all_ifaces_names = [iface['name'] for iface in all_ifaces_config]

    key = 'podnet_a_%s_ifname' if podnet_type == 'PodNet A' else 'podnet_b_%s_ifname'
    # update config json file for public interface
    public_ifname = get_public_ifname()
    update_config_file(key % 'public', public_ifname)
    for iface in all_ifaces_config:
        if iface['name'] == 'public0':
           iface['ifname'] = public_ifname
    print('\nAdded `public` ifname to config.json file')
    print('\nScanning for new interface.')
    # Look for New interface and configure it
    first_iteration = True  # Flag to track the first iteration
    while find_non_configured_ifaces(all_ifaces_config)[1] > 0:
        new_interfaces = scan_for_new_interfaces(all_ifaces_names)
        if new_interfaces:
            print("\nNew interface(s) detected", new_interfaces)
            print('\nCurrent status of the Network:')
            print_table(all_ifaces_config)
            print()
            for ifname in new_interfaces:
                name = choose_interface_name(all_ifaces_config)
                add_new_interface(all_ifaces_config, name, ifname)
                name = name[:-1] if name[-1].isdigit() else name
                update_config_file(key % str(name), ifname)
            first_iteration = True

        elif first_iteration:
            print("No new interfaces detected: Scanning for new interfaces.", end="")
            first_iteration = False
        else:
            print(".", end="", flush=True)  # Print a dot without newline
        time.sleep(5)  # Scan every 5 seconds (adjust as needed)

    print('All interfaces are configured and updated config json.')

    # Setup robosoc functionality.
    # set the /etc/cloudcix/pod/robosoc.py file to executable ie to +x
    os.system('sudo chmod +x /etc/cloudcix/pod/podnet_installer/robosoc.py > /dev/null 2>&1')
    with open('/etc/cron.d/robosoc', 'w') as file:
        file.write('*/15 * * * * root /etc/cloudcix/pod/podnet_installer/robosoc.py > /dev/null 2>&1 \n')
    # for cron job file, file must be executable so set to +x
    os.system('sudo chmod +x /etc/cron.d/robosoc > /dev/null 2>&1')
    print('RoboSOC functionality setup successfully.')
