import socket
from _thread import *
from player import Player
import pickle
import sys

server = "192.168.1.116"
#This is the local ip adress as gotten from the command prompt using "ipconfig" and looking at
#IPv4 Address . . . . . . . . .
port = 5555

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
try:
    s.bind((server,port))
except socket.error as e:
    str(e)

s.listen(2) # Number of people who can connect to the server
print("Waiting for connection, Server has Started")
players=[Player((0,0),100,100,(80,170,80)),Player((100,100),100,100,(170,80,80))]


def read_pos(str):
    str= str.split(",")
    return (int(str[0]),int(str[1]))
def make_pos(tup):
    return "{},{}".format(tup[0],tup[1])

def threaded_client(uconn,player):
    uconn.send(pickle.dumps(players[player]))
    reply=''
    while True:
        try: # Don't know if we'll run into an error, but if so, break
            data=pickle.loads(uconn.recv(2048))#Receiving 2048 bits at maximum
            players[player]=data
            # reply=data.decode("utf-8")# Not sure what this does
            reply=players[(player+1)%2]
            if not data:  #If no data, we'vedisconnected
                print("Disconnected")
                break
            else:
                print("Received: ",data)
                print("Sending: ",reply)
            uconn.sendall(pickle.dumps(reply))
        except:
            break
    print("Lost Connection")
    uconn.close

currentPlayer=0
while True:
    conn, addr = s.accept() #Connection is an object, adrress is an ip adress
    print("Connected to:",addr)
    start_new_thread(threaded_client,(conn,currentPlayer))
    currentPlayer+=1
