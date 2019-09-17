#!~/.pyvenvs/e2e_lan
# -*- coding: utf-8 -*-

"""Module Summary

Additional details...

Functions
-----------
f(str, int): finds the int in the str and returns the index
"""

import os
import sys
import platform
import socket
import select
import json
import lan_socket
import subprocess
import termcolor

# OS = platform.system()

# if OS == "Darwin":
# 	# mac-os notifications
# 	def notify(title, text):
# 		os.system(f"""
# 				  osascript -e 'display notification "{text}" with title "{title}"'
# 				  """)

# else:
# 	# linux notifications
# 	def notify(text):
# 		os.system('notify-send '+text);


def encode(message):
    return int(message.encode("utf-8").hex(), 16)


def decode(message):
    return bytearray.fromhex(hex(message)[2:]).decode("utf-8")


def prompt():
    print(termcolor.colored("> ", "red"), end="", flush=True)


def main(args):
    socket1 = lan_socket.LanSocket()

    socket1.listen("localhost", 8080)

    prompt()

    while True:
        socket_list = [sys.stdin, socket1.sock_listen]

        # Get the list sockets which are readable
        read_sockets, _, _ = select.select(socket_list, [], [])

        for sock in read_sockets:
            # incoming message from remote server
            if sock == socket1.sock_listen:
                data = socket1.receive()
                if not data:
                    print("\nDisconnected")
                    break
                else:
                    print(termcolor.colored("> ", "green"), data)
                    prompt()

            else:
                msg = sys.stdin.readline()
                socket1.send(msg)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
    # subprocess.call('python test.py', shell=True)
