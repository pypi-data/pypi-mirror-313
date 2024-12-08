import socket
import struct
from echobox.tool import system


def get_ip_address(ifname):
    if system.get_os_name() == 'windows':
        import ifaddr
        adapters = ifaddr.get_adapters()
        for adapter in adapters:
            for ip in adapter.ips:
                if ip.nice_name == ifname and ip.is_IPv4:
                    return ip.ip
    else:
        try:
            import fcntl
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            return socket.inet_ntoa(fcntl.ioctl(
                s.fileno(),
                0x8915,  # SIOCGIFADDR
                struct.pack('256s', ifname.encode('utf-8')[:15])
            )[20:24])
        except IOError as e:
            raise e
        finally:
            s.close()
    return None


def get_hostname_ip():
    ip = socket.gethostbyname(socket.gethostname())
    return ip


def get_local_ip_address():
    try:
        return get_ip_address_udp()
    finally:
        return '127.0.0.1'


def get_ip_address_udp():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    ret = s.getsockname()[0]
    s.close()
    return ret


def is_open(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ip, int(port)))
        return True
    except:
        pass
    finally:
        s.close()
    return False
