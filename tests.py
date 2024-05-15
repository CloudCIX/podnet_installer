# stdlib
import ipaddress
import os
# lib
import psutil
# local
from interface_utils import read_interface_file
from sql_utils import (
    # blends
    cop_blend,
    copregion_blend,
    pat_blend,
    region_blend,
    # methods
    get_cidata,
    get_instanciated_infra,
    get_instanciated_metadata,
    get_test_details,
    region_flavor,
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
def hard_ram_count(test_id, ram_min):
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
    instanciated_metadata = get_instanciated_metadata()

    pass_message   = '2.4.1 Hardware private0  - Pass - Operstate = '
    warn_message   = '2.4.1 Hardware private0  - Warn - Operstate = '
    fail_message   = '2.4.1 Hardware private0  - Fail - Operstate = '
    ignore_message = '2.4.1 Hardware private0  - Ignore'

    test_map_bit = 2**test_id
    instanciated_blend = instanciated_metadata['config.json'].get('blend', 0)

    if test_map_bit & ignore or (region_flavor & instanciated_blend == 0): # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    operstate = read_interface_file('private0', 'operstate')

    if operstate == 'up':                                                  # Test pass
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
    instanciated_metadata = get_instanciated_metadata()

    pass_message   = '2.4.2 Hardware private0  - Pass - Carrier = '
    warn_message   = '2.4.2 Hardware private0  - Warn - Carrier = '
    fail_message   = '2.4.2 Hardware private0  - Fail - Carrier = '
    ignore_message = '2.4.2 Hardware private0  - Ignore'

    test_map_bit = 2**test_id
    instanciated_blend = instanciated_metadata['config.json'].get('blend', 0)

    if test_map_bit & ignore or (region_flavor & instanciated_blend == 0): # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    carrier = read_interface_file('private0', 'carrier')

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

# 2.4.3 Private Port Ethernet Name - Region Flavor Pods
def hard_priv_ethn(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()
    instanciated_metadata = get_instanciated_metadata()

    pass_message   = '2.4.3 Hardware private0  - Pass - Ethernet Name Match'
    warn_message   = '2.4.3 Hardware private0  - Warn - Ethernet Name = '
    fail_message   = '2.4.3 Hardware private0  - Fail - Ethernet Name = '
    ignore_message = '2.4.3 Hardware private0  - Ignore'

    test_map_bit = 2**test_id
    instanciated_blend = instanciated_metadata['config.json'].get('blend', 0)

    if test_map_bit & ignore or (region_flavor & instanciated_blend == 0): # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_infra = get_instanciated_infra()
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

# 2.5.1 Inter Port Operstate - Region Flavor Pods
def hard_intr_oper(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()
    instanciated_metadata = get_instanciated_metadata()

    pass_message   = '2.5.1 Hardware inter0  - Pass - Operstate = '
    warn_message   = '2.5.1 Hardware inter0  - Warn - Operstate = '
    fail_message   = '2.5.1 Hardware inter0  - Fail - Operstate = '
    ignore_message = '2.5.1 Hardware inter0  - Ignore'

    test_map_bit = 2**test_id

    instanciated_blend = instanciated_metadata['config.json'].get('blend', 0)
    if test_map_bit & ignore or (region_flavor & instanciated_blend == 0): # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    operstate = read_interface_file('inter0', 'operstate')

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

# 2.5.2 Inter Port Carrier - Region Flavor Pods
def hard_intr_carr(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()
    instanciated_metadata = get_instanciated_metadata()

    pass_message   = '2.5.2 Hardware inter0  - Pass - Carrier = '
    warn_message   = '2.5.2 Hardware inter0  - Warn - Carrier = '
    fail_message   = '2.5.2 Hardware inter0  - Fail - Carrier = '
    ignore_message = '2.5.2 Hardware inter0  - Ignore'

    test_map_bit = 2**test_id
    instanciated_blend = instanciated_metadata['config.json'].get('blend', 0)

    if test_map_bit & ignore or (region_flavor & instanciated_blend == 0): # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    carrier = read_interface_file('inter0', 'carrier')

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

# 2.5.3 Inter Port Ethernet Name - Region Flavor Pods
def hard_intr_ethn(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()
    instanciated_metadata = get_instanciated_metadata()

    pass_message   = '2.5.3 Hardware inter0  - Pass - Ethernet Name Match'
    warn_message   = '2.5.3 Hardware inter0  - Warn - Ethernet Name = '
    fail_message   = '2.5.3 Hardware inter0  - Fail - Ethernet Name = '
    ignore_message = '2.5.3 Hardware inter0  - Ignore'

    test_map_bit = 2**test_id
    instanciated_blend = instanciated_metadata['config.json'].get('blend', 0)

    if test_map_bit & ignore or (region_flavor & instanciated_blend == 0): # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_infra = get_instanciated_infra()
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

# 3.1.1 Instanciated and CIDATA config.json match
def config_matches(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '3.1.1 Instanciated and CIDATA config.json  - Pass - match'
    warn_message   = '3.1.1 Instanciated and CIDATA config.json  - Warn - not a match '
    fail_message   = '3.1.1 Instanciated and CIDATA config.json  - Fail - not a match'
    ignore_message = '3.1.1 Instanciated and CIDATA config.json  - Ignore'

    test_map_bit = 2**test_id

    if test_map_bit & ignore:                                           # Test Ignore
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

    if test_map_bit & ignore:  # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_metadata = get_instanciated_metadata()
    pod_number = instanciated_metadata['config.json'].get('pod_number', -1)

    if int(pod_number) in range(0, 255):  # Test pass
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


# 3.2.2 Validation of pod_name from Instantiated Metadata config.json
def inst_conf_pnam(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '3.2.2 Instanciated config.json `pod_name` - Pass - Pod Name ='
    warn_message   = '3.2.2 Instanciated config.json `pod_name` - Warn - Pod Name ='
    fail_message   = '3.2.2 Instanciated config.json `pod_name` - Fail - Pod Name ='
    ignore_message = '3.2.2 Instanciated config.json `pod_name` - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:  # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_metadata = get_instanciated_metadata()
    pod_name = instanciated_metadata['config.json'].get('pod_name', '')

    if pod_name != '':  # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message} {pod_name}'
    else:
        if test_map_bit & fail:  # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message} {pod_name}'
        elif test_map_bit & warn:  # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message} {pod_name}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return


# 3.2.3 Validation of blend from Instantiated Metadata config.json
def inst_conf_blen(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '3.2.3 Instanciated config.json `blend` - Pass - Valid'
    warn_message   = '3.2.3 Instanciated config.json `blend` - Warn - Invalid'
    fail_message   = '3.2.3 Instanciated config.json `blend` - Fail - Invalid'
    ignore_message = '3.2.3 Instanciated config.json `blend` - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:  # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_metadata = get_instanciated_metadata()
    blend = instanciated_metadata['config.json'].get('blend', 0)

    if int(blend) in [cop_blend, copregion_blend, pat_blend, region_blend]:  # Test pass
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


# 3.2.4 Validation of `podnet_a_enable` from Instantiated Metadata config.json
def inst_conf_aena(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '3.2.4 Instanciated config.json `podnet_a_enable` - Pass - is False'
    warn_message   = '3.2.4 Instanciated config.json `podnet_a_enable` - Warn - is True'
    fail_message   = '3.2.4 Instanciated config.json `podnet_a_enable` - Fail - is True'
    ignore_message = '3.2.4 Instanciated config.json `podnet_a_enable` - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:  # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_metadata = get_instanciated_metadata()
    podnet_a_enable = instanciated_metadata['config.json'].get('podnet_a_enable', True)

    if podnet_a_enable is False:  # Test pass
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


# 3.2.5 Validation of `podnet_a_enable` from Instantiated Metadata config.json
def inst_conf_aenb(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '3.2.5 Instanciated config.json `podnet_a_enable` - Pass - Boolean'
    warn_message   = '3.2.5 Instanciated config.json `podnet_a_enable` - Warn - not Boolean'
    fail_message   = '3.2.5 Instanciated config.json `podnet_a_enable` - Fail - not Boolean'
    ignore_message = '3.2.5 Instanciated config.json `podnet_a_enable` - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:  # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_metadata = get_instanciated_metadata()
    podnet_a_enable = instanciated_metadata['config.json'].get('podnet_a_enable', 123)

    if type(podnet_a_enable) is bool:  # Test pass
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


# 3.2.6 Validation of `podnet_b_enable` from Instantiated Metadata config.json
def inst_conf_bena(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '3.2.6 Instanciated config.json `podnet_b_enable` - Pass - is False'
    warn_message   = '3.2.6 Instanciated config.json `podnet_b_enable` - Warn - is True'
    fail_message   = '3.2.6 Instanciated config.json `podnet_b_enable` - Fail - is True'
    ignore_message = '3.2.6 Instanciated config.json `podnet_b_enable` - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:  # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_metadata = get_instanciated_metadata()
    podnet_b_enable = instanciated_metadata['config.json'].get('podnet_b_enable', True)

    if podnet_b_enable is False:  # Test pass
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


# 3.2.7 Validation of `podnet_b_enable` from Instantiated Metadata config.json
def inst_conf_benb(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '3.2.7 Instanciated config.json `podnet_b_enable` - Pass - Boolean'
    warn_message   = '3.2.7 Instanciated config.json `podnet_b_enable` - Warn - not Boolean'
    fail_message   = '3.2.7 Instanciated config.json `podnet_b_enable` - Fail - not Boolean'
    ignore_message = '3.2.7 Instanciated config.json `podnet_b_enable` - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:  # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_metadata = get_instanciated_metadata()
    podnet_b_enable = instanciated_metadata['config.json'].get('podnet_b_enable', 123)

    if type(podnet_b_enable) is bool:  # Test pass
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


# 3.2.8 Validation of `podnet_a_enable` and `podnet_b_enable` from Instantiated Metadata config.json
def inst_conf_aben(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '3.2.8 Instanciated config.json `podnet_a_enable` and `podnet_b_enable` - Pass - both are not True'
    warn_message   = '3.2.8 Instanciated config.json `podnet_a_enable` and `podnet_b_enable` - Warn - both are True'
    fail_message   = '3.2.8 Instanciated config.json `podnet_a_enable` and `podnet_b_enable` - Fail - both are True'
    ignore_message = '3.2.8 Instanciated config.json `podnet_a_enable` and `podnet_b_enable` - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:  # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_metadata = get_instanciated_metadata()
    podnet_a_enable = instanciated_metadata['config.json'].get('podnet_a_enable', True)
    podnet_b_enable = instanciated_metadata['config.json'].get('podnet_b_enable', True)

    if podnet_a_enable is True and podnet_b_enable is True:
        if test_map_bit & fail:  # Test fail
            fail_map += test_map_bit
            result[test_id] = f'{fail_message}'
        elif test_map_bit & warn:  # Test warn
            warn_map += test_map_bit
            result[test_id] = f'{warn_message}'
    else:  # Test pass
        pass_map += test_map_bit
        result[test_id] = f'{pass_message}'
    update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
    return


# 3.2.9 Validation of `ipv4_link_subnet` from Instantiated Metadata config.json
def inst_conf_ip4l(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '3.2.9 Instanciated config.json `ipv4_link_subnet` range - Pass - is >= /29'
    warn_message   = '3.2.9 Instanciated config.json `ipv4_link_subnet` range - Warn - is not >= /29'
    fail_message   = '3.2.9 Instanciated config.json `ipv4_link_subnet` range - Fail - is not >= /29'
    ignore_message = '3.2.9 Instanciated config.json `ipv4_link_subnet` range - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:  # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_metadata = get_instanciated_metadata()
    mask = instanciated_metadata['config.json'].get('ipv4_link_subnet', '0.0.0.0/30').split('/')[1]

    if int(mask) <= 29:  # Test pass
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


# 3.2.10 Validation of `ipv6_link_subnet` from Instantiated Metadata config.json
def inst_conf_ip6l(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '3.2.10 Instanciated config.json `ipv6_link_subnet` range - Pass - is >= /126'
    warn_message   = '3.2.10 Instanciated config.json `ipv6_link_subnet` range - Warn - is not >= /126'
    fail_message   = '3.2.10 Instanciated config.json `ipv6_link_subnet` range - Fail - is not >= /126'
    ignore_message = '3.2.10 Instanciated config.json `ipv6_link_subnet` range - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:  # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_metadata = get_instanciated_metadata()
    mask = instanciated_metadata['config.json'].get('ipv6_link_subnet', '::/127').split('/')[1]

    if int(mask) <= 126:  # Test pass
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


# 3.2.11 Validation of `primary_ipv4_subnet` from Instantiated Metadata config.json
def inst_conf_ip4s(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '3.2.11 Instanciated config.json `primary_ipv4_subnet` range - Pass - is >= /29'
    warn_message   = '3.2.11 Instanciated config.json `primary_ipv4_subnet` range - Warn - is not >= /29'
    fail_message   = '3.2.11 Instanciated config.json `primary_ipv4_subnet` range - Fail - is not >= /29'
    ignore_message = '3.2.11 Instanciated config.json `primary_ipv4_subnet` range - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:  # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_metadata = get_instanciated_metadata()
    mask = instanciated_metadata['config.json'].get('primary_ipv4_subnet', '0.0.0.0/30').split('/')[1]

    if int(mask) <= 29:  # Test pass
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


# 3.2.12 Validation of `ipv6_subnet` from Instantiated Metadata config.json
def inst_conf_ip6s(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '3.2.12 Instanciated config.json `ipv6_subnet` range - Pass - is >= /48'
    warn_message   = '3.2.12 Instanciated config.json `ipv6_subnet` range - Warn - is not >= /48'
    fail_message   = '3.2.12 Instanciated config.json `ipv6_subnet` range - Fail - is not >= /48'
    ignore_message = '3.2.12 Instanciated config.json `ipv6_subnet` range - Ignore'

    test_map_bit = 2 ** test_id

    if test_map_bit & ignore:  # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

    instanciated_metadata = get_instanciated_metadata()
    mask = instanciated_metadata['config.json'].get('ipv6_subnet', '::/127').split('/')[1]

    if int(mask) <= 48:  # Test pass
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


# 3.2.13 Validation of `dns_ips` from Instantiated Metadata config.json
def inst_conf_dnss(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '3.2.13 Instanciated config.json `dns_ips` - Pass - all are valid IPs'
    warn_message   = '3.2.13 Instanciated config.json `dns_ips` - Warn - all are not valid IPs'
    fail_message   = '3.2.13 Instanciated config.json `dns_ips` - Fail - all are not valid IPs'
    ignore_message = '3.2.13 Instanciated config.json `dns_ips` - Ignore'

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
            ipaddress.ip_address(dns_ip)
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


# 3.2.14 Validation of `ceph_monitors` from Instantiated Metadata config.json
def inst_conf_cmon(test_id):
    result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map = get_test_details()

    pass_message   = '3.2.13 Instanciated config.json `ceph_monitors` - Pass - is list and all are valid IPs'
    warn_message   = '3.2.13 Instanciated config.json `ceph_monitors` - Warn - Invalid'
    fail_message   = '3.2.13 Instanciated config.json `ceph_monitors` - Fail - Invalid'
    ignore_message = '3.2.13 Instanciated config.json `ceph_monitors` - Ignore'

    test_map_bit = 2 ** test_id
    instanciated_metadata = get_instanciated_metadata()
    instanciated_blend = instanciated_metadata['config.json'].get('blend', 0)

    if test_map_bit & ignore or (region_flavor & instanciated_blend == 0): # Test Ignore
        ignore_map += test_map_bit
        result[test_id] = ignore_message
        update_test_details(result, fail, ignore, warn, fail_map, warn_map, ignore_map, pass_map)
        return

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

    if type(ceph_monitors) is list and valid is True:  # Test pass
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