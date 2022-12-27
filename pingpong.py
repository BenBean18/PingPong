class PingPong:
    BOARD_SIZE = (80, 20)
    PADDLE_HEIGHT = 5
    
    ballPosition = (1, 1)
    # this is updated by host only
    leftPaddlePosition = 8 # host
    rightPaddlePosition = 8 # client

    def render(self):
        s = ""
        s += "\033[2J" # clear screen
        for y in range(self.BOARD_SIZE[1]):
            for x in range(self.BOARD_SIZE[0]):
                if x == 0 and y >= self.leftPaddlePosition and y <= self.leftPaddlePosition + self.PADDLE_HEIGHT:
                    s += "\u2588"
                elif x == self.BOARD_SIZE[0]-1 and y >= self.rightPaddlePosition and y <= self.rightPaddlePosition + self.PADDLE_HEIGHT:
                    s += "\u2588"
                elif x == self.ballPosition[0] and y == self.ballPosition[1]:
                    s += "\033[34m\u2588\033[37m"
                else:
                    s += "\u2591"
            s += "\n"
        print(s, end="", flush=True)

#PingPong().render()