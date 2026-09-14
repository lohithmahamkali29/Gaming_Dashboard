import socket


def discover_subnet(prefix=None, port=20777, timeout=0.08):
    """Best-effort UDP discovery; unavailable hosts are silently skipped."""
    prefix = prefix or _local_prefix()
    found = []
    for host_number in range(1, 255):
        host = f'{prefix}.{host_number}'
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(timeout)
        try:
            sock.sendto(b'RACE_CONTROL_DISCOVER', (host, port))
            found.append({'ip_address': host, 'port': port})
        except OSError:
            pass
        finally:
            sock.close()
    return found


def _local_prefix():
    try:
        local_ip = socket.gethostbyname(socket.gethostname())
    except socket.error:
        local_ip = '127.0.0.1'
    return '.'.join(local_ip.split('.')[:3])
