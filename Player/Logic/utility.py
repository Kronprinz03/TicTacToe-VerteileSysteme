import netifaces

def get_local_ip():
    for interface in netifaces.interfaces():
        addresses = netifaces.ifaddresses(interface)
        ipv4_info = addresses.get(netifaces.AF_INET)

        if ipv4_info:
            for link in ipv4_info:
                ip = link.get('addr')
                if ip and not ip.startswith('127.'):
                    return ip
    return 'localhost' 