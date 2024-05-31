# PAT Install Appliance A Configuration
# stdlib
import subprocess
# libs
import curses
from cloudcix.rcc import deploy_lsh, CouldNotExecuteException
from crontab import CronTab
# local
from sql_utils import get_instanciated_metadata


def disable_robot_password_ssh(podnet_ip):
    # move the robot.conf from /etc/cloudcix/pod/templates/robot.conf to /etc/ssh/sshd_config.d/robot.conf
    command = 'sudo cp /etc/cloudcix/pod/templates/robot.conf /etc/ssh/sshd_config.d/robot.conf 2>&1 && '
    command += 'sudo systemctl restart sshd > /dev/null 2>&1'

    # Deploy the bash script to the Host
    try:
        stdout, stderr = deploy_lsh(
            host_ip=podnet_ip,
            payload=command,
            username='robot',
        )
    except CouldNotExecuteException as e:
        return False, str(e)

    if stderr:
        return False, f'{stderr}'
    if stdout:
        return True, f'{stdout}'


def upload_ssh_key(podnet):
    # Note: password `cloudcix` is set during ISO preparation.
    os_cmd = 'sshpass -p cloudcix ssh-copy-id '
    os_cmd += '-o StrictHostKeyChecking=no '
    os_cmd += f'-i "/home/administrator/.ssh/id_rsa.pub" '
    os_cmd += f'robot@{podnet} > /dev/null 2>&1'
    try:
        subprocess.run(os_cmd, shell=True, check=True)
    except subprocess.CalledProcessError as error:
        return False, error
    return True, ''


