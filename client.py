from pingpong import *
from protocol import *
import icmp, time
from enum import Enum
import keyboard, random

class BallDirection(Enum):
    UL = 0
    UR = 1
    DR = 2
    DL = 3
    def bounce(self):
        return BallDirection((self.value - 1) % 4)
    def bounce2(self):
        return BallDirection((self.value + 1) % 4)
    def opposite(self):
        return BallDirection((self.value + 2) % 4)
    def moveBall(self, x, y):
        if self == BallDirection.UL:
            return (x-1, y-1)
        if self == BallDirection.UR:
            return (x+1, y-1)
        if self == BallDirection.DR:
            return (x+1, y+1)
        if self == BallDirection.DL:
            return (x-1, y+1)

# becomes opposite when it hits a wall or paddle

# for now it will go on forever, but I should add a winner packet or something

class Client:
    peerIP = "127.0.0.1"
    state = PingPong()

    def __init__(self, peerIP = "127.0.0.1"):
        self.peerIP = peerIP
        icmp.sendPing(peerIP, PaddlePositionPacket.encode(self.state.rightPaddlePosition))

    def update(self):
        receivedPacket = decodePacket(icmp.recvPingData(self.peerIP, 0.01)) # short timeout since we should already have data
#       print(receivedPacket)
        if type(receivedPacket) == tuple:
            self.state.ballPosition = receivedPacket
#            print("set pos")
        elif type(receivedPacket) == int:
            self.state.leftPaddlePosition = receivedPacket

    def movePaddle(self, up: bool):
        self.state.rightPaddlePosition += -1 if up else 1
        if self.state.rightPaddlePosition < 0:
            self.state.rightPaddlePosition = 0
        if self.state.rightPaddlePosition > self.state.BOARD_SIZE[1]:
            self.state.rightPaddlePosition = self.state.BOARD_SIZE[1]
        icmp.sendPing(self.peerIP, PaddlePositionPacket.encode(self.state.rightPaddlePosition))

    def mainloop(self):
        keyboard.on_press_key("up", lambda _: self.movePaddle(True))
        keyboard.on_press_key("down", lambda _: self.movePaddle(False))
        while True:
            try:
                self.update()
                self.state.render()
                time.sleep(0.01)
            except KeyboardInterrupt:
                break

client = Client(input("Host IP: "))
client.mainloop()