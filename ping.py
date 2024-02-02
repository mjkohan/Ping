import dns.resolver
import socket
import struct


def ping(host, num_of_requests):
    ip_address = check_host(host)
    if ip_address == -1:
        return
    print(ip_address)

def check_host(host):
    try:
        ip_address = dns.resolver.resolve(host, 'A')[0].address
        return ip_address
    except dns.resolver.NXDOMAIN:
        print(f"Error: Unable to resolve {host}")
        return -1
    except dns.resolver.NoAnswer:
        print(f"Error: No IP address found for {host}")
        return -1
def send_icmp(host):

    icmp_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    icmp_socket.settimeout(1)
    header = struct.pack('!BBHHH', 8, 0, 0, 111, 1)
    data = b'Hello, ICMP!' 
    icmp_checksum = calculate_checksum(header + data)
    header = struct.pack('!BBHHH', 8, 0, icmp_checksum, 111, 1)
    icmp_packet = header + data
    icmp_socket.sendto(icmp_packet, (host, 0))
    try:
        response, _ = icmp_socket.recvfrom(1024)

    except socket.timeout:
        raise socket.error

    icmp_socket.close()

def calculate_checksum(data):
    checksum = 0
    for i in range(0, len(data), 2):
        checksum += (data[i] << 8) + data[i+1]
    checksum = (checksum >> 16) + (checksum & 0xFFFF)
    return (~checksum) & 0xFFFF
if __name__ == "__main__":

    host = input("Enter the domain / IP address : ")
    num_of_requests = int(input("Enter the number of requests: "))
    ping(host, num_of_requests)

   


    
