import time
import socket
import dns.resolver
import struct

def ping(host, num_of_requests):
    ip_address = check_host(host)
    if ip_address == -1:
        return

    num_of_lost = 0
    num_of_received = 0
    times = []

    print(f"\nPinging {host} ({ip_address}) with {num_of_requests} requests:\n")

    for _ in range(num_of_requests):
        start_time = time.time()
        try:
            send_icmp(ip_address)
            end_time = time.time()
            elapsed_time = (end_time - start_time) * 1000  
            times.append(elapsed_time)
            print(f"Reply from {ip_address}: time={elapsed_time:.2f}ms")
            num_of_received += 1
        except socket.error:
            print("Request timed out.")
            num_of_lost += 1

    packet_loss_percentage = (num_of_lost / num_of_requests) * 100 
    print(f"\nPing statistics for {host} ({ip_address}):")
    print(f"    Packets: Sent = {num_of_requests}, Received = {num_of_received}, Lost = {num_of_lost} ({packet_loss_percentage:.2f}%)\n")

    if num_of_received > 0:
        print(f"Approximate round trip times")
        print(f"    Minimum = {min(times):.2f}ms, Maximum = {max(times):.2f}ms, Average = {(sum(times) / num_of_received):.2f}ms")

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
    data = b'test' 
    icmp_checksum = calculate_checksum(header + data)
    header = struct.pack('!BBHHH', 8, 0, icmp_checksum, 111, 1)

    icmp_packet = header + data
    icmp_socket.sendto(icmp_packet, (host, 0))

    try:
        response, _ = icmp_socket.recvfrom(1024)
    except socket.timeout:
        raise socket.error
    finally:
        icmp_socket.close()

def calculate_checksum(data):
    checksum = 0
    for i in range(0, len(data), 2):
        checksum += (data[i] << 8) + data[i+1]
    checksum = (checksum >> 16) + (checksum & 0xFFFF)
    return (~checksum) & 0xFFFF

if __name__ == "__main__":
    host = input("Enter the domain / IP address: ")
    num_of_requests = int(input("Enter the number of requests: "))
    ping(host, num_of_requests)
