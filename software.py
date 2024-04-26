import subprocess


__all__ = [
    'validate_software',
]


def podnet_software_requirements():
    return ['ethtool', 'strongswan', 'nftables']


def appliance_software_requirements():
    return [
        'ethtool', 'docker', 'nginx', 'apt-transport-https', 'ca-certificates', 'curl',
        'gnupg-agent', 'apache2', 'openssl', 'certbot', 'software-properties-common', 'sshpass',
    ]


def validate_software(installer_type):
    # collect the minimum values
    if installer_type == 'podnet':
        required_packages = podnet_software_requirements()
    elif installer_type == 'appliance':
        required_packages = appliance_software_requirements()

    requirements_met = True
    error_list = []

    # Check operating system
    # Using lsb_release command to get the distribution information
    distro_info = subprocess.run(['lsb_release', '-a'], capture_output=True, text=True).stdout
    os_version = None
    for line in distro_info.split('\n'):
        if 'Release:' in line:
            os_version = line.split(':')[1].strip()
            break

    # Check if the OS version is Ubuntu 22.04 or higher
    if os_version:
        if float(os_version) < 22.04:
            error_list.append(
                f"Test (1.4.1): Operating System version '{os_version}'"
                f" does not meet the minimum requirement of Ubuntu 22.04 or higher.",
            )
            requirements_met = False
    else:
        error_list.append("Test (1.4.2):Unable to determine the operating system version.")
        requirements_met = False

    # Check if required packages are installed
    for i, package in enumerate(required_packages):
        package_check = subprocess.run(['dpkg-query', '-W', '-f=${Status}', package], capture_output=True, text=True)
        if 'install ok installed' not in package_check.stdout:
            error_list.append(f"Test (1.4.{3+i})Package '{package}' is not installed.")
            requirements_met = False

    return requirements_met, error_list
