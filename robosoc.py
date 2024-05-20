#!/usr/bin/env python3
# stdlib
import os
import shutil
from datetime import datetime
from string import Template
# lib
import ipaddress
from urllib.error import HTTPError
from urllib.request import urlretrieve
# local


template_robosoc = Template("""
table inet RoboSOC_Blocklist {
    set RoboSOC_ipv4 {
        type ipv4_addr
        flags interval
        elements = {
            $element_ipv4s
        }
    }

    set RoboSOC_ipv6 {
        type ipv6_addr
        flags interval
        elements = {
            $element_ipv6s
        }
    }

    chain RoboSOC_block_input {
        type filter hook input priority filter - 2; policy accept;
        ip saddr @RoboSOC_ipv4 drop
        ip6 saddr @RoboSOC_ipv6 drop
    }

    chain RoboSOC_block_output {
        type filter hook output priority filter - 2; policy accept;
        ip daddr @RoboSOC_ipv4 drop
        ip6 daddr @RoboSOC_ipv6 drop
    }

    chain RoboSOC_block_forward {
        type filter hook forward priority filter - 2; policy accept;
        ip saddr @RoboSOC_ipv4 drop
        ip6 saddr @RoboSOC_ipv6 drop
        ip daddr @RoboSOC_ipv4 drop
        ip6 daddr @RoboSOC_ipv6 drop
    }
}
""")


def download_ipblocklist(filename, path, url):
    """
    Downloads file from the given url to the given path
    :param filename: name of the file to be downloaded
    :param path: location of the file to be placed
    :param url: website link to download file
    :return: boolean: downloaded status
    """
    try:
        urlretrieve(url, f'{path}candidate_{filename}.txt')
        return True
    except HTTPError:
        return False


def get_publish_datetime(file_path):
    """
    Finds out the Published datetime from the ipblocklist text file
    :param file_path: string: given ipblocklist file path
    :return publish_datetime: string: Published datetime
    """
    publish_datetime = '00:00:00 01/01/2023'
    with open(file_path, 'r') as file:
        lines = file.readlines()
    for line in lines:
        if 'Published' in line:
            publish_datetime = line.split('@')[1].strip()
    return publish_datetime


def check_to_process_blocklist(candidate_file_path, active_file_path):
    """
    Collects the Publish datetime from both candidate and active files and compares.
    If candidate publish datetime is greater than active then sets process to True
    :param candidate_file_path: string: Candidate ipblocklist txt file path
    :param active_file_path: string: Active ipblocklist txt file path
    :return process: boolean: flag to continue the processing blocklist.
    """
    candidate_publish_datetime = get_publish_datetime(candidate_file_path)
    active_publish_datetime = get_publish_datetime(active_file_path)

    # Convert the strings to datetime objects
    candidate_publish_datetime_object = datetime.strptime(candidate_publish_datetime, '%H:%M:%S %d/%m/%y')
    active_publish_datetime_object = datetime.strptime(active_publish_datetime, '%H:%M:%S %d/%m/%y')

    # Compare the datetime objects
    process = False
    if candidate_publish_datetime_object > active_publish_datetime_object:
        process = True

    return process


def direct_load_robosoc_nft(path, ipv4s, ipv6s):
    """
    Generates /etc/cloudcix/robosoc/robosoc.nft from above defined template_robosoc template
    with all the ipv4 and ipv6 RoboSOC blocklist.
    :param path: '/etc/cloudcix/robosoc/'
    :param ipv4s: 'list of ipv4 addresses'
    :param ipv6s: 'list of ipv6 addresses'
    :return: None
    """
    nft_filename = 'robosoc.nft'
    # load the robosoc.j2 template and update with ipaddresses
    element_ipv4s = '{' + ', '.join(ipv4s) + '}'
    element_ipv6s = '{' + ', '.join(ipv6s) + '}'
    robosoc_template = template_robosoc.substitute({
        'element_ipv4s': element_ipv4s,
        'element_ipv6s': element_ipv6s,
    })
    # write to the robosoc.nft file
    with open(f'{path}{nft_filename}', 'w') as file:
        file.write(robosoc_template)

    # Restart the nftables
    os.system('sudo systemctl restart nftables')


def read_ipblocklist(file_path):
    """
    Reads IPaddresses from a file at given file_path
    :param file_path: location of the file to read ipaddresses
    :return: tuple of sets of ipv4 and ipv6 addresses
    """
    ipv4s = []
    ipv6s = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
    for line in lines:
        line = line.strip()
        if '#' not in line and line != '':
            if ':' not in line:
                try:
                    ip4 = str(ipaddress.ip_network(line, strict=False))
                    ipv4s.append(ip4)
                except ValueError:
                    pass
            if ':' in line:
                try:
                    ip6 = str(ipaddress.ip_network(line, strict=False))
                    ipv6s.append(ip6)
                except ValueError:
                    pass
    return set(ipv4s), set(ipv6s)


