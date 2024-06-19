# stdlib
import ipaddress
import os
from urllib.parse import urlparse
# lib
import psutil
from ping3 import ping
from validate_email_address import validate_email
# local
from interface_utils import read_interface_file
from sql_utils import (
    # methods
    get_cidata,
    get_instanciated_infra,
    get_instanciated_metadata,
    get_test_details,
    update_test_details,
)


#######################################################
#  Block 1. Hardware Tests                            #
#######################################################

# 1.1.1 CPU
def hard_core_coun(test_id, cores_min):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '1.1.1 Hardware CPU-Core Count  - Pass - Count = '
    warn_message   = '1.1.1 Hardware CPU-Core Count  - Warn - Count = '
    fail_message   = '1.1.1 Hardware CPU-Core Count  - Fail - Count = '
    ignore_message = '1.1.1 Hardware CPU-Core Count  - Ignore'

    test_map_bit = 2**test_id

    if test_map_bit & ignore:                                        # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    cores = os.cpu_count()

    if cores >= cores_min:                                           # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message} {cores}'
    else:
        if test_map_bit & fail:                                    # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message} {cores}'
        elif test_map_bit & warn:                                  # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message} {cores}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return

# 1.2.1 RAM
def hard_ram__coun(test_id, ram_min):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '1.2.1 Hardware RAM Count       - Pass - Count = '
    warn_message   = '1.2.1 Hardware RAM Count       - Warn - Count = '
    fail_message   = '1.2.1 Hardware RAM Count       - Fail - Count = '
    ignore_message = '1.2.1 Hardware RAM Count       - Ignore'

    test_map_bit = 2**test_id

    if test_map_bit & ignore:                                    # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    ram = int((psutil.virtual_memory()).total / 1E9)

    if ram >= ram_min:                                          # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message} {ram}GB'
    else:
        if test_map_bit & fail:                                # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message} {ram}GB'
        elif test_map_bit & warn:                              # Test warn

            warn_map += test_map_bit
            result[test_id] = f'{warn_message} {ram}GB'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return

# 1.3.1 Storage
def hard_stor_coun(test_id, storage_min):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '1.3.1 Hardware Storage         - Pass - Count = '
    warn_message   = '1.3.1 Hardware Storage         - Warn - Count = '
    fail_message   = '1.3.1 Hardware Storage         - Fail - Count = '
    ignore_message = '1.3.1 Hardware Storage         - Ignore'

    test_map_bit = 2**test_id

    if test_map_bit & ignore:                                           # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    storage = 400   # Replace this with actual reading code

    if storage >= storage_min:                                          # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message} {storage}GB'
    else:
        if test_map_bit & fail:                                       # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message} {storage}GB'
        elif test_map_bit & warn:                                     # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message} {storage}GB'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return

# 1.4.1 PodNet Port
def hard_pprt_coun(test_id, ports_min):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '1.4.1 Hardware PodNet Ports    - Pass - Count = '
    warn_message   = '1.4.1 Hardware PodNet Ports    - Warn - Count = '
    fail_message   = '1.4.1 Hardware PodNet Ports    - Fail - Count = '
    ignore_message = '1.4.1 Hardware PodNet Ports    - Ignore'

    test_map_bit = 2**test_id

    if test_map_bit & ignore:                                           # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    ports = len([port for port in os.listdir('/sys/class/net/') if port not in ['lo', 'docker0']])

    if ports >= ports_min:                                             # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message} {ports}'
    else:
        if test_map_bit & fail:                                       # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message} {ports}'
        elif test_map_bit & warn:                                     # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message} {ports}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return

# 1.4.2 Appliance Port
def hard_aprt_coun(test_id, ports_min):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '1.4.2 Hardware Appliance Ports - Pass - Count = '
    warn_message   = '1.4.2 Hardware Appliance Ports - Warn - Count = '
    fail_message   = '1.4.2 Hardware Appliance Ports - Fail - Count = '
    ignore_message = '1.4.2 Hardware Appliance Ports - Ignore'

    test_map_bit = 2**test_id

    if test_map_bit & ignore:                                           # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    ports = len([port for port in os.listdir('/sys/class/net/') if port not in ['lo', 'docker0']])

    if ports >= ports_min:                                             # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message} {ports}'
    else:
        if test_map_bit & fail:                                       # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message} {ports}'
        elif test_map_bit & warn:                                     # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message} {ports}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return

