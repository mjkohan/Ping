import dns.resolver


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

if __name__ == "__main__":

    host = input("Enter the domain / IP address : ")
    num_of_requests = int(input("Enter the number of requests: "))
    ping(host, num_of_requests)

   


    
