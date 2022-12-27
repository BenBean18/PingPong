from pingpong import *
from protocol import *
import icmp, time
from enum import Enum
import keyboard, random

class BallDirection(Enum):
    L = -2
    R = -1
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

class Host:
    peerIP = "127.0.0.1"
    ballDirection = BallDirection.UL
    state = PingPong()
    lastUpdatedBall = None

    def __init__(self, peerIP = "127.0.0.1"):
        self.peerIP = peerIP
        self.state.ballPosition = (1,1)
        icmp.sendPing(peerIP, BallPositionPacket.encode(self.state.ballPosition[0], self.state.ballPosition[1]))
        icmp.sendPing(peerIP, PaddlePositionPacket.encode(self.state.leftPaddlePosition))
        self.lastUpdatedBall = time.time()
    
    def paddleBounce(self):
        print("paddle bounce")
        if self.state.ballPosition[0] < 2:
            self.ballDirection = BallDirection.UR if (self.state.ballPosition[1] - self.state.leftPaddlePosition + (self.state.PADDLE_HEIGHT/2)) / self.state.PADDLE_HEIGHT < 0 else BallDirection.DR
        else:
            self.ballDirection = BallDirection.UL if (self.state.ballPosition[1] - self.state.rightPaddlePosition + (self.state.PADDLE_HEIGHT/2)) / self.state.PADDLE_HEIGHT < 0 else BallDirection.DL

    def isInACorner(self):
        (x, y) = self.state.ballPosition
        maxX, maxY = self.state.BOARD_SIZE
        return (x <= 0 and y <= 0) or (x >= maxX and y <= 0) or (x <= 0 and y >= maxY) or (x >= maxX and y >= maxY)

    def doABounce(self):
        # worst physics ever
        direction = BallDirection(0)
        while True:
            ballPos = direction.moveBall(self.state.ballPosition[0], self.state.ballPosition[1])
            if self.isInACorner():
                self.ballDirection = self.ballDirection.opposite()
                return
            elif (direction == self.ballDirection.opposite()) or ballPos[0] < 0 or ballPos[0] > self.state.BOARD_SIZE[0] or ballPos[1] < 0 or ballPos[1] > self.state.BOARD_SIZE[1]:
                direction = BallDirection((direction.value+1) % 4)
            else:
                self.ballDirection = direction
                return

    def physicsUpdate(self):
        receivedPacket = decodePacket(icmp.recvPingData(self.peerIP, 0.01)) # short timeout since we should already have data
        if type(receivedPacket) == tuple:
            print("I'm the host...the heck?")
        elif type(receivedPacket) == int:
            self.state.rightPaddlePosition = receivedPacket
        if self.state.ballPosition[0] <= 0 or self.state.ballPosition[0] > self.state.BOARD_SIZE[0]:
            self.doABounce()
            self.state.ballPosition = (self.state.BOARD_SIZE[0] // 2, self.state.BOARD_SIZE[1] // 2)
        elif (self.state.ballPosition[0] == 0 and self.state.ballPosition[1] == 0) or (self.state.ballPosition[0] == self.state.BOARD_SIZE[0] and self.state.ballPosition[1] == self.state.BOARD_SIZE[1])\
            or (self.state.ballPosition[0] == 0 and self.state.ballPosition[1] == self.state.BOARD_SIZE[1]) or (self.state.ballPosition[0] == self.state.BOARD_SIZE[0] and self.state.ballPosition[1] == 0):
            self.doABounce()
        elif self.state.ballPosition[1] > self.state.BOARD_SIZE[1] or self.state.ballPosition[1] <= 0:
            self.doABounce()
        elif (self.state.ballPosition[0] == 1 and self.state.ballPosition[1] >= self.state.leftPaddlePosition and self.state.ballPosition[1] <= self.state.leftPaddlePosition + self.state.PADDLE_HEIGHT)\
            or\
            (self.state.ballPosition[0] == self.state.BOARD_SIZE[0]-1 and self.state.ballPosition[1] >= self.state.rightPaddlePosition and self.state.ballPosition[1] <= self.state.rightPaddlePosition + self.state.PADDLE_HEIGHT):
            self.paddleBounce()
        self.state.ballPosition = self.ballDirection.moveBall(self.state.ballPosition[0], self.state.ballPosition[1])
        self.lastUpdatedBall = time.time()
        icmp.sendPing(self.peerIP, BallPositionPacket.encode(self.state.ballPosition[0], self.state.ballPosition[1]))

    def movePaddle(self, up: bool):
        self.state.leftPaddlePosition += -1 if up else 1
        if self.state.leftPaddlePosition < 0:
            self.state.leftPaddlePosition = 0
        if self.state.leftPaddlePosition > self.state.BOARD_SIZE[1]:
            self.state.leftPaddlePosition = self.state.BOARD_SIZE[1]
        icmp.sendPing(self.peerIP, PaddlePositionPacket.encode(self.state.leftPaddlePosition))

    def mainloop(self):
        keyboard.on_press_key("up", lambda _: self.movePaddle(True))
        keyboard.on_press_key("down", lambda _: self.movePaddle(False))
        while True:
            try:
                self.state.render()
                self.physicsUpdate()
                time.sleep(0.1)
            except KeyboardInterrupt:
                break

host = Host(input("Client IP: "))
host.mainloop()