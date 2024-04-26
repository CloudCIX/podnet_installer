import os
import subprocess

__all__ = [
    'validate_hardware',
]


def podnet_min_hardware_requirements():
    # Minimum requirements
    min_cores = 4
    min_storage = 300  # in GB, per drive
    min_ram = 24  # in GB
    min_network_ports = 5
    min_network_speed = 1  # in Gbps
    return min_cores, min_storage, min_ram, min_network_ports, min_network_speed


def appliance_min_hardware_requirements():
    # Minimum requirements
    min_cores = 4
    min_storage = 300  # in GB, per drive
    min_ram = 24  # in GB
    min_network_ports = 1
    min_network_speed = 1  # in Gbps
    return min_cores, min_storage, min_ram, min_network_ports, min_network_speed


# Function to gather hardware information using subprocess
def validate_hardware(installer_type):
    # collect the minimum values
    if installer_type == 'podnet':
        min_cores, min_storage, min_ram, min_network_ports, min_network_speed = podnet_min_hardware_requirements()
    elif installer_type == 'appliance':
        min_cores, min_storage, min_ram, min_network_ports, min_network_speed = appliance_min_hardware_requirements()

    # Gather processor information
    lscpu_output = subprocess.run(['lscpu'], capture_output=True, text=True).stdout
    cores = 0
    for line in lscpu_output.split('\n'):
        if 'CPU(s):' in line and ' CPU(s)' not in line:
            cores = int(line.split(':')[1].strip())

    # Gather storage information
    lsblk_output = subprocess.run(['lsblk', '-o', 'SIZE,TYPE'], capture_output=True, text=True).stdout
    storage_gb = 0
    for line in lsblk_output.split('\n'):
        if 'disk' in line:
            size = line.split()[0]
            # Convert size to GB
            if 'G' in size:
                storage_gb += int(size.replace('G', ''))
            elif 'T' in size:
                storage_gb += int(float(size.replace('T', '')) * 1024)

    # Gather memory information
    meminfo_output = subprocess.run(['grep', 'MemTotal', '/proc/meminfo'], capture_output=True, text=True).stdout
    mem_total_kb = int(meminfo_output.split(':')[1].strip().split()[0])
    ram_gb = mem_total_kb / 1024 / 1024  # Convert KB to GB

    # Gather network information
    network_ports = [port for port in os.listdir('/sys/class/net/') if port not in ['lo', 'docker0']]
    network_speed = 1  # in Gbps
    for port in network_ports:
        # Use ethtool to get the details of the network interface
        eth_output = subprocess.run(['ethtool', port], capture_output=True, text=True).stdout
        for line in eth_output.split('\n'):
            if 'Speed:' in line and 'Unknown' not in line:
                # Extract the speed value from the line
                speed_mbps = line.split(':')[1].strip('Mb/s')
                speed_gbps = int(speed_mbps) / 1000  #  Convert Mbps to Gbps
                if network_speed < speed_gbps:
                    network_speed = speed_gbps

    # Compare hardware information with minimum requirements
    requirements_met = True
    error_list = []

    if cores < min_cores:
        error_list.append(f"Test (1.3.1): Processor cores insufficient. Minimum: {min_cores}, Found: {cores}")
        requirements_met = False

    if storage_gb < min_storage:
        error_list.append(
            f"Test (1.3.2): Storage insufficient. Minimum: {min_storage}GB, Found: {storage_gb}GB",
        )
        requirements_met = False

    if ram_gb < min_ram:
        error_list.append(f"Test (1.3.3): Memory insufficient. Minimum: {min_ram}GB, Found: {ram_gb:.2f}GB")
        requirements_met = False

    if len(network_ports) < min_network_ports:
        error_list.append(f"Test (1.3.4): Network ports insufficient. Minimum: {min_network_ports}, Found: {len(network_ports)}")
        requirements_met = False

    if network_speed < min_network_speed:
        error_list.append(f"Test (1.3.5): Network speed insufficient. Minimum: {min_network_speed} Gbps, Found: {network_speed} Gbps")
        requirements_met = False

    return requirements_met, error_list
