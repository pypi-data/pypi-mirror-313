from ipaddress import IPv4Network


def get_ips(network: str) -> list[str]:
    network = [
        str(ip) for ip in IPv4Network('172.16.0.22', strict=False).hosts()
    ]
    return network
