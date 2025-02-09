import socket
import threading
import time
from scapy.all import ARP, Ether, srp

# Function to scan the network and find all live devices
def network_scan(target_ip):
    print("Scanning network for live hosts...")
    # Create ARP request packet to get the MAC addresses of all live devices in the network
    arp_request = ARP(pdst=target_ip)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request

    # Send the packet and receive responses
    answered_list = srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    
    devices = []
    for element in answered_list:
        device_info = {'ip': element[1].psrc, 'mac': element[1].hwsrc}
        devices.append(device_info)
    
    return devices

# Function to scan a single port on a device
def scan_port(host, port, open_ports):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)  # Timeout after 1 second
    try:
        sock.connect((host, port))
        open_ports.append(port)
    except (socket.timeout, socket.error):
        pass
    finally:
        sock.close()

# Function to scan all ports on a given host
def scan_device_ports(host, ports):
    open_ports = []
    print(f"Scanning {host} for open ports...")
    threads = []
    
    # Scanning ports in parallel using threads
    for port in ports:
        thread = threading.Thread(target=scan_port, args=(host, port, open_ports))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()

    return open_ports

# Main function to start the scan
def main(target_network, port_range):
    # Discover live hosts in the given network range
    devices = network_scan(target_network)
    
    if not devices:
        print("No live hosts found in the network.")
        return

    print(f"Found {len(devices)} devices in the network:\n")
    for device in devices:
        print(f"IP: {device['ip']} | MAC: {device['mac']}")
    
    print("\nStarting port scan...")
    
    # Define the range of ports to scan
    start_port, end_port = port_range
    
    # Scan each device for open ports
    for device in devices:
        open_ports = scan_device_ports(device['ip'], range(start_port, end_port + 1))
        if open_ports:
            print(f"\nOpen ports on {device['ip']} ({device['mac']}):")
            for port in open_ports:
                print(f"  - Port {port} is OPEN")
        else:
            print(f"\nNo open ports found on {device['ip']} ({device['mac']})")
    
# Run the program
if __name__ == "__main__":
    target_network = input("Enter the target network range (e.g., 192.168.1.0/24): ")
    start_port = int(input("Enter the starting port number: "))
    end_port = int(input("Enter the ending port number: "))
    
    main(target_network, (start_port, end_port))
