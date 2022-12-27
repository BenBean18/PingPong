import struct
# Host/client architecture, lower IP is host
# Data needed to transmit:
# Host -> Client: 
# - Ball position
# - Host paddle position
# Client -> Host:
# - Client paddle position

# Board is 80 x 40, and is limited to not being over 256 x 256.
# so storing top of paddle.
# paddle is 5 tall.

# I'll just use a byte each to make it easy

# Pass just the received packet data to this
class BallPositionPacket:
    def decode(data: bytes):
        if b"!b" not in data:
            raise Exception("BallPositionPacket: No header found")
        elif len(data) != 4:
            raise Exception("BallPositionPacket: Invalid packet length")
        elif data[:2] != b"!b":
            raise Exception("BallPositionPacket: Incorrect header placement")
        else:
            return (data[2], data[3])
    def encode(x: int, y: int):
        return b"!b"+bytes([x, y])

class PaddlePositionPacket:
    def decode(data: bytes):
        if b"!p" not in data:
            raise Exception("PaddlePositionPacket: No header found")
        elif len(data) != 3:
            raise Exception("PaddlePositionPacket: Invalid packet length")
        elif data[:2] != b"!p":
            raise Exception("PaddlePositionPacket: Incorrect header placement")
        else:
            return data[2]
    def encode(paddleTop: int):
        return b"!p"+bytes([paddleTop])

def decodePacket(data: bytes):
    if b"!b" in data:
        # Ball position packet
        return BallPositionPacket.decode(b"!b"+data.split(b"!b")[1])
    elif b"!p" in data:
        # Paddle position packet
        return PaddlePositionPacket.decode(b"!p"+data.split(b"!p")[1])