def compare_ipblocklist(candidate_file_path, active_file_path):
    """
    1. Finds ipv4s and ipv6s from the given files (candidate and active)
    2. Finds the differences between candidate and active sets
    3. Finds the removed ones and added ones for ipv4 and ipv6
    4. Returns a dictionary of removed and added ipv4s and ipv6s respectively.
    :param candidate_file_path: string: path to candidate ipblocklist
    :param active_file_path: string: path to active ipblocklist
    :return: dictionary with removed and added ipv4s and ipv6s
    """
    candidate_ipv4s, candidate_ipv6s = read_ipblocklist(candidate_file_path)
    active_ipv4s, active_ipv6s = read_ipblocklist(active_file_path)

    # Find the difference(the ones that are not common in two sets)
    difference_ipv4s = candidate_ipv4s ^ active_ipv4s
    difference_ipv6s = candidate_ipv6s ^ active_ipv6s

    # Find the removed (the ones that are only in difference and not in candidate)
    removed_ipv4s = difference_ipv4s - candidate_ipv4s
    removed_ipv6s = difference_ipv6s - candidate_ipv6s

    # Find the added (the ones that are only in difference and not in active)
    added_ipv4s = difference_ipv4s - active_ipv4s
    added_ipv6s = difference_ipv6s - active_ipv6s

    return {
        'removed_ipv4s': '{' + ', '.join(removed_ipv4s) + '}' if len(removed_ipv4s) > 0 else '',
        'removed_ipv6s': '{' + ', '.join(removed_ipv6s) + '}' if len(removed_ipv6s) > 0 else '',
        'added_ipv4s': '{' + ', '.join(added_ipv4s) + '}' if len(added_ipv4s) > 0 else '',
        'added_ipv6s': '{' + ', '.join(added_ipv6s) + '}' if len(added_ipv6s) > 0 else '',
    }


def apply_add_ips(element, version):
    """
    Adds element to the concerned Chain of RoboSOC_Blocklist nftable
    :param element: A string of set of ipaddresses e.g "{'1.1.1.1/32', '2.4.5.6/30'}"
    :param version: type 4 or 6 of IPaddress
    :return: None
    """
    if len(element):
        cmd = f'sudo nft add element inet RoboSOC_Blocklist RoboSOC_ipv{version} {element}'
        os.system(cmd)


def apply_remove_ips(element, version):
    """
    Deletes element to the concerned Chain of RoboSOC_Blocklist nftable
    :param element: A string of set of ipaddresses e.g "{'1.1.1.1/32', '2.4.5.6/30'}"
    :param version: type 4 or 6 of IPaddress
    :return: None
    """
    if len(element):
        cmd = f'sudo nft delete element inet RoboSOC_Blocklist RoboSOC_ipv{version} {element}'
        os.system(cmd)


def update_robosoc_nft_file():
    """
    Replaces the robosoc.nft with updated ipblocklist to store the changes.
    :return: None
    """
    os.system('sudo nft list table inet RoboSOC_Blocklist > /etc/cloudcix/robosoc/robosoc.nft')


def update_active_file(filename, path):
    """
    Moves the current candidate file to active file to given path
    :param filename: name of the file to be moved
    :param path: location of the file to be placed
    :return: None
    """
    shutil.move(f'{path}candidate_{filename}.txt', f'{path}active_{filename}.txt')


def process_robosoc_ipblocklist():
    """
    Processes RoboSOC blocklist:
    1. For first time, all the ipaddresses in candidate_ipblocklist.txt are loaded to nftables
    2. For not the first time, only the changes applied such as removing ipaddresses and adding ipaddresses.
    3. Updates the changes applied to robosoc.nft file
    4. Moves the downloaded candidate_ipblocklist.txt to active_ipblocklist.txt for comparing on next iterations.
    :return: None
    """
    filename = 'ipblocklist'
    path = '/etc/cloudcix/robosoc/'
    url = f'https://www.cloudcix.com/{filename}.txt'

    # First download the ipblocklist from website
    if not download_ipblocklist(filename, path, url):
        return

    # For the first time loading entire ip blocklist directly ie when no active ipblocklist
    if not os.path.exists(f'{path}active_{filename}.txt'):
        # delete any old robosoc.nft files from /etc/cloudcix/robosoc/robosoc.nft
        robosoc_nft_path = f'{path}robosoc.nft'
        if os.path.exists(robosoc_nft_path):
            os.remove(robosoc_nft_path)
        # Clear all robosoc ipblocklist from nftables
        os.system('sudo systemctl restart nftables')
        # supply the file and get the ipv4s and ipv6s
        all_ipv4s, all_ipv6s = read_ipblocklist(f'{path}candidate_{filename}.txt')
        # load directly into robosoc.nft file via robosoc.j2
        direct_load_robosoc_nft(path, all_ipv4s, all_ipv6s)

    # Not the First time, then unload removed and load the added only
    else:
        if check_to_process_blocklist(f'{path}candidate_{filename}.txt', f'{path}active_{filename}.txt'):
            # supply candidate (newly downloaded) and active (already present)
            processed_ips = compare_ipblocklist(f'{path}candidate_{filename}.txt', f'{path}active_{filename}.txt')
            # apply removed and then added ips
            apply_remove_ips(processed_ips['removed_ipv4s'], 4)
            apply_remove_ips(processed_ips['removed_ipv6s'], 6)
            apply_add_ips(processed_ips['added_ipv4s'], 4)
            apply_add_ips(processed_ips['added_ipv6s'], 6)
        else:
            #  Active ipblocklist is in sync with Candidate ipblocklist, remove downloaded candidate file
            os.remove(f'{path}candidate_{filename}.txt')
            return

    # update robosoc.nft file and move downloaded candidate file to active ipblocklist.txt file
    update_robosoc_nft_file()
    update_active_file(filename, path)
    return


if __name__ == '__main__':
    process_robosoc_ipblocklist()
