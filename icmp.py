import socket, time
icmp = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)

def sendPing(ip: str, data: bytes):
    icmp.settimeout(None)
    icmp.sendto(b"b'E\x00\x00<\xcd\x01\x00\x00\x80\x01\x87C\xc0\xa82\xf6\xc0\xa825\x08\x00L\xf6\x00\x01\x00e" + data, (ip, 0))

# sendPing(icmp, "127.0.0.1", b"!!!Pickle Sandwiches")

def recvPingData(desiredIP: str, timeout: float):
    icmp.settimeout(timeout)
    start = time.time()
    while (time.time() - start) < timeout:
        try:
            (data, (ip, port)) = icmp.recvfrom(1024)
            if ip != desiredIP:
                continue
            else:
                return data
        except socket.timeout:
            return b""

# time.sleep(5.0)
# print(recvPingData("192.168.50.53", 0.01))