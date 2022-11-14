#!/usr/bin/env python3
import socket

serverip = 0
with open('server-ip.txt', 'r') as f:
    serverip = f.readlines()[0].rstrip()

# HOST = "localhost"
HOST = serverip
PORT = 9889


def getItem(cmd1, c):
    getcmd = cmd1.split()
    res = c.recv(9542).decode()
    print(res)


def setItem(cmd1, c):
    value = input()
    if not value:
        print("CLIENT_ERROR PROTOCOL WAS NOT FOLLOWED")
        c.close()
    c.send(value.encode())
    status = c.recv(9542).decode()
    print(status)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c:
    c.connect((HOST, PORT))

    # while True:
    print("\n ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ CLIENT MENU ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(
        "\n ~~~~~~ Enter GET/SET operations as specified: get KEY {1,2,3} / set KEY len(VALUE) {1,2,3} \\n VALUE ~~~~~~~")
    print("######################################## Choose from storage options : ########################################\n")
    print("                                               1 - NATIVE STORAGE                                              \n")
    print("                                               2 - FIRESTORE                               \n")
    print("                                               3 - GOOGLE CLOUD BUCKET STORAGE         \n")
    cmd1 = input()
    c.send(cmd1.encode())
    if cmd1[:3] == "set":
        setItem(cmd1, c)
    elif cmd1[:3] == "get":
        getItem(cmd1, c)
    else:
        error = c.recv(9542).decode()
        # print(error)
