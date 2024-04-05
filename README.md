# podnet_installer

This installer performs the following tasks

1. Asks to choose between PodNet A and B
2. Finds out the public interface name and adds it to config.json file
3. Continuously scans for new interfaces, as a new interface detected asks and configures it, so it completes all other
   network interfaces.
4. Applys RoboSOC Blocklist addresses by creating a cron job that periodically(every 15min) reads the robosoc_ip_blocklist