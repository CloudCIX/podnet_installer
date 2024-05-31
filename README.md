# podnet_installer

Installer Tasks:

1 Network
  - 1.1 Public Interface setup
    - 1.1.1 Connect the Public Interface 
    - 1.1.2 Scan for the Public Interface
    - 1.1.3 Configure the Public Interface(call primitive)
  - 1.2 Management Interface setup
    - 1.2.1 Connect the Mgmt Interface 
    - 1.2.2 Scan for the Mgmt Interface
    - 1.2.3 Configure the Mgmt Interface(call primitive)
  - 1.3 OOB Interface setup
    - 1.3.1 Connect the OOB Interface 
    - 1.3.2 Scan for the OOB Interface
    - 1.3.3 Configure the OOB Interface(call primitive)
  - 1.4 Private Interface setup
    - 1.4.1 Connect the Private Interface 
    - 1.4.2 Scan for the Private Interface
    - 1.4.3 Configure the Private Interface(call primitive)
  - 1.5 Inter Interface setup
    - 1.5.1 Connect the Inter Interface 
    - 1.5.2 Scan for the Inter Interface
    - 1.5.3 Configure the Inter Interface(call primitive)

2 Update config.json
  - 2.1 Update Interface names
    - 2.1.1 logical interface name for Public Interface
    - 2.1.2 logical interface name for Management Interface

3 Firewall 
  - 3.1 Prepare Firewall rules
    - 3.1.1 Inbound Rules IPv4
    - 3.1.2 Inbound Rules IPv6
    - 3.1.3 Forward Rules IPv4
    - 3.1.4 Forward Rules IPv6
    - 3.1.5 Outbound Rules IPv4
    - 3.1.6 Outbound Rules IPv6           
  - 3.2 Configure Firewall rules
    - 3.3.1 Call Primitive(call primitive)

4 RoboSOC
  - 4.1 set robosoc.py executable
  - 4.2 setup cron job
  
5 Docker Setup
  - 5.1 Setting up NFS mount drive
  - 5.2 Starting Docker container
  - 5.3 Setup_user_expiration_cron(cop)
  - 5.4 Setup_api_postgres_backup_cron(cop)
  - 5.5 Robot ssh key publish to podnet A(region)
  - 5.6 Robot ssh key publish to podnet B(region)
