# Ping Pong

## Pong over ICMP

This is Pong over `ping`, aka ping pong :) It worked best on Linux for me, although theoretically it should work on any platform.

## Instructions
- Run one instance of `host.py` on one machine, and one instance of `client.py` on another machine. Both of these programs need to run as administrator to be able to access raw sockets used for ICMP.
- Enter the IP address of the other machine into each machine when you are prompted.
- Play Pong! To move your paddle, press the up or down arrow.

## Dependencies
- The `keyboard` module for detecting arrow key presses, available from PyPI