# 2.1.1 Public Port Operstate
def hard_publ_oper(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '2.1.1 Hardware public0  - Pass - Operstate = '
    warn_message   = '2.1.1 Hardware public0  - Warn - Operstate = '
    fail_message   = '2.1.1 Hardware public0  - Fail - Operstate = '
    ignore_message = '2.1.1 Hardware public0  - Ignore'

    test_map_bit = 2**test_id

    if test_map_bit & ignore:                                           # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    operstate = read_interface_file('public0', 'operstate')

    if operstate == 'up':                                               # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message} {operstate}'
    else:
        if test_map_bit & fail:                                       # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message} {operstate}'
        elif test_map_bit & warn:                                     # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message} {operstate}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return

# 2.1.2 Public Port Carrier
def hard_publ_carr(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '2.1.2 Hardware public0  - Pass - Carrier = '
    warn_message   = '2.1.2 Hardware public0  - Warn - Carrier = '
    fail_message   = '2.1.2 Hardware public0  - Fail - Carrier = '
    ignore_message = '2.1.2 Hardware public0  - Ignore'

    test_map_bit = 2**test_id

    if test_map_bit & ignore:                                           # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    carrier = read_interface_file('public0', 'carrier')

    if carrier == '1':                                                  # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message} {carrier}'
    else:
        if test_map_bit & fail:                                       # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message} {carrier}'
        elif test_map_bit & warn:                                     # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message} {carrier}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return

# 2.1.3 Public Port Ethernet Name
def hard_publ_ethn(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '2.1.3 Hardware public0  - Pass - Ethernet Name Match'
    warn_message   = '2.1.3 Hardware public0  - Warn - Ethernet Name = '
    fail_message   = '2.1.3 Hardware public0  - Fail - Ethernet Name = '
    ignore_message = '2.1.3 Hardware public0  - Ignore'

    test_map_bit = 2**test_id

    if test_map_bit & ignore:                                           # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_infra = get_instanciated_infra()
    instanciated_metadata = get_instanciated_metadata()
    metadata_field = f'{instanciated_infra["hostname"].replace("-", "_")}_public_ifname'
    metadata_name = instanciated_metadata['config.json'].get(metadata_field, '')
    infra_name = 'Not Found'
    try:
        ethernets = instanciated_infra['netplan']['network']['ethernets']
        for interface_name, interface_data in ethernets.items():
            if interface_data.get('set-name', '') == 'public0':
                infra_name = interface_name
                break
    except KeyError:
        pass

    if metadata_name == infra_name:                                     # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message}'
    else:
        if test_map_bit & fail:                                       # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message} {metadata_name} != {infra_name}'
        elif test_map_bit & warn:                                     # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message} {metadata_name} != {infra_name}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return

# 2.2.1 Management Port Operstate
def hard_mgmt_oper(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '2.2.1 Hardware mgmt0  - Pass - Operstate = '
    warn_message   = '2.2.1 Hardware mgmt0  - Warn - Operstate = '
    fail_message   = '2.2.1 Hardware mgmt0  - Fail - Operstate = '
    ignore_message = '2.2.1 Hardware mgmt0  - Ignore'

    test_map_bit = 2**test_id

    if test_map_bit & ignore:                                           # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    operstate = read_interface_file('mgmt0', 'operstate')

    if operstate == 'up':                                               # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message} {operstate}'
    else:
        if test_map_bit & fail:                                       # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message} {operstate}'
        elif test_map_bit & warn:                                     # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message} {operstate}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return

# 2.2.2 Management Port Carrier
def hard_mgmt_carr(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '2.2.2 Hardware mgmt0  - Pass - Carrier = '
    warn_message   = '2.2.2 Hardware mgmt0  - Warn - Carrier = '
    fail_message   = '2.2.2 Hardware mgmt0  - Fail - Carrier = '
    ignore_message = '2.2.2 Hardware mgmt0  - Ignore'

    test_map_bit = 2**test_id

    if test_map_bit & ignore:                                           # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    carrier = read_interface_file('mgmt0', 'carrier')

    if carrier == '1':                                                  # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message} {carrier}'
    else:
        if test_map_bit & fail:                                       # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message} {carrier}'
        elif test_map_bit & warn:                                     # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message} {carrier}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return

# 2.2.3 Management Port Ethernet Name
def hard_mgmt_ethn(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '2.2.3 Hardware mgmt0  - Pass - Ethernet Name Match'
    warn_message   = '2.2.3 Hardware mgmt0  - Warn - Ethernet Name = '
    fail_message   = '2.2.3 Hardware mgmt0  - Fail - Ethernet Name = '
    ignore_message = '2.2.3 Hardware mgmt0  - Ignore'

    test_map_bit = 2**test_id

    if test_map_bit & ignore:                                           # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_infra = get_instanciated_infra()
    instanciated_metadata = get_instanciated_metadata()

    metadata_field = f'{instanciated_infra["hostname"].replace("-", "_")}_mgmt_ifname'
    metadata_name = instanciated_metadata['config.json'].get(metadata_field, '')
    infra_name = 'Not Found'
    try:
        ethernets = instanciated_infra['netplan']['network']['ethernets']
        for interface_name, interface_data in ethernets.items():
            if interface_data.get('set-name', '') == 'mgmt0':
                infra_name = interface_name
                break
    except KeyError:
        pass

    if metadata_name == infra_name:                                     # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message}'
    else:
        if test_map_bit & fail:                                       # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message} {metadata_name} != {infra_name}'
        elif test_map_bit & warn:                                     # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message} {metadata_name} != {infra_name}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return

# 2.3.1 OOB Port Operstate
def hard_oob__oper(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '2.3.1 Hardware oob0  - Pass - Operstate = '
    warn_message   = '2.3.1 Hardware oob0  - Warn - Operstate = '
    fail_message   = '2.3.1 Hardware oob0  - Fail - Operstate = '
    ignore_message = '2.3.1 Hardware oob0  - Ignore'

    test_map_bit = 2**test_id

    if test_map_bit & ignore:                                           # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    operstate = read_interface_file('oob0', 'operstate')

    if operstate == 'up':                                               # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message} {operstate}'
    else:
        if test_map_bit & fail:                                       # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message} {operstate}'
        elif test_map_bit & warn:                                     # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message} {operstate}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return

# 2.3.2 OOB Port Carrier
def hard_oob__carr(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '2.3.2 Hardware oob0  - Pass - Carrier = '
    warn_message   = '2.3.2 Hardware oob0  - Warn - Carrier = '
    fail_message   = '2.3.2 Hardware oob0  - Fail - Carrier = '
    ignore_message = '2.3.2 Hardware oob0  - Ignore'

    test_map_bit = 2**test_id

    if test_map_bit & ignore:                                           # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    carrier = read_interface_file('oob0', 'carrier')

    if carrier == '1':                                                  # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message} {carrier}'
    else:
        if test_map_bit & fail:                                       # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message} {carrier}'
        elif test_map_bit & warn:                                     # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message} {carrier}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return

# 2.3.3 OOOB Port Ethernet Name
def hard_oob__ethn(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '2.3.3 Hardware oob0  - Pass - Ethernet Name Match'
    warn_message   = '2.3.3 Hardware oob0  - Warn - Ethernet Name = '
    fail_message   = '2.3.3 Hardware oob0  - Fail - Ethernet Name = '
    ignore_message = '2.3.3 Hardware oob0  - Ignore'

    test_map_bit = 2**test_id

    if test_map_bit & ignore:                                           # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_infra = get_instanciated_infra()
    instanciated_metadata = get_instanciated_metadata()

    metadata_field = f'{instanciated_infra["hostname"].replace("-", "_")}_oob_ifname'
    metadata_name = instanciated_metadata['config.json'].get(metadata_field, '')
    infra_name = 'Not Found'
    try:
        ethernets = instanciated_infra['netplan']['network']['ethernets']
        for interface_name, interface_data in ethernets.items():
            if interface_data.get('set-name', '') == 'oob0':
                infra_name = interface_name
                break
    except KeyError:
        pass

    if metadata_name == infra_name:                                     # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message}'
    else:
        if test_map_bit & fail:                                       # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message} {metadata_name} != {infra_name}'
        elif test_map_bit & warn:                                     # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message} {metadata_name} != {infra_name}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return

# 2.4.1 Private Port Operstate - Region Flavor Pods
def hard_priv_oper(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '2.4.1 Hardware private0  - Pass - Operstate = '
    warn_message   = '2.4.1 Hardware private0  - Warn - Operstate = '
    fail_message   = '2.4.1 Hardware private0  - Fail - Operstate = '
    ignore_message = '2.4.1 Hardware private0  - Ignore'

    test_map_bit = 2**test_id

    if test_map_bit & ignore:                                           # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    operstate = read_interface_file('private0', 'operstate')

    if operstate == 'up':                                                # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message} {operstate}'
    else:
        if test_map_bit & fail:                                          # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message} {operstate}'
        elif test_map_bit & warn:                                        # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message} {operstate}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return

# 2.4.2 Private Port Carrier - Region Flavor Pods
def hard_priv_carr(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '2.4.2 Hardware private0  - Pass - Carrier = '
    warn_message   = '2.4.2 Hardware private0  - Warn - Carrier = '
    fail_message   = '2.4.2 Hardware private0  - Fail - Carrier = '
    ignore_message = '2.4.2 Hardware private0  - Ignore'

    test_map_bit = 2**test_id

    if test_map_bit & ignore:                                         # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    carrier = read_interface_file('private0', 'carrier')

    if carrier == '1':                                                # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message} {carrier}'
    else:
        if test_map_bit & fail:                                       # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message} {carrier}'
        elif test_map_bit & warn:                                     # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message} {carrier}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return

# 2.4.3 Private Port Ethernet Name - Region Flavor Pods
def hard_priv_ethn(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '2.4.3 Hardware private0  - Pass - Ethernet Name Match'
    warn_message   = '2.4.3 Hardware private0  - Warn - Ethernet Name = '
    fail_message   = '2.4.3 Hardware private0  - Fail - Ethernet Name = '
    ignore_message = '2.4.3 Hardware private0  - Ignore'

    test_map_bit = 2**test_id

    if test_map_bit & ignore:                                         # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_infra = get_instanciated_infra()
    instanciated_metadata = get_instanciated_metadata()
    metadata_field = f'{instanciated_infra["hostname"].replace("-", "_")}_private_ifname'
    metadata_name = instanciated_metadata['config.json'].get(metadata_field, '')
    infra_name = 'Not Found'
    try:
        ethernets = instanciated_infra['netplan']['network']['ethernets']
        for interface_name, interface_data in ethernets.items():
            if interface_data.get('set-name', '') == 'private0':
                infra_name = interface_name
                break
    except KeyError:
        pass

    if metadata_name == infra_name:                                    # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message}'
    else:
        if test_map_bit & fail:                                        # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message} {metadata_name} != {infra_name}'
        elif test_map_bit & warn:                                      # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message} {metadata_name} != {infra_name}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return

# 2.5.1 Inter Port Operstate - Region Flavor Pods
def hard_intr_oper(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '2.5.1 Hardware inter0  - Pass - Operstate = '
    warn_message   = '2.5.1 Hardware inter0  - Warn - Operstate = '
    fail_message   = '2.5.1 Hardware inter0  - Fail - Operstate = '
    ignore_message = '2.5.1 Hardware inter0  - Ignore'

    test_map_bit = 2**test_id

    if test_map_bit & ignore:                                          # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    operstate = read_interface_file('inter0', 'operstate')

    if operstate == 'up':                                             # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message} {operstate}'
    else:
        if test_map_bit & fail:                                       # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message} {operstate}'
        elif test_map_bit & warn:                                     # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message} {operstate}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return

# 2.5.2 Inter Port Carrier - Region Flavor Pods
def hard_intr_carr(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '2.5.2 Hardware inter0  - Pass - Carrier = '
    warn_message   = '2.5.2 Hardware inter0  - Warn - Carrier = '
    fail_message   = '2.5.2 Hardware inter0  - Fail - Carrier = '
    ignore_message = '2.5.2 Hardware inter0  - Ignore'

    test_map_bit = 2**test_id

    if test_map_bit & ignore:                                         # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    carrier = read_interface_file('inter0', 'carrier')

    if carrier == '1':                                                # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message} {carrier}'
    else:
        if test_map_bit & fail:                                       # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message} {carrier}'
        elif test_map_bit & warn:                                     # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message} {carrier}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return

# 2.5.3 Inter Port Ethernet Name - Region Flavor Pods
def hard_intr_ethn(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '2.5.3 Hardware inter0  - Pass - Ethernet Name Match'
    warn_message   = '2.5.3 Hardware inter0  - Warn - Ethernet Name = '
    fail_message   = '2.5.3 Hardware inter0  - Fail - Ethernet Name = '
    ignore_message = '2.5.3 Hardware inter0  - Ignore'

    test_map_bit = 2**test_id

    if test_map_bit & ignore:                                        # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_infra = get_instanciated_infra()
    instanciated_metadata = get_instanciated_metadata()
    metadata_field = f'{instanciated_infra["hostname"].replace("-", "_")}_inter_ifname'
    metadata_name = instanciated_metadata['config.json'].get(metadata_field, '')
    infra_name = 'Not Found'
    try:
        ethernets = instanciated_infra['netplan']['network']['ethernets']
        for interface_name, interface_data in ethernets.items():
            if interface_data.get('set-name', '') == 'inter0':
                infra_name = interface_name
                break
    except KeyError:
        pass

    if metadata_name == infra_name:                                   # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message}'
    else:
        if test_map_bit & fail:                                       # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message} {metadata_name} != {infra_name}'
        elif test_map_bit & warn:                                     # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message} {metadata_name} != {infra_name}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return

# 3.1.1 Instanciated and CIDATA config.json match
def config_matches(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '3.1.1 Instanciated and CIDATA config.json  - Pass - match'
    warn_message   = '3.1.1 Instanciated and CIDATA config.json  - Warn - not a match '
    fail_message   = '3.1.1 Instanciated and CIDATA config.json  - Fail - not a match'
    ignore_message = '3.1.1 Instanciated and CIDATA config.json  - Ignore'

    test_map_bit = 2**test_id

    if test_map_bit & ignore:                                          # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    cidata = get_cidata()
    instanciated_metadata = get_instanciated_metadata()

    if cidata['config.json'] == instanciated_metadata['config.json']: # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message}'
    else:
        if test_map_bit & fail:                                       # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message}'
        elif test_map_bit & warn:                                     # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return


# 3.2.1 Validation of pod_number from Instantiated Metadata config.json
def inst_conf_pnum(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '3.2.1 Instanciated config.json `pod_number` - Pass - in range'
    warn_message   = '3.2.1 Instanciated config.json `pod_number` - Warn - not in range'
    fail_message   = '3.2.1 Instanciated config.json `pod_number` - Fail - not in range'
    ignore_message = '3.2.1 Instanciated config.json `pod_number` - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:                                       # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_metadata = get_instanciated_metadata()
    pod_number = instanciated_metadata['config.json'].get('pod_number', -1)

    if int(pod_number) in range(0, 255):                            # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message}'
    else:
        if test_map_bit & fail:                                     # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message}'
        elif test_map_bit & warn:                                   # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return


# 3.2.2 Validation of pod_name from Instantiated Metadata config.json
def inst_conf_pnam(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '3.2.2 Instanciated config.json `pod_name` - Pass - Pod Name ='
    warn_message   = '3.2.2 Instanciated config.json `pod_name` - Warn - Pod Name ='
    fail_message   = '3.2.2 Instanciated config.json `pod_name` - Fail - Pod Name ='
    ignore_message = '3.2.2 Instanciated config.json `pod_name` - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:                                       # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_metadata = get_instanciated_metadata()
    pod_name = instanciated_metadata['config.json'].get('pod_name', '')

    if pod_name != '':                                              # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message} {pod_name}'
    else:
        if test_map_bit & fail:                                     # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message} {pod_name}'
        elif test_map_bit & warn:                                   # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message} {pod_name}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return


# 3.2.3 Validation of blend from Instantiated Metadata config.json
def inst_conf_blen(test_id, allowed_blends):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '3.2.3 Instanciated config.json `blend` - Pass - Valid'
    warn_message   = '3.2.3 Instanciated config.json `blend` - Warn - Invalid'
    fail_message   = '3.2.3 Instanciated config.json `blend` - Fail - Invalid'
    ignore_message = '3.2.3 Instanciated config.json `blend` - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:                                       # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_metadata = get_instanciated_metadata()
    blend = instanciated_metadata['config.json'].get('blend', 0)

    if int(blend) in allowed_blends:                                # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message}'
    else:
        if test_map_bit & fail:                                     # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message}'
        elif test_map_bit & warn:                                   # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return


# 3.2.4 Validation of `podnet_a_enabled` from Instantiated Metadata config.json
def inst_conf_aena(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '3.2.4 Instanciated config.json `podnet_a_enabled` - Pass - is False'
    warn_message   = '3.2.4 Instanciated config.json `podnet_a_enabled` - Warn - is True'
    fail_message   = '3.2.4 Instanciated config.json `podnet_a_enabled` - Fail - is True'
    ignore_message = '3.2.4 Instanciated config.json `podnet_a_enabled` - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:                                       # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_metadata = get_instanciated_metadata()
    podnet_a_enabled = instanciated_metadata['config.json'].get('podnet_a_enabled', True)

    if podnet_a_enabled is False:                                    # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message}'
    else:
        if test_map_bit & fail:                                     # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message}'
        elif test_map_bit & warn:                                   # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return


# 3.2.5 Validation of `podnet_a_enabled` from Instantiated Metadata config.json
def inst_conf_aenb(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '3.2.5 Instanciated config.json `podnet_a_enabled` - Pass - Boolean'
    warn_message   = '3.2.5 Instanciated config.json `podnet_a_enabled` - Warn - not Boolean'
    fail_message   = '3.2.5 Instanciated config.json `podnet_a_enabled` - Fail - not Boolean'
    ignore_message = '3.2.5 Instanciated config.json `podnet_a_enabled` - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:                                       # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_metadata = get_instanciated_metadata()
    podnet_a_enabled = instanciated_metadata['config.json'].get('podnet_a_enabled', 123)

    if type(podnet_a_enabled) is bool:                               # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message}'
    else:
        if test_map_bit & fail:                                     # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message}'
        elif test_map_bit & warn:                                   # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return


# 3.2.6 Validation of `podnet_b_enabled` from Instantiated Metadata config.json
def inst_conf_bena(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '3.2.6 Instanciated config.json `podnet_b_enabled` - Pass - is False'
    warn_message   = '3.2.6 Instanciated config.json `podnet_b_enabled` - Warn - is True'
    fail_message   = '3.2.6 Instanciated config.json `podnet_b_enabled` - Fail - is True'
    ignore_message = '3.2.6 Instanciated config.json `podnet_b_enabled` - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:                                       # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_metadata = get_instanciated_metadata()
    podnet_b_enabled = instanciated_metadata['config.json'].get('podnet_b_enabled', True)

    if podnet_b_enabled is False:                                    # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message}'
    else:
        if test_map_bit & fail:                                     # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message}'
        elif test_map_bit & warn:                                   # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return


# 3.2.7 Validation of `podnet_b_enabled` from Instantiated Metadata config.json
def inst_conf_benb(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '3.2.7 Instanciated config.json `podnet_b_enabled` - Pass - Boolean'
    warn_message   = '3.2.7 Instanciated config.json `podnet_b_enabled` - Warn - not Boolean'
    fail_message   = '3.2.7 Instanciated config.json `podnet_b_enabled` - Fail - not Boolean'
    ignore_message = '3.2.7 Instanciated config.json `podnet_b_enabled` - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:                                       # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_metadata = get_instanciated_metadata()
    podnet_b_enabled = instanciated_metadata['config.json'].get('podnet_b_enabled', 123)

    if type(podnet_b_enabled) is bool:                               # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message}'
    else:
        if test_map_bit & fail:                                     # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message}'
        elif test_map_bit & warn:                                   # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return


# 3.2.8 Validation of `podnet_a_enabled` and `podnet_b_enabled` from Instantiated Metadata config.json
def inst_conf_aben(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '3.2.8 Instanciated config.json `podnet_a_enabled` and `podnet_b_enabled` - Pass - both are not True'
    warn_message   = '3.2.8 Instanciated config.json `podnet_a_enabled` and `podnet_b_enabled` - Warn - both are True'
    fail_message   = '3.2.8 Instanciated config.json `podnet_a_enabled` and `podnet_b_enabled` - Fail - both are True'
    ignore_message = '3.2.8 Instanciated config.json `podnet_a_enabled` and `podnet_b_enabled` - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:                                       # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_metadata = get_instanciated_metadata()
    podnet_a_enabled = instanciated_metadata['config.json'].get('podnet_a_enabled', True)
    podnet_b_enabled = instanciated_metadata['config.json'].get('podnet_b_enabled', True)

    if podnet_a_enabled is True and podnet_b_enabled is True:
        if test_map_bit & fail:                                     # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message}'
        elif test_map_bit & warn:                                   # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message}'
    else:                                                           # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return


# 3.2.9 Validation of `ipv4_link_subnet` for a Valid network Range, from Instantiated Metadata config.json
def inst_conf_4lvr(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '3.2.9 Instanciated config.json `ipv4_link_subnet` network range - Pass - is valid'
    warn_message   = '3.2.9 Instanciated config.json `ipv4_link_subnet` network range - Warn - is not valid'
    fail_message   = '3.2.9 Instanciated config.json `ipv4_link_subnet` network range - Fail - is not valid'
    ignore_message = '3.2.9 Instanciated config.json `ipv4_link_subnet` network range - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:                                       # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_metadata = get_instanciated_metadata()
    ipv4_link_subnet = instanciated_metadata['config.json'].get('ipv4_link_subnet', '')

    try:
        ipaddress.ip_network(ipv4_link_subnet)
        valid_subnet = True
    except ValueError:
        valid_subnet = False

    if valid_subnet is True:                                       # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message}'
    else:
        if test_map_bit & fail:                                    # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message}'
        elif test_map_bit & warn:                                  # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return


# 3.2.10 Validation of `ipv4_link_subnet` range mask, from Instantiated Metadata config.json
def inst_conf_4lvm(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '3.2.10 Instanciated config.json `ipv4_link_subnet` range mask - Pass - is >= /29'
    warn_message   = '3.2.10 Instanciated config.json `ipv4_link_subnet` range mask - Warn - is not >= /29'
    fail_message   = '3.2.10 Instanciated config.json `ipv4_link_subnet` range mask - Fail - is not >= /29'
    ignore_message = '3.2.10 Instanciated config.json `ipv4_link_subnet` range mask - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:                                       # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_metadata = get_instanciated_metadata()
    ipv4_link_subnet = instanciated_metadata['config.json'].get('ipv4_link_subnet', '')
    try:
        ipaddress.ip_network(ipv4_link_subnet)
        valid_subnet = True
        mask = ipv4_link_subnet.split('/')[1]
    except ValueError:
        valid_subnet = False
        mask = 30

    if valid_subnet is True and int(mask) <= 29:                   # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message}'
    else:
        if test_map_bit & fail:                                    # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message}'
        elif test_map_bit & warn:                                  # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return


# 3.2.11 Validation of `ipv4_link_cpe` for a Valid IPAddress, from Instantiated Metadata config.json
def inst_conf_4cva(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '3.2.11 Instanciated config.json `ipv4_link_cpe` IPAddress - Pass - is valid'
    warn_message   = '3.2.11 Instanciated config.json `ipv4_link_cpe` IPAddress - Warn - is not valid'
    fail_message   = '3.2.11 Instanciated config.json `ipv4_link_cpe` IPAddress - Fail - is not valid'
    ignore_message = '3.2.11 Instanciated config.json `ipv4_link_cpe` IPAddress - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:                                       # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_metadata = get_instanciated_metadata()
    ipv4_link_cpe = instanciated_metadata['config.json'].get('ipv4_link_cpe', '')

    try:
        ipaddress.ip_address(ipv4_link_cpe)
        valid_address = True
    except ValueError:
        valid_address = False

    if valid_address is True:                          # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message}'
    else:
        if test_map_bit & fail:                        # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message}'
        elif test_map_bit & warn:                      # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return


# 3.2.12 Validation of `ipv4_link_cpe` from Instantiated Metadata config.json
def inst_conf_4cpe(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '3.2.12 Instanciated config.json `ipv4_link_cpe` - Pass - is in `ipv4_link_subnet`'
    warn_message   = '3.2.12 Instanciated config.json `ipv4_link_cpe` - Warn - is not in `ipv4_link_subnet`'
    fail_message   = '3.2.12 Instanciated config.json `ipv4_link_cpe` - Fail - is not in `ipv4_link_subnet`'
    ignore_message = '3.2.12 Instanciated config.json `ipv4_link_cpe` - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:                                       # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_metadata = get_instanciated_metadata()
    ipv4_link_subnet = instanciated_metadata['config.json'].get('ipv4_link_subnet', '')
    ipv4_link_cpe = instanciated_metadata['config.json'].get('ipv4_link_cpe', '')

    try:
        network = ipaddress.ip_network(ipv4_link_subnet)
        address = ipaddress.ip_address(ipv4_link_cpe)
        if address in network:
            in_range = True
        else:
            in_range = False
    except ValueError:
        in_range = False

    if in_range is True:                                           # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message}'
    else:
        if test_map_bit & fail:                                    # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message}'
        elif test_map_bit & warn:                                  # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return


# 3.2.13 Validation of `ipv4_link_pe` for a Valid IPAddress, from Instantiated Metadata config.json
def inst_conf_4pva(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '3.2.13 Instanciated config.json `ipv4_link_pe` IPAddress - Pass - is valid'
    warn_message   = '3.2.13 Instanciated config.json `ipv4_link_pe` IPAddress - Warn - is not valid'
    fail_message   = '3.2.13 Instanciated config.json `ipv4_link_pe` IPAddress - Fail - is not valid'
    ignore_message = '3.2.13 Instanciated config.json `ipv4_link_pe` IPAddress - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:                                       # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_metadata = get_instanciated_metadata()
    ipv4_link_subnet = instanciated_metadata['config.json'].get('ipv4_link_subnet', '')
    ipv4_link_pe = instanciated_metadata['config.json'].get('ipv4_link_pe', '')

    try:
        network = ipaddress.ip_network(ipv4_link_subnet)
        address = ipaddress.ip_address(ipv4_link_pe)
        if address in network:
            in_range = True
        else:
            in_range = False
    except ValueError:
        in_range = False

    if in_range is True:                                           # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message}'
    else:
        if test_map_bit & fail:                                    # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message}'
        elif test_map_bit & warn:                                  # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return


# 3.2.14 Validation of `ipv4_link_pe` from Instantiated Metadata config.json
def inst_conf__4pe(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '3.2.14 Instanciated config.json `ipv4_link_pe` - Pass - is in `ipv4_link_subnet`'
    warn_message   = '3.2.14 Instanciated config.json `ipv4_link_pe` - Warn - is not in `ipv4_link_subnet`'
    fail_message   = '3.2.14 Instanciated config.json `ipv4_link_pe` - Fail - is not in `ipv4_link_subnet`'
    ignore_message = '3.2.14 Instanciated config.json `ipv4_link_pe` - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:                                       # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_metadata = get_instanciated_metadata()
    ipv4_link_subnet = instanciated_metadata['config.json'].get('ipv4_link_subnet', '')
    ipv4_link_pe = instanciated_metadata['config.json'].get('ipv4_link_pe', '')

    try:
        network = ipaddress.ip_network(ipv4_link_subnet)
        address = ipaddress.ip_address(ipv4_link_pe)
        if address in network:
            in_range = True
        else:
            in_range = False
    except ValueError:
        in_range = False

    if in_range is True:                                           # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message}'
    else:
        if test_map_bit & fail:                                    # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message}'
        elif test_map_bit & warn:                                  # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return


# 3.2.15 Validation of `ipv4_link_pe` != `ipv4_link_cpe` from Instantiated Metadata config.json
def inst_conf_4pvc(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '3.2.15 Instanciated config.json `ipv4_link_pe` and `ipv4_link_cpe` - Pass - are not same'
    warn_message   = '3.2.15 Instanciated config.json `ipv4_link_pe` and `ipv4_link_cpe` - Warn - are same'
    fail_message   = '3.2.15 Instanciated config.json `ipv4_link_pe` and `ipv4_link_cpe` - Fail - are same'
    ignore_message = '3.2.15 Instanciated config.json `ipv4_link_pe` and `ipv4_link_cpe` - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:                                       # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_metadata = get_instanciated_metadata()
    ipv4_link_pe = instanciated_metadata['config.json'].get('ipv4_link_pe', '')
    ipv4_link_cpe = instanciated_metadata['config.json'].get('ipv4_link_cpe', '')

    try:
        pe = ipaddress.ip_address(ipv4_link_pe)
        cpe = ipaddress.ip_address(ipv4_link_cpe)
        if pe == cpe:
            different = False
        else:
            different = True
    except ValueError:
        different = False

    if different is True:                                          # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message}'
    else:
        if test_map_bit & fail:                                    # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message}'
        elif test_map_bit & warn:                                  # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return


# 3.2.16 Validation of `ipv6_link_subnet` for a Valid network Range, from Instantiated Metadata config.json
def inst_conf_6lvr(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '3.2.16 Instanciated config.json `ipv6_link_subnet` network range - Pass - is valid'
    warn_message   = '3.2.16 Instanciated config.json `ipv6_link_subnet` network range - Warn - is not valid'
    fail_message   = '3.2.16 Instanciated config.json `ipv6_link_subnet` network range - Fail - is not valid'
    ignore_message = '3.2.16 Instanciated config.json `ipv6_link_subnet` network range - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:                                       # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_metadata = get_instanciated_metadata()
    ipv6_link_subnet = instanciated_metadata['config.json'].get('ipv6_link_subnet', '')

    try:
        ipaddress.ip_network(ipv6_link_subnet)
        valid_subnet = True
    except ValueError:
        valid_subnet = False

    if valid_subnet is True:                                       # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message}'
    else:
        if test_map_bit & fail:                                    # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message}'
        elif test_map_bit & warn:                                  # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return


# 3.2.17 Validation of `ipv4_link_subnet` range mask, from Instantiated Metadata config.json
def inst_conf_6lvm(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '3.2.17 Instanciated config.json `ipv6_link_subnet` range mask - Pass - is >= /126'
    warn_message   = '3.2.17 Instanciated config.json `ipv6_link_subnet` range mask - Warn - is not >= /126'
    fail_message   = '3.2.17 Instanciated config.json `ipv6_link_subnet` range mask - Fail - is not >= /126'
    ignore_message = '3.2.17 Instanciated config.json `ipv6_link_subnet` range mask - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:                                       # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_metadata = get_instanciated_metadata()
    ipv6_link_subnet = instanciated_metadata['config.json'].get('ipv6_link_subnet', '')
    try:
        ipaddress.ip_network(ipv6_link_subnet)
        valid_subnet = True
        mask = ipv6_link_subnet.split('/')[1]
    except ValueError:
        valid_subnet = False
        mask = 127

    if valid_subnet is True and int(mask) <= 126:                   # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message}'
    else:
        if test_map_bit & fail:                                    # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message}'
        elif test_map_bit & warn:                                  # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return


# 3.2.18 Validation of `ipv8_link_cpe` for a Valid IPAddress, from Instantiated Metadata config.json
def inst_conf_6cva(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '3.2.18 Instanciated config.json `ipv6_link_cpe` IPAddress - Pass - is valid'
    warn_message   = '3.2.18 Instanciated config.json `ipv6_link_cpe` IPAddress - Warn - is not valid'
    fail_message   = '3.2.18 Instanciated config.json `ipv6_link_cpe` IPAddress - Fail - is not valid'
    ignore_message = '3.2.18 Instanciated config.json `ipv6_link_cpe` IPAddress - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:                                       # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_metadata = get_instanciated_metadata()
    ipv6_link_cpe = instanciated_metadata['config.json'].get('ipv6_link_cpe', '')

    try:
        ipaddress.ip_address(ipv6_link_cpe)
        valid_address = True
    except ValueError:
        valid_address = False

    if valid_address is True:                          # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message}'
    else:
        if test_map_bit & fail:                        # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message}'
        elif test_map_bit & warn:                      # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return


# 3.2.19 Validation of `ipv6_link_cpe` from Instantiated Metadata config.json
def inst_conf_6cpe(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '3.2.19 Instanciated config.json `ipv6_link_cpe` - Pass - is in `ipv6_link_subnet`'
    warn_message   = '3.2.19 Instanciated config.json `ipv6_link_cpe` - Warn - is not in `ipv6_link_subnet`'
    fail_message   = '3.2.19 Instanciated config.json `ipv6_link_cpe` - Fail - is not in `ipv6_link_subnet`'
    ignore_message = '3.2.19 Instanciated config.json `ipv6_link_cpe` - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:                                       # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_metadata = get_instanciated_metadata()
    ipv6_link_subnet = instanciated_metadata['config.json'].get('ipv6_link_subnet', '')
    ipv6_link_cpe = instanciated_metadata['config.json'].get('ipv6_link_cpe', '')

    try:
        network = ipaddress.ip_network(ipv6_link_subnet)
        address = ipaddress.ip_address(ipv6_link_cpe)
        if address in network:
            in_range = True
        else:
            in_range = False
    except ValueError:
        in_range = False

    if in_range is True:                                           # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message}'
    else:
        if test_map_bit & fail:                                    # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message}'
        elif test_map_bit & warn:                                  # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return


# 3.2.20 Validation of `ipv6_link_pe` for a Valid IPAddress, from Instantiated Metadata config.json
def inst_conf_6pva(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '3.2.20 Instanciated config.json `ipv6_link_pe` IPAddress - Pass - is valid'
    warn_message   = '3.2.20 Instanciated config.json `ipv6_link_pe` IPAddress - Warn - is not valid'
    fail_message   = '3.2.20 Instanciated config.json `ipv6_link_pe` IPAddress - Fail - is not valid'
    ignore_message = '3.2.20 Instanciated config.json `ipv6_link_pe` IPAddress - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:                                       # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_metadata = get_instanciated_metadata()
    ipv6_link_subnet = instanciated_metadata['config.json'].get('ipv6_link_subnet', '')
    ipv6_link_pe = instanciated_metadata['config.json'].get('ipv6_link_pe', '')

    try:
        network = ipaddress.ip_network(ipv6_link_subnet)
        address = ipaddress.ip_address(ipv6_link_pe)
        if address in network:
            in_range = True
        else:
            in_range = False
    except ValueError:
        in_range = False

    if in_range is True:                                           # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message}'
    else:
        if test_map_bit & fail:                                    # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message}'
        elif test_map_bit & warn:                                  # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return


# 3.2.21 Validation of `ipv6_link_pe` from Instantiated Metadata config.json
def inst_conf__6pe(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '3.2.21 Instanciated config.json `ipv6_link_pe` - Pass - is in `ipv6_link_subnet`'
    warn_message   = '3.2.21 Instanciated config.json `ipv6_link_pe` - Warn - is not in `ipv6_link_subnet`'
    fail_message   = '3.2.21 Instanciated config.json `ipv6_link_pe` - Fail - is not in `ipv6_link_subnet`'
    ignore_message = '3.2.21 Instanciated config.json `ipv6_link_pe` - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:                                       # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_metadata = get_instanciated_metadata()
    ipv6_link_subnet = instanciated_metadata['config.json'].get('ipv6_link_subnet', '')
    ipv6_link_pe = instanciated_metadata['config.json'].get('ipv6_link_pe', '')

    try:
        network = ipaddress.ip_network(ipv6_link_subnet)
        address = ipaddress.ip_address(ipv6_link_pe)
        if address in network:
            in_range = True
        else:
            in_range = False
    except ValueError:
        in_range = False

    if in_range is True:                                           # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message}'
    else:
        if test_map_bit & fail:                                    # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message}'
        elif test_map_bit & warn:                                  # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return


# 3.2.22 Validation of `ipv6_link_pe` != `ipv6_link_cpe` from Instantiated Metadata config.json
def inst_conf_6pvc(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '3.2.22 Instanciated config.json `ipv6_link_pe` and `ipv6_link_cpe` - Pass - are not same'
    warn_message   = '3.2.22 Instanciated config.json `ipv6_link_pe` and `ipv6_link_cpe` - Warn - are same'
    fail_message   = '3.2.22 Instanciated config.json `ipv6_link_pe` and `ipv6_link_cpe` - Fail - are same'
    ignore_message = '3.2.22 Instanciated config.json `ipv6_link_pe` and `ipv6_link_cpe` - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:                                       # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_metadata = get_instanciated_metadata()
    ipv6_link_pe = instanciated_metadata['config.json'].get('ipv6_link_pe', '')
    ipv6_link_cpe = instanciated_metadata['config.json'].get('ipv6_link_cpe', '')

    try:
        pe = ipaddress.ip_address(ipv6_link_pe)
        cpe = ipaddress.ip_address(ipv6_link_cpe)
        if pe == cpe:
            different = False
        else:
            different = True
    except ValueError:
        different = False

    if different is True:                                          # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message}'
    else:
        if test_map_bit & fail:                                    # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message}'
        elif test_map_bit & warn:                                  # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return


# 3.2.23 Validation of `primary_ipv4_subnet` for a Valid network Range, from Instantiated Metadata config.json
def inst_conf_4pmv(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '3.2.23 Instanciated config.json `primary_ipv4_subnet` network range - Pass - is valid'
    warn_message   = '3.2.23 Instanciated config.json `primary_ipv4_subnet` network range - Warn - is not valid'
    fail_message   = '3.2.23 Instanciated config.json `primary_ipv4_subnet` network range - Fail - is not valid'
    ignore_message = '3.2.23 Instanciated config.json `primary_ipv4_subnet` network range - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:                                       # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_metadata = get_instanciated_metadata()
    primary_ipv4_subnet = instanciated_metadata['config.json'].get('primary_ipv4_subnet', '')

    try:
        ipaddress.ip_network(primary_ipv4_subnet)
        valid_subnet = True
    except ValueError:
        valid_subnet = False

    if valid_subnet is True:                                       # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message}'
    else:
        if test_map_bit & fail:                                    # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message}'
        elif test_map_bit & warn:                                  # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return


# 3.2.24 Validation of `primary_ipv4_subnet` range mask, from Instantiated Metadata config.json
def inst_conf_4pmm(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '3.2.24 Instanciated config.json `primary_ipv4_subnet` range mask - Pass - is >= /29'
    warn_message   = '3.2.24 Instanciated config.json `primary_ipv4_subnet` range mask - Warn - is not >= /29'
    fail_message   = '3.2.24 Instanciated config.json `primary_ipv4_subnet` range mask - Fail - is not >= /29'
    ignore_message = '3.2.24 Instanciated config.json `primary_ipv4_subnet` range mask - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:                                       # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_metadata = get_instanciated_metadata()
    primary_ipv4_subnet = instanciated_metadata['config.json'].get('primary_ipv4_subnet', '')
    try:
        ipaddress.ip_network(primary_ipv4_subnet)
        valid_subnet = True
        mask = primary_ipv4_subnet.split('/')[1]
    except ValueError:
        valid_subnet = False
        mask = 30

    if valid_subnet is True and int(mask) <= 29:                   # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message}'
    else:
        if test_map_bit & fail:                                    # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message}'
        elif test_map_bit & warn:                                  # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return


# 3.2.25 Validation of `ipv6_subnet` for a Valid network Range, from Instantiated Metadata config.json
def inst_conf_6pmv(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '3.2.25 Instanciated config.json `ipv6_subnet` network range - Pass - is valid'
    warn_message   = '3.2.25 Instanciated config.json `ipv6_subnet` network range - Warn - is not valid'
    fail_message   = '3.2.25 Instanciated config.json `ipv6_subnet` network range - Fail - is not valid'
    ignore_message = '3.2.25 Instanciated config.json `ipv6_subnet` network range - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:                                       # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_metadata = get_instanciated_metadata()
    ipv6_subnet = instanciated_metadata['config.json'].get('ipv6_subnet', '')

    try:
        ipaddress.ip_network(ipv6_subnet)
        valid_subnet = True
    except ValueError:
        valid_subnet = False

    if valid_subnet is True:                                       # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message}'
    else:
        if test_map_bit & fail:                                    # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message}'
        elif test_map_bit & warn:                                  # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return


# 3.2.26 Validation of `ipv6_subnet` range mask, from Instantiated Metadata config.json
def inst_conf_6pmm(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '3.2.26 Instanciated config.json `ipv6_subnet` range mask - Pass - is >= /48'
    warn_message   = '3.2.26 Instanciated config.json `ipv6_subnet` range mask - Warn - is not >= /48'
    fail_message   = '3.2.26 Instanciated config.json `ipv6_subnet` range mask - Fail - is not >= /48'
    ignore_message = '3.2.26 Instanciated config.json `ipv6_subnet` range mask - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:  # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_metadata = get_instanciated_metadata()
    ipv6_subnet = instanciated_metadata['config.json'].get('ipv6_subnet', '')
    try:
        ipaddress.ip_network(ipv6_subnet)
        valid_subnet = True
        mask = ipv6_subnet.split('/')[1]
    except ValueError:
        valid_subnet = False
        mask = 49

    if valid_subnet is True and int(mask) <= 49:                   # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message}'
    else:
        if test_map_bit & fail:                                    # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message}'
        elif test_map_bit & warn:                                  # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return


# 3.2.27 Validation of `dns_ips` from Instantiated Metadata config.json
def inst_conf_dnss(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '3.2.27 Instanciated config.json `dns_ips` - Pass - all are valid IPs'
    warn_message   = '3.2.27 Instanciated config.json `dns_ips` - Warn - all are not valid IPs'
    fail_message   = '3.2.27 Instanciated config.json `dns_ips` - Fail - all are not valid IPs'
    ignore_message = '3.2.27 Instanciated config.json `dns_ips` - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:  # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_metadata = get_instanciated_metadata()
    dns_ips = instanciated_metadata['config.json'].get('dns_ips', 'add').split(',')
    valid_ips = True
    for dns_ip in dns_ips:
        try:
            ipaddress.ip_address(dns_ip.strip())
        except ValueError:
            valid_ips = False

    if valid_ips is True:  # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message}'
    else:
        if test_map_bit & fail:  # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message}'
        elif test_map_bit & warn:  # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return


# 3.2.28 Validation of `ceph_monitors` from Instantiated Metadata config.json
def inst_conf_cmon(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '3.2.28 Instanciated config.json `ceph_monitors` - Pass - is list and all are valid IPs'
    warn_message   = '3.2.28 Instanciated config.json `ceph_monitors` - Warn - Invalid'
    fail_message   = '3.2.28 Instanciated config.json `ceph_monitors` - Fail - Invalid'
    ignore_message = '3.2.28 Instanciated config.json `ceph_monitors` - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:                                      # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_metadata = get_instanciated_metadata()
    ceph_monitors = instanciated_metadata['config.json'].get('ceph_monitors', [])
    ipv6_subnet = instanciated_metadata['config.json'].get('ipv6_subnet', '::/127')
    valid = True
    for cmon in ceph_monitors:
        try:
            if ipaddress.ip_address(cmon) not in ipaddress.ip_network(ipv6_subnet):
                valid = False
                break
        except ValueError:
            valid = False
            break

    if type(ceph_monitors) is list and valid is True:             # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message}'
    else:
        if test_map_bit & fail:                                   # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message}'
        elif test_map_bit & warn:                                 # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return


# 5 ENV Tests
# 5.1 Keys
# 5.1.1 Validation of pod_number from Instantiated Metadata env file
def inst_env__pnum(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '5.1.1 Instanciated env `pod_number` - Pass - in range'
    warn_message   = '5.1.1 Instanciated env `pod_number` - Warn - not in range'
    fail_message   = '5.1.1 Instanciated env `pod_number` - Fail - not in range'
    ignore_message = '5.1.1 Instanciated env `pod_number` - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:                                       # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_metadata = get_instanciated_metadata()
    pod_number = instanciated_metadata['.env'].get('POD_NUMBER', -1)

    if int(pod_number) in range(0, 255):                            # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message}'
    else:
        if test_map_bit & fail:                                     # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message}'
        elif test_map_bit & warn:                                   # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return


# 5.1.2 Validation of pod_name from Instantiated Metadata .env
def inst_env__podn(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '5.1.2 Instanciated .env `pod_name` - Pass - Pod Name ='
    warn_message   = '5.1.2 Instanciated .env `pod_name` - Warn - Pod Name ='
    fail_message   = '5.1.2 Instanciated .env `pod_name` - Fail - Pod Name ='
    ignore_message = '5.1.2 Instanciated .env `pod_name` - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:                                       # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_metadata = get_instanciated_metadata()
    pod_name = instanciated_metadata['.env'].get('POD_NAME', '')

    if pod_name != '':                                              # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message} {pod_name}'
    else:
        if test_map_bit & fail:                                     # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message} {pod_name}'
        elif test_map_bit & warn:                                   # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message} {pod_name}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return


# 5.1.3 Validation of organization_url from Instantiated Metadata .env
def inst_env__podu(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '5.1.3 Instanciated .env `organization_url` - Pass - URL ='
    warn_message   = '5.1.3 Instanciated .env `organization_url` - Warn - URL ='
    fail_message   = '5.1.3 Instanciated .env `organization_url` - Fail - URL ='
    ignore_message = '5.1.3 Instanciated .env `organization_url` - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:                                       # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_metadata = get_instanciated_metadata()
    organization_url = instanciated_metadata['.env'].get('ORGANIZATION_URL', None)

    if organization_url not in ['', None]:                                              # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message} {organization_url}'
    else:
        if test_map_bit & fail:                                     # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message} {organization_url}'
        elif test_map_bit & warn:                                   # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message} {organization_url}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return


# 5.1.4 Validation of cloudcix_version from Instantiated Metadata .env
def inst_env__cixv(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '5.1.4 Instanciated .env `cloudcix_version` - Pass - Version ='
    warn_message   = '5.1.4 Instanciated .env `cloudcix_version` - Warn - Version ='
    fail_message   = '5.1.4 Instanciated .env `cloudcix_version` - Fail - Version ='
    ignore_message = '5.1.4 Instanciated .env `cloudcix_version` - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:                                       # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_metadata = get_instanciated_metadata()
    cloudcix_version = instanciated_metadata['.env'].get('CLOUDCIX_VERSION', '')

    if isinstance(cloudcix_version, int) is True:                   # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message} {cloudcix_version}'
    else:
        if test_map_bit & fail:                                     # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message} {cloudcix_version}'
        elif test_map_bit & warn:                                   # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message} {cloudcix_version}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return


# 5.1.5 Validation of docker_mgmt_ip6 from Instantiated Metadata .env
def inst_env__ipv6(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '5.1.5 Instanciated .env `docker_mgmt_ip6` - Pass - is Valid'
    warn_message   = '5.1.5 Instanciated .env `docker_mgmt_ip6` - Warn - is not Valid'
    fail_message   = '5.1.5 Instanciated .env `docker_mgmt_ip6` - Fail - is not Valid'
    ignore_message = '5.1.5 Instanciated .env `docker_mgmt_ip6` - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:                                       # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_metadata = get_instanciated_metadata()
    docker_mgmt_ip6 = instanciated_metadata['.env'].get('DOCKER_MGMT_IP6', '')
    ipv6_subnet = instanciated_metadata['config.json'].get('ipv6_subnet', '')

    try:
        docker_mgmt_ip6 = ipaddress.ip_network(docker_mgmt_ip6)
        ipv6_subnet = ipaddress.ip_network(ipv6_subnet)
        if docker_mgmt_ip6 in ipv6_subnet:
            in_range = True
        else:
            in_range = False
    except ValueError:
        in_range = False

    if in_range is True:                   # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message}'
    else:
        if test_map_bit & fail:                                     # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message}'
        elif test_map_bit & warn:                                   # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return


# 5.1.6 Validation of pms3 from Instantiated Metadata .env
def inst_env__pms3(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '5.1.6 Instanciated .env `pms3` - Pass - is Valid'
    warn_message   = '5.1.6 Instanciated .env `pms3` - Warn - is not Valid'
    fail_message   = '5.1.6 Instanciated .env `pms3` - Fail - is not Valid'
    ignore_message = '5.1.6 Instanciated .env `pms3` - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:                                       # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_metadata = get_instanciated_metadata()
    pms3 = instanciated_metadata['.env'].get('PMS3', '')
    primary_ipv4_subnet = instanciated_metadata['config.json'].get('primary_ipv4_subnet', '')

    try:
        pms3 = ipaddress.ip_address(pms3)
        primary_ipv4_subnet = ipaddress.ip_network(primary_ipv4_subnet)
        if pms3 in primary_ipv4_subnet:
            in_range = True
        else:
            in_range = False
    except ValueError:
        in_range = False

    if in_range is True:                                           # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message}'
    else:
        if test_map_bit & fail:                                     # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message}'
        elif test_map_bit & warn:                                   # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return


# 5.1.7 Validation of pms4 from Instantiated Metadata .env
def inst_env__pms4(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '5.1.7 Instanciated .env `pms4` - Pass - is Valid'
    warn_message   = '5.1.7 Instanciated .env `pms4` - Warn - is not Valid'
    fail_message   = '5.1.7 Instanciated .env `pms4` - Fail - is not Valid'
    ignore_message = '5.1.7 Instanciated .env `pms4` - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:                                       # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_metadata = get_instanciated_metadata()
    pms4 = instanciated_metadata['.env'].get('PMS4', '')
    primary_ipv4_subnet = instanciated_metadata['config.json'].get('primary_ipv4_subnet', '')

    try:
        pms4 = ipaddress.ip_address(pms4)
        primary_ipv4_subnet = ipaddress.ip_network(primary_ipv4_subnet)
        if pms4 in primary_ipv4_subnet:
            in_range = True
        else:
            in_range = False
    except ValueError:
        in_range = False

    if in_range is True:                                           # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message}'
    else:
        if test_map_bit & fail:                                     # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message}'
        elif test_map_bit & warn:                                   # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return


# 5.1.8 Validation of pms5 from Instantiated Metadata .env
def inst_env__pms5(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '5.1.8 Instanciated .env `pms5` - Pass - is Valid'
    warn_message   = '5.1.8 Instanciated .env `pms5` - Warn - is not Valid'
    fail_message   = '5.1.8 Instanciated .env `pms5` - Fail - is not Valid'
    ignore_message = '5.1.8 Instanciated .env `pms5` - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:                                       # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_metadata = get_instanciated_metadata()
    pms5 = instanciated_metadata['.env'].get('PMS5', '')
    primary_ipv4_subnet = instanciated_metadata['config.json'].get('primary_ipv4_subnet', '')

    try:
        pms5 = ipaddress.ip_address(pms5)
        primary_ipv4_subnet = ipaddress.ip_network(primary_ipv4_subnet)
        if pms5 in primary_ipv4_subnet:
            in_range = True
        else:
            in_range = False
    except ValueError:
        in_range = False

    if in_range is True:                                           # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message}'
    else:
        if test_map_bit & fail:                                     # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message}'
        elif test_map_bit & warn:                                   # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return


# 5.1.9 Validation of pms6 from Instantiated Metadata .env
def inst_env__pms6(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '5.1.9 Instanciated .env `pms6` - Pass - is Valid'
    warn_message   = '5.1.9 Instanciated .env `pms6` - Warn - is not Valid'
    fail_message   = '5.1.9 Instanciated .env `pms6` - Fail - is not Valid'
    ignore_message = '5.1.9 Instanciated .env `pms6` - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:                                       # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_metadata = get_instanciated_metadata()
    pms6 = instanciated_metadata['.env'].get('PMS6', '')
    primary_ipv4_subnet = instanciated_metadata['config.json'].get('primary_ipv4_subnet', '')

    try:
        pms6 = ipaddress.ip_address(pms6)
        primary_ipv4_subnet = ipaddress.ip_network(primary_ipv4_subnet)
        if pms6 in primary_ipv4_subnet:
            in_range = True
        else:
            in_range = False
    except ValueError:
        in_range = False

    if in_range is True:                                           # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message}'
    else:
        if test_map_bit & fail:                                     # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message}'
        elif test_map_bit & warn:                                   # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return


# 5.1.10 Validation of email_host from Instantiated Metadata .env
def inst_env__host(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '5.1.10 Instanciated .env `email_host` - Pass - is Valid'
    warn_message   = '5.1.10 Instanciated .env `email_host` - Warn - is not Valid'
    fail_message   = '5.1.10 Instanciated .env `email_host` - Fail - is not Valid'
    ignore_message = '5.1.10 Instanciated .env `email_host` - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:                                       # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_metadata = get_instanciated_metadata()
    email_host = instanciated_metadata['.env'].get('EMAIL_HOST', '')

    try:
        result = urlparse(email_host)
        # A valid URL should have at least a scheme and a netloc
        valid = all([result.scheme, result.netloc])
    except ValueError:
        valid = False

    if valid is True:                                           # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message}'
    else:
        if test_map_bit & fail:                                     # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message}'
        elif test_map_bit & warn:                                   # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return


# 5.1.11 Validation of email_user from Instantiated Metadata .env
def inst_env__user(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '5.1.11 Instanciated .env `email_user` - Pass - is Valid'
    warn_message   = '5.1.11 Instanciated .env `email_user` - Warn - is not Valid'
    fail_message   = '5.1.11 Instanciated .env `email_user` - Fail - is not Valid'
    ignore_message = '5.1.11 Instanciated .env `email_user` - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:                                       # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_metadata = get_instanciated_metadata()
    email_user = instanciated_metadata['.env'].get('EMAIL_USER', '')

    if validate_email(email_user) is True:                          # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message}'
    else:
        if test_map_bit & fail:                                     # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message}'
        elif test_map_bit & warn:                                   # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return


# 5.1.12 Validation of email_password from Instantiated Metadata .env
def inst_env__pass(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '5.1.12 Instanciated .env `email_password` - Pass - is Valid'
    warn_message   = '5.1.12 Instanciated .env `email_password` - Warn - is not Valid'
    fail_message   = '5.1.12 Instanciated .env `email_password` - Fail - is not Valid'
    ignore_message = '5.1.12 Instanciated .env `email_password` - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:                                       # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_metadata = get_instanciated_metadata()
    email_password = instanciated_metadata['.env'].get('EMAIL_PASSWORD', '')

    if email_password not in ['', None]:                            # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message}'
    else:
        if test_map_bit & fail:                                     # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message}'
        elif test_map_bit & warn:                                   # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return


# 5.1.13 Validation of email_port from Instantiated Metadata .env
def inst_env__port(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '5.1.13 Instanciated .env `email_port` - Pass - Port = '
    warn_message   = '5.1.13 Instanciated .env `email_port` - Warn - Port = '
    fail_message   = '5.1.13 Instanciated .env `email_port` - Fail - Port = '
    ignore_message = '5.1.13 Instanciated .env `email_port` - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:                                       # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_metadata = get_instanciated_metadata()
    email_port = instanciated_metadata['.env'].get('EMAIL_PORT', '')

    if isinstance(email_port, int) is True:                         # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message} {email_port}'
    else:
        if test_map_bit & fail:                                     # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message} {email_port}'
        elif test_map_bit & warn:                                   # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message} {email_port}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return


# 5.1.14 Validation of email_reply_to from Instantiated Metadata .env
def inst_env__reto(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '5.1.14 Instanciated .env `email_reply_to` - Pass - is Valid'
    warn_message   = '5.1.14 Instanciated .env `email_reply_to` - Warn - is not Valid'
    fail_message   = '5.1.14 Instanciated .env `email_reply_to` - Fail - is not Valid'
    ignore_message = '5.1.14 Instanciated .env `email_reply_to` - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:                                       # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_metadata = get_instanciated_metadata()
    email_reply_to = instanciated_metadata['.env'].get('EMAIL_REPLY_TO', '')

    if validate_email(email_reply_to) is True:                      # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message}'
    else:
        if test_map_bit & fail:                                     # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message}'
        elif test_map_bit & warn:                                   # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return


# 5.1.15 Validation of pat_name from Instantiated Metadata .env
def inst_env__patn(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '5.1.15 Instanciated .env `pat_name` - Pass - is Valid'
    warn_message   = '5.1.15 Instanciated .env `pat_name` - Warn - is not Valid'
    fail_message   = '5.1.15 Instanciated .env `pat_name` - Fail - is not Valid'
    ignore_message = '5.1.15 Instanciated .env `pat_name` - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:                                       # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_metadata = get_instanciated_metadata()
    pat_name = instanciated_metadata['.env'].get('PAT_NAME', '')

    if pat_name not in ['', None]:                                 # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message}'
    else:
        if test_map_bit & fail:                                     # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message}'
        elif test_map_bit & warn:                                   # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return


# 5.1.16 Validation of pat_organization_url from Instantiated Metadata .env
def inst_env__patu(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '5.1.16 Instanciated .env `pat_organization_url` - Pass - is Valid'
    warn_message   = '5.1.16 Instanciated .env `pat_organization_url` - Warn - is not Valid'
    fail_message   = '5.1.16 Instanciated .env `pat_organization_url` - Fail - is not Valid'
    ignore_message = '5.1.16 Instanciated .env `pat_organization_url` - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:                                       # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_metadata = get_instanciated_metadata()
    pat_organization_url = instanciated_metadata['.env'].get('PAT_ORGANIZATION_URL', '')

    if pat_organization_url not in ['', None]:
        valid = False
    else:
        try:
            result = urlparse(pat_organization_url)
            # A valid URL should have at least a scheme and a netloc
            valid = all([result.scheme, result.netloc])
        except ValueError:
            valid = False

    if valid is True:                                               # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message}'
    else:
        if test_map_bit & fail:                                     # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message}'
        elif test_map_bit & warn:                                   # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return


# 5.1.17 Validation of portal_name from Instantiated Metadata .env
def inst_env__pnam(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '5.1.17 Instanciated .env `portal_name` - Pass - is Valid'
    warn_message   = '5.1.17 Instanciated .env `portal_name` - Warn - is not Valid'
    fail_message   = '5.1.17 Instanciated .env `portal_name` - Fail - is not Valid'
    ignore_message = '5.1.17 Instanciated .env `portal_name` - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:                                       # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_metadata = get_instanciated_metadata()
    portal_name = instanciated_metadata['.env'].get('PORTAL_NAME', '')

    if portal_name not in ['', None]:                               # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message}'
    else:
        if test_map_bit & fail:                                     # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message}'
        elif test_map_bit & warn:                                   # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return


# 5.1.18 Validation of pgadmin_email from Instantiated Metadata .env
def inst_env__pgem(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '5.1.18 Instanciated .env `pgadmin_email` - Pass - is Valid'
    warn_message   = '5.1.18 Instanciated .env `pgadmin_email` - Warn - is not Valid'
    fail_message   = '5.1.18 Instanciated .env `pgadmin_email` - Fail - is not Valid'
    ignore_message = '5.1.18 Instanciated .env `pgadmin_email` - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:                                       # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_metadata = get_instanciated_metadata()
    pgadmin_email = instanciated_metadata['.env'].get('PGADMIN_EMAIL', '')

    if validate_email(pgadmin_email) is True:                       # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message}'
    else:
        if test_map_bit & fail:                                     # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message}'
        elif test_map_bit & warn:                                   # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return


# 5.1.19 Validation of pgadmin_password from Instantiated Metadata .env
def inst_env__pgpa(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '5.1.19 Instanciated .env `pgadmin_password` - Pass - is Valid'
    warn_message   = '5.1.19 Instanciated .env `pgadmin_password` - Warn - is not Valid'
    fail_message   = '5.1.19 Instanciated .env `pgadmin_password` - Fail - is not Valid'
    ignore_message = '5.1.19 Instanciated .env `pgadmin_password` - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:                                       # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_metadata = get_instanciated_metadata()
    pgadmin_password = instanciated_metadata['.env'].get('PGADMIN_PASSWORD', '')

    if pgadmin_password not in ['', None]:                            # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message}'
    else:
        if test_map_bit & fail:                                     # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message}'
        elif test_map_bit & warn:                                   # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return


# 5.1.20 Validation of cloudcix_api_username from Instantiated Metadata .env
def inst_env__apiu(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '5.1.20 Instanciated .env `cloudcix_api_username` - Pass - is Valid'
    warn_message   = '5.1.20 Instanciated .env `cloudcix_api_username` - Warn - is not Valid'
    fail_message   = '5.1.20 Instanciated .env `cloudcix_api_username` - Fail - is not Valid'
    ignore_message = '5.1.20 Instanciated .env `cloudcix_api_username` - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:                                       # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_metadata = get_instanciated_metadata()
    cloudcix_api_username = instanciated_metadata['.env'].get('CLOUDCIX_API_USERNAME', '')

    if validate_email(cloudcix_api_username) is True:               # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message}'
    else:
        if test_map_bit & fail:                                     # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message}'
        elif test_map_bit & warn:                                   # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return


# 5.1.21 Validation of cloudcix_api_password from Instantiated Metadata .env
def inst_env__apip(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '5.1.21 Instanciated .env `cloudcix_api_password` - Pass - is Valid'
    warn_message   = '5.1.21 Instanciated .env `cloudcix_api_password` - Warn - is not Valid'
    fail_message   = '5.1.21 Instanciated .env `cloudcix_api_password` - Fail - is not Valid'
    ignore_message = '5.1.21 Instanciated .env `cloudcix_api_password` - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:                                       # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_metadata = get_instanciated_metadata()
    cloudcix_api_password = instanciated_metadata['.env'].get('CLOUDCIX_API_PASSWORD', '')

    if cloudcix_api_password not in ['', None]:                     # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message}'
    else:
        if test_map_bit & fail:                                     # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message}'
        elif test_map_bit & warn:                                   # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return


# 5.1.22 Validation of cloudcix_api_key from Instantiated Metadata .env
def inst_env__apik(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '5.1.22 Instanciated .env `cloudcix_api_key` - Pass - is Valid'
    warn_message   = '5.1.22 Instanciated .env `cloudcix_api_key` - Warn - is not Valid'
    fail_message   = '5.1.22 Instanciated .env `cloudcix_api_key` - Fail - is not Valid'
    ignore_message = '5.1.22 Instanciated .env `cloudcix_api_key` - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:                                       # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_metadata = get_instanciated_metadata()
    cloudcix_api_key = instanciated_metadata['.env'].get('CLOUDCIX_API_KEY', '')

    if cloudcix_api_key not in ['', None]:                          # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message}'
    else:
        if test_map_bit & fail:                                     # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message}'
        elif test_map_bit & warn:                                   # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return


# 5.1.23 Validation of pod_secret_key from Instantiated Metadata .env
def inst_env__podk(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '5.1.23 Instanciated .env `pod_secret_key` - Pass - is Valid'
    warn_message   = '5.1.23 Instanciated .env `pod_secret_key` - Warn - is not Valid'
    fail_message   = '5.1.23 Instanciated .env `pod_secret_key` - Fail - is not Valid'
    ignore_message = '5.1.23 Instanciated .env `pod_secret_key` - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:                                       # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_metadata = get_instanciated_metadata()
    pod_secret_key = instanciated_metadata['.env'].get('POD_SECRET_KEY', '')

    if pod_secret_key not in ['', None]:                            # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message}'
    else:
        if test_map_bit & fail:                                     # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message}'
        elif test_map_bit & warn:                                   # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return


# 5.1.24 Validation of pgsqlapi_user from Instantiated Metadata .env
def inst_env__sqlu(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '5.1.24 Instanciated .env `pgsqlapi_user` - Pass - is Valid'
    warn_message   = '5.1.24 Instanciated .env `pgsqlapi_user` - Warn - is not Valid'
    fail_message   = '5.1.24 Instanciated .env `pgsqlapi_user` - Fail - is not Valid'
    ignore_message = '5.1.24 Instanciated .env `pgsqlapi_user` - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:                                       # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_metadata = get_instanciated_metadata()
    pgsqlapi_user = instanciated_metadata['.env'].get('PGSQLAPI_USER', '')

    if validate_email(pgsqlapi_user) is True:                       # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message}'
    else:
        if test_map_bit & fail:                                     # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message}'
        elif test_map_bit & warn:                                   # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return


# 5.1.25 Validation of pgsqlapi_password from Instantiated Metadata .env
def inst_env__sqlp(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '5.1.25 Instanciated .env `pgsqlapi_password` - Pass - is Valid'
    warn_message   = '5.1.25 Instanciated .env `pgsqlapi_password` - Warn - is not Valid'
    fail_message   = '5.1.25 Instanciated .env `pgsqlapi_password` - Fail - is not Valid'
    ignore_message = '5.1.25 Instanciated .env `pgsqlapi_password` - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:                                       # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_metadata = get_instanciated_metadata()
    pgsqlapi_password = instanciated_metadata['.env'].get('PGSQLAPI_PASSWORD', '')

    if pgsqlapi_password not in ['', None]:                         # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message}'
    else:
        if test_map_bit & fail:                                     # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message}'
        elif test_map_bit & warn:                                   # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return


# 5.1.26 Validation of pgsqltotp_user from Instantiated Metadata .env
def inst_env__otpu(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '5.1.26 Instanciated .env `pgsqltotp_user` - Pass - is Valid'
    warn_message   = '5.1.26 Instanciated .env `pgsqltotp_user` - Warn - is not Valid'
    fail_message   = '5.1.26 Instanciated .env `pgsqltotp_user` - Fail - is not Valid'
    ignore_message = '5.1.26 Instanciated .env `pgsqltotp_user` - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:                                       # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_metadata = get_instanciated_metadata()
    pgsqltotp_user = instanciated_metadata['.env'].get('PGSQLTOTP_USER', '')

    if validate_email(pgsqltotp_user) is True:                      # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message}'
    else:
        if test_map_bit & fail:                                     # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message}'
        elif test_map_bit & warn:                                   # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return


# 5.1.27 Validation of pgsqltotp_password from Instantiated Metadata .env
def inst_env__otpp(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '5.1.27 Instanciated .env `pgsqltotp_password` - Pass - is Valid'
    warn_message   = '5.1.27 Instanciated .env `pgsqltotp_password` - Warn - is not Valid'
    fail_message   = '5.1.27 Instanciated .env `pgsqltotp_password` - Fail - is not Valid'
    ignore_message = '5.1.27 Instanciated .env `pgsqltotp_password` - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:                                       # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_metadata = get_instanciated_metadata()
    pgsqltotp_password = instanciated_metadata['.env'].get('PGSQLTOTP_PASSWORD', '')

    if pgsqltotp_password not in ['', None]:                        # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message}'
    else:
        if test_map_bit & fail:                                     # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message}'
        elif test_map_bit & warn:                                   # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return


# 5.1.28 Validation of membershipldap_dc from Instantiated Metadata .env
def inst_env__mldc(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '5.1.28 Instanciated .env `membershipldap_dc` - Pass - is Valid'
    warn_message   = '5.1.28 Instanciated .env `membershipldap_dc` - Warn - is not Valid'
    fail_message   = '5.1.28 Instanciated .env `membershipldap_dc` - Fail - is not Valid'
    ignore_message = '5.1.28 Instanciated .env `membershipldap_dc` - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:                                       # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_metadata = get_instanciated_metadata()
    membershipldap_dc = instanciated_metadata['.env'].get('MEMBERSHIPLDAP_DC', '')

    if membershipldap_dc not in ['', None]:                      # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message}'
    else:
        if test_map_bit & fail:                                     # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message}'
        elif test_map_bit & warn:                                   # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return


# 5.1.29 Validation of membershipldap_password from Instantiated Metadata .env
def inst_env__mlpa(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '5.1.29 Instanciated .env `membershipldap_password` - Pass - is Valid'
    warn_message   = '5.1.29 Instanciated .env `membershipldap_password` - Warn - is not Valid'
    fail_message   = '5.1.29 Instanciated .env `membershipldap_password` - Fail - is not Valid'
    ignore_message = '5.1.29 Instanciated .env `membershipldap_password` - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:                                       # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_metadata = get_instanciated_metadata()
    membershipldap_password = instanciated_metadata['.env'].get('MEMBERSHIPLDAP_PASSWORD', '')

    if membershipldap_password not in ['', None]:                   # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message}'
    else:
        if test_map_bit & fail:                                     # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message}'
        elif test_map_bit & warn:                                   # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return


# 5.1.30 Validation of robot_api_username from Instantiated Metadata .env
def inst_env__robu(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '5.1.30 Instanciated .env `robot_api_username` - Pass - is Valid'
    warn_message   = '5.1.30 Instanciated .env `robot_api_username` - Warn - is not Valid'
    fail_message   = '5.1.30 Instanciated .env `robot_api_username` - Fail - is not Valid'
    ignore_message = '5.1.30 Instanciated .env `robot_api_username` - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:                                       # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_metadata = get_instanciated_metadata()
    robot_api_username = instanciated_metadata['.env'].get('ROBOT_API_USERNAME', '')

    if validate_email(robot_api_username) is True:                  # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message}'
    else:
        if test_map_bit & fail:                                     # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message}'
        elif test_map_bit & warn:                                   # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return


# 5.1.31 Validation of robot_api_password from Instantiated Metadata .env
def inst_env__robp(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '5.1.31 Instanciated .env `robot_api_password` - Pass - is Valid'
    warn_message   = '5.1.31 Instanciated .env `robot_api_password` - Warn - is not Valid'
    fail_message   = '5.1.31 Instanciated .env `robot_api_password` - Fail - is not Valid'
    ignore_message = '5.1.31 Instanciated .env `robot_api_password` - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:                                       # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_metadata = get_instanciated_metadata()
    robot_api_password = instanciated_metadata['.env'].get('ROBOT_API_PASSWORD', '')

    if robot_api_password not in ['', None]:                        # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message}'
    else:
        if test_map_bit & fail:                                     # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message}'
        elif test_map_bit & warn:                                   # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return


# 5.1.32 Validation of robot_api_key from Instantiated Metadata .env
def inst_env__robk(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '5.1.32 Instanciated .env `robot_api_key` - Pass - is Valid'
    warn_message   = '5.1.32 Instanciated .env `robot_api_key` - Warn - is not Valid'
    fail_message   = '5.1.32 Instanciated .env `robot_api_key` - Fail - is not Valid'
    ignore_message = '5.1.32 Instanciated .env `robot_api_key` - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:                                       # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_metadata = get_instanciated_metadata()
    robot_api_key = instanciated_metadata['.env'].get('ROBOT_API_KEY', '')

    if robot_api_key not in ['', None]:                          # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message}'
    else:
        if test_map_bit & fail:                                     # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message}'
        elif test_map_bit & warn:                                   # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return


# 5.1.33 Validation of cop_name from Instantiated Metadata .env
def inst_env__copn(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '5.1.33 Instanciated .env `cop_name` - Pass - is Valid'
    warn_message   = '5.1.33 Instanciated .env `cop_name` - Warn - is not Valid'
    fail_message   = '5.1.33 Instanciated .env `cop_name` - Fail - is not Valid'
    ignore_message = '5.1.33 Instanciated .env `cop_name` - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:                                       # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_metadata = get_instanciated_metadata()
    cop_name = instanciated_metadata['.env'].get('COP_NAME', '')

    if cop_name not in ['', None]:                                  # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message}'
    else:
        if test_map_bit & fail:                                     # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message}'
        elif test_map_bit & warn:                                   # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return


# 5.1.34 Validation of cop_organization_url from Instantiated Metadata .env
def inst_env__copu(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '5.1.34 Instanciated .env `cop_organization_url` - Pass - is Valid'
    warn_message   = '5.1.34 Instanciated .env `cop_organization_url` - Warn - is not Valid'
    fail_message   = '5.1.34 Instanciated .env `cop_organization_url` - Fail - is not Valid'
    ignore_message = '5.1.34 Instanciated .env `cop_organization_url` - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:                                       # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_metadata = get_instanciated_metadata()
    cop_organization_url = instanciated_metadata['.env'].get('COP_ORGANIZATION_URL', '')

    if cop_organization_url not in ['', None]:                      # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message}'
    else:
        if test_map_bit & fail:                                     # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message}'
        elif test_map_bit & warn:                                   # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return


# 5.1.35 Validation of cloudcix_lock_user from Instantiated Metadata .env
def inst_env__loku(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '5.1.35 Instanciated .env `cloudcix_lock_user` - Pass - is Valid'
    warn_message   = '5.1.35 Instanciated .env `cloudcix_lock_user` - Warn - is not Valid'
    fail_message   = '5.1.35 Instanciated .env `cloudcix_lock_user` - Fail - is not Valid'
    ignore_message = '5.1.35 Instanciated .env `cloudcix_lock_user` - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:                                       # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_metadata = get_instanciated_metadata()
    cloudcix_lock_user = instanciated_metadata['.env'].get('CLOUDCIX_LOCK_USER', '')

    if cloudcix_lock_user not in ['', None]:                      # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message}'
    else:
        if test_map_bit & fail:                                     # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message}'
        elif test_map_bit & warn:                                   # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return


# 5.1.36 Validation of cloudcix_lock_credentials from Instantiated Metadata .env
def inst_env__lokp(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '5.1.36 Instanciated .env `cloudcix_lock_credentials` - Pass - is Valid'
    warn_message   = '5.1.36 Instanciated .env `cloudcix_lock_credentials` - Warn - is not Valid'
    fail_message   = '5.1.36 Instanciated .env `cloudcix_lock_credentials` - Fail - is not Valid'
    ignore_message = '5.1.36 Instanciated .env `cloudcix_lock_credentials` - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:                                       # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_metadata = get_instanciated_metadata()
    cloudcix_lock_credentials = instanciated_metadata['.env'].get('CLOUDCIX_LOCK_CREDENTIALS', '')

    if cloudcix_lock_credentials not in ['', None]:                      # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message}'
    else:
        if test_map_bit & fail:                                     # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message}'
        elif test_map_bit & warn:                                   # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return


def is_host_reachable_verbose(host, count=4):
    success = False
    for i in range(count):
        response = ping(host)
        if response is not None:
            success = True
            break
    return success


# 6 Ping Tests
# 6.1 IPv4 addresses
# 6.1.1 Ping PE
def ping_ipv4___pe(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '6.1.1 Ping Test IPv4 PE - Pass - Success'
    warn_message   = '6.1.1 Ping Test IPv4 PE - Warn - Failed'
    fail_message   = '6.1.1 Ping Test IPv4 PE - Fail - Failed'
    ignore_message = '6.1.1 Ping Test IPv4 PE - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:  # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_metadata = get_instanciated_metadata()
    ipv4_link_pe = instanciated_metadata['config.json'].get('ipv4_link_pe', '127.0.0.127')

    if is_host_reachable_verbose(ipv4_link_pe):  # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message}'
    else:
        if test_map_bit & fail:  # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message}'
        elif test_map_bit & warn:  # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return


# 6.1.2 Ping CPE
def ping_ipv4__cpe(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '6.1.2 Ping Test IPv4 CPE - Pass - Success'
    warn_message   = '6.1.2 Ping Test IPv4 CPE - Warn - Failed'
    fail_message   = '6.1.2 Ping Test IPv4 CPE - Fail - Failed'
    ignore_message = '6.1.2 Ping Test IPv4 CPE - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:  # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_metadata = get_instanciated_metadata()
    ipv4_link_cpe = instanciated_metadata['config.json'].get('ipv4_link_cpe', '127.0.0.127')

    if is_host_reachable_verbose(ipv4_link_cpe):  # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message}'
    else:
        if test_map_bit & fail:  # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message}'
        elif test_map_bit & warn:  # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return


# 6.1.3 Ping 8.8.8.8
def ping_ipv4_8888(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '6.1.3 Ping Test IPv4 8.8.8.8 - Pass - Success'
    warn_message   = '6.1.3 Ping Test IPv4 8.8.8.8 - Warn - Failed'
    fail_message   = '6.1.3 Ping Test IPv4 8.8.8.8 - Fail - Failed'
    ignore_message = '6.1.3 Ping Test IPv4 8.8.8.8 - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:  # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    if is_host_reachable_verbose('8.8.8.8'):  # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message}'
    else:
        if test_map_bit & fail:  # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message}'
        elif test_map_bit & warn:  # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return


# 6.2 IPv6 addresses
# 6.2.1 Ping PE
def ping_ipv6___pe(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '6.2.1 Ping Test IPv6 PE - Pass - Success'
    warn_message   = '6.2.1 Ping Test IPv6 PE - Warn - Failed'
    fail_message   = '6.2.1 Ping Test IPv6 PE - Fail - Failed'
    ignore_message = '6.2.1 Ping Test IPv6 PE - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:  # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_metadata = get_instanciated_metadata()
    ipv6_link_pe = instanciated_metadata['config.json'].get('ipv6_link_pe', '::127')

    if is_host_reachable_verbose(ipv6_link_pe):  # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message}'
    else:
        if test_map_bit & fail:  # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message}'
        elif test_map_bit & warn:  # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return


# 6.2.2 Ping CPE
def ping_ipv6__cpe(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '6.2.2 Ping Test IPv6 CPE - Pass - Success'
    warn_message   = '6.2.2 Ping Test IPv6 CPE - Warn - Failed'
    fail_message   = '6.2.2 Ping Test IPv6 CPE - Fail - Failed'
    ignore_message = '6.2.2 Ping Test IPv6 CPE - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:  # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_metadata = get_instanciated_metadata()
    ipv6_link_cpe = instanciated_metadata['config.json'].get('ipv6_link_cpe', '::127')

    if is_host_reachable_verbose(ipv6_link_cpe):  # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message}'
    else:
        if test_map_bit & fail:  # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message}'
        elif test_map_bit & warn:  # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return


# 6.2.3 Ping 2001:4860:4860::8888
def ping_ipv6_8888(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '6.2.3 Ping Test IPv4 2001:4860:4860::8888 - Pass - Success'
    warn_message   = '6.2.3 Ping Test IPv4 2001:4860:4860::8888 - Warn - Failed'
    fail_message   = '6.2.3 Ping Test IPv4 2001:4860:4860::8888 - Fail - Failed'
    ignore_message = '6.2.3 Ping Test IPv4 2001:4860:4860::8888 - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:  # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    if is_host_reachable_verbose('2001:4860:4860::8888'):  # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message}'
    else:
        if test_map_bit & fail:  # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message}'
        elif test_map_bit & warn:  # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return


# 6.3 DNS hostnames
# 6.3.1 Ping www.google.com
def ping_dns__ggle(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '6.3.1 Ping Test www.google.com - Pass - Success'
    warn_message   = '6.3.1 Ping Test www.google.com - Warn - Failed'
    fail_message   = '6.3.1 Ping Test www.google.com - Fail - Failed'
    ignore_message = '6.3.1 Ping Test www.google.com - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:  # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    if is_host_reachable_verbose('www.google.com'):  # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message}'
    else:
        if test_map_bit & fail:  # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message}'
        elif test_map_bit & warn:  # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return