def build(win):
    config = get_instanciated_metadata()['config.json']

    # 1 Network Setup
    # 1.1 Public Interface
    # Appliance has no Public Interface

    # 1.2 Management Interface
    # Management Interface is already configured by cloud-init's user-data for Appliance A

    # 1.3 OOB Interface
    # Appliance has no OOB Interface

    # 1.4 Private Interface
    # Appliance has no Private Interface

    # 1.5 Inter Interface
    # Appliance has no Inter Interface

    # 2 Update config.json
    # Not Applicable for Appliance

    # 3 Firewall setup
    # Not Applicable for Appliance

    # 4 RoboSOC setup
    # Not Applicable for Appliance

    # 5 Docker setup
    win.addstr(1, 1, '5 Docker Setup:                                 ', curses.color_pair(2))
    # 5.1 NFS mount drive
    win.addstr(2, 1, '5.1 Setting up NFS mount drive:                 ', curses.color_pair(2))
    win.refresh()
    network6 = config['ipv6_subnet'].split('/')[0]
    try:
        subprocess.run(
            f'sudo echo -e /etc/cloudcix/robot {network6}/64(rw,sync,no_subtree_check) >> /etc/exports',
            shell=True,
            check=True,
        )
        subprocess.run('sudo exportfs -a', shell=True, check=True)
        subprocess.run(
            'sudo systemctl restart nfs-kernel-server > /dev/null 2>&1',
            shell=True,
            check=True,
        )
        win.addstr(2, 1, '5.1 Setting up NFS mount drive:          SUCCESS', curses.color_pair(3))
        win.refresh()
    except subprocess.CalledProcessError as error:
        win.addstr(2, 1, '5.1 Setting up NFS mount drive:           FAILED', curses.color_pair(3))
        win.addstr(18, 1, f'Error: {error}', curses.color_pair(3))
        win.refresh()
        return False

    # 5.2 Start Docker services
    win.addstr(3, 1, '5.2 Starting Docker services:                   ', curses.color_pair(2))
    win.refresh()
    try:
        subprocess.run(
            'sudo docker-compose --file /etc/cloudcix/docker/docker-compose.yml up -d  > /dev/null 2>&1',
            shell=True,
            check=True,
        )
        win.addstr(3, 1, '5.2 Setting up NFS mount drive:          SUCCESS', curses.color_pair(3))
        win.refresh()
    except subprocess.CalledProcessError as error:
        win.addstr(3, 1, '5.2 Setting up NFS mount drive:           FAILED', curses.color_pair(3))
        win.addstr(18, 1, f'Error: {error}', curses.color_pair(3))
        win.refresh()
        return False

    # 5.3 Setup Cron job for User expiration notifications
    win.addstr(4, 1, '5.3 User expiration notifications:              ', curses.color_pair(2))
    win.refresh()
    with CronTab(user='root') as cron:
        jobs = cron.find_command('user_expiration_cron')
    if len(list(jobs)) == 0:
        with CronTab(user='root') as cron:
            job = cron.new('docker restart user_expiration_cron')
            job.setall('0 4 * * 1')
    win.addstr(4, 1, '5.3 User expiration notifications:       SUCCESS', curses.color_pair(2))
    win.refresh()

    # 5.4 Setup Cron job for backing up API PGSQL database
    win.addstr(5, 1, '5.4 Backing up API PGSQL database:              ', curses.color_pair(2))
    win.refresh()
    with CronTab(user='root') as cron:
        jobs = cron.find_command('pgsqlapi pg_dumpall')
    if len(list(jobs)) == 0:
        with CronTab(user='root') as cron:
            job = cron.new(
                'docker exec -t pgsqlapi pg_dumpall -F t -U postgres > api_backup_$(date +%d-%m-%y).tar'
            )
            job.setall('0 0 * * *')
    win.addstr(5, 1, '5.4 Backing up API PGSQL database:       SUCCESS', curses.color_pair(2))
    win.refresh()

    # 5.5 Robot ssh key publish to PodNet A
    win.addstr(6, 1, '5.5 Robot user ssh key access PodNet A:         ', curses.color_pair(2))
    win.refresh()
    podnet_a = f'{network6}10:0:2'
    attempt = 1
    key_uploaded = False
    while not key_uploaded:
        if upload_ssh_key(podnet_a):
            win.addstr(18, 1, 'Successfully uploaded Robot user ssh public key to PodNet A.', curses.color_pair(4))
            key_uploaded = True
        else:
            if attempt == 3 and not key_uploaded:
                msg = 'Failed to upload Robot user ssh public key. Ensure PodNet A is running and try again.'
                win.addstr(18, 1, msg, curses.color_pair(3))
                win.refresh()
                break
            attempt += 1
    # disable robot user ssh password access
    if key_uploaded and disable_robot_password_ssh(podnet_a):
        win.addstr(6, 1, '5.5 Robot user ssh key access PodNet A:  SUCCESS', curses.color_pair(4))
        win.refresh()
    else:
        win.addstr(6, 1, '5.5 Robot user ssh key access PodNet A:   FAILED', curses.color_pair(3))
        win.refresh()
        return False

    # 5.6 Robot ssh key publish to Podnet B
    win.addstr(7, 1, '5.6 Robot user ssh key access PodNet B:         ', curses.color_pair(2))
    win.refresh()
    podnet_b = f'{network6}10:0:3'
    attempt = 1
    key_uploaded = False
    while not key_uploaded:
        if upload_ssh_key(podnet_b):
            win.addstr(18, 1, 'Successfully uploaded Robot user ssh public key to PodNet B.', curses.color_pair(4))
            key_uploaded = True
        else:
            if attempt == 3 and not key_uploaded:
                msg = 'Failed to upload Robot user ssh public key. Ensure PodNet B is running and try again.'
                win.addstr(18, 1, msg, curses.color_pair(3))
                win.refresh()
                break
            attempt += 1
    # disable robot user ssh password access
    if key_uploaded and disable_robot_password_ssh(podnet_b):
        win.addstr(7, 1, '5.6 Robot user ssh key access PodNet B:  SUCCESS', curses.color_pair(4))
        win.refresh()
    else:
        win.addstr(7, 1, '5.6 Robot user ssh key access PodNet B:   FAILED', curses.color_pair(3))
        win.refresh()
        return False

    # Finish
    return True
