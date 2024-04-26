# stdlib
import ipaddress
# local
from utils import config_filepath, config_file_exists, read_config_file

__all__ = [
    'validate_config',
]


def podnet_keys():
    keys = [
        'ipv4_link_subnet',
        'ipv6_link_subnet',
    ]
    return keys


def appliance_keys():
    keys = [
        'ceph_monitors',
    ]
    return keys


def validate_config_keys(installer_type, config):
    """
    A list of keys that are required to be in config loaded to ensure program runs smoothly
    """
    required_params = [
        'pod_number',
        'pod_name',
        'blend',
        'primary_ipv4_subnet',
        'ipv6_subnet',
        'dns_ips',
    ]

    if 'podnet' in installer_type:
        required_params.extend(podnet_keys())
    elif 'appliance' in installer_type:
        required_params.extend(appliance_keys())

    missing_keys = []

    for key in required_params:
        if key not in config:
            missing_keys.append(key)

    if len(missing_keys) > 0:
        error_msg = f'The following keys were missing from the config file loaded: {", ".join(missing_keys)}'
        return False, error_msg

    return True, None


def validate_config(installer_type):
    result = True
    errors_list = []

    # Search for the config.json file
    if not config_file_exists():
        errors_list.append(f'The {config_filepath} file NOT found!')
        return False, errors_list

    # Load the config.json file
    config = read_config_file()

    # Validate config keys
    valid_keys, error = validate_config_keys(installer_type, config)
    if not valid_keys:
        errors_list.append(error)
        return False, errors_list

    # Validate config values
    # pod identifiers
    success, errors = validate_pod_identifiers(config)
    if not success:
        result = False
        errors_list.extend(errors)
    # pod ipaddress objects
    success, errors = validate_pod_ips(config, installer_type)
    if not success:
        result = False
        errors_list.extend(errors)

    return result, errors_list


def validate_pod_identifiers(config):
    result = True
    error_list = []
    # pod_number
    try:
        pod_number = int(config['pod_number'])
        if pod_number not in range(0, 255):
            error_list.append(
                'Test (1.2.2): Invalid "pod_number". It must be a value in range 0-254.',
            )
            result = False
    except (TypeError, ValueError):
        error_list.append('Test (1.2.1): Invalid "pod_number". It must be an integer value.')
        result = False

    # pod_name
    pod_name = str(config['pod_name'])
    if pod_name in ['', None]:
        error_list.append('Test(1.2.3): Invalid "pod_name". It is required.')
        result = False

    # blend
    try:
        blend = int(config['blend'])
        if blend not in [2, 4, 6, 7]:
            error_list.append(
                f'Test (1.2.5): Invalid "blend" {blend}. It can only be a value in set {2, 4, 6, 7}.',
            )
            result = False
    except (TypeError, ValueError):
        error_list.append(
            'Test (1.2.4): Invalid "blend". It must be an integer value in set {2, 4, 6, 7}.',
        )
        result = False

    return result, error_list


def validate_pod_ips(config, installer_type):
    # Test 1.2.x  IP Address consistency tests
    result = True
    error_list = []

    # IPv4 Primary Subnet
    try:
        ipv4_primary_subnet = ipaddress.ip_network(config['primary_ipv4_subnet'])
        if not int(str(ipv4_primary_subnet).split('/')[1]) <= 29:
            error_list.append('Test (1.2.7): Invalid "primary_ipv4_subnet". The prefix must be <= 29.')
            result = False
    except ValueError:
        ipv4_primary_subnet = ipaddress.ip_network('0.0.0.0/29')
        error_list.append(
            'Test (1.2.6): Invalid "primary_ipv4_subnet". It is NOT valid IP address.',
        )
        result = False

    # IPv6 Main Subnet
    try:
        ipv6_subnet = ipaddress.ip_network(config['ipv6_subnet'])
        if not int(str(ipv6_subnet).split('/')[1]) <= 48:
            error_list.append('Test (1.2.9): Invalid "ipv6_subnet".The prefix must be <= 48.')
            result = False
    except ValueError:
        ipv6_subnet = ipaddress.ip_network('::/48')
        error_list.append('Test (1.2.8): Invalid "ipv6_subnet". It is NOT valid IP address subnet.')
        result = False

    # dns ips
    dns_ips = config['dns_ips']
    if dns_ips in ['', None]:
        error_list.append('Test (1.2.10): Invalid "dns_ips".It is required.')
        result = False
    try:
        for ip in dns_ips.split(','):
            ipaddress.ip_address(ip.strip())
    except ValueError:
        error_list.append('Test (1.2.11): Invalid "dns_ips". It must have valid IP addresses.')
        result = False

    # IPv4 and IPv6 Link Subnet only for podnet
    if 'podnet' in installer_type:
        try:
            ipv4_link_subnet = ipaddress.ip_network(config['ipv4_link_subnet'])
            if not int(str(ipv4_link_subnet).split('/')[1]) <= 29:
                error_list.append('Test (1.2.13): Invalid "ipv4_link_subnet". The prefix must be <= 29.')
                result = False
        except ValueError:
            ipv4_link_subnet = ipaddress.ip_network('0.0.0.0/29')
            error_list.append('Test (1.2.12): Invalid "ipv4_link_subnet". It is NOT a valid IP subnet cidr.')
            result = False

        if ipv4_link_subnet in ipv4_primary_subnet:
            error_list.append('Test (1.2.14): "ipv4_link_subnet" must NOT be within "ipv4_primary_subnet".')
            result = False

        try:
            ipv6_link_subnet = ipaddress.ip_network(config['ipv6_link_subnet'])
            if not int(str(ipv6_link_subnet).split('/')[1]) <= 126:
                error_list.append('Test (1.2.16): Invalid "ipv6_link_subnet".The prefix must be <= 126.')
                result = False
        except ValueError:
            ipv6_link_subnet = ipaddress.ip_network('::/126')
            error_list.append('Test (1.2.15): Invalid "ipv6_link_subnet".It is NOT valid IP address subnet.')
            result = False

        if ipv6_link_subnet in ipv6_subnet:
            error_list.append('Test (1.2.17): "ipv6_link_subnet" must NOT be within "ipv6_subnet".')
            result = False

    # ceph_monitors only for an appliance that its blend includes the region flavour
    if 'appliance' in installer_type:
        ceph_monitors = config['ceph_monitors']
        if ceph_monitors in ['', None]:
            error_list.append('Test (1.2.18): Invalid "ceph_monitors". The "ceph_monitors" is required.')
            result = False
        try:
            for ip in dns_ips.split(','):
                ipaddress.ip_address(ip)
        except ValueError:
            error_list.append('Test (1.2.19): Invalid "ceph_monitors". It must have valid IP addresses.')
            result = False

    return result, error_list
