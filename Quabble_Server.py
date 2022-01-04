import socket
from _thread import *
from Player_Class import Player
import pickle
import sys

server = "192.168.1.116"
#This is the local ip adress as gotten from the command prompt using "ipconfig" and looking at
#IPv4 Address . . . . . . . . .
port = 5745

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
try:
    s.bind((server,port))
except socket.error as e:
    str(e)

s.listen(2) # Number of people who can connect to the server
print("Waiting for connection, Server has Started")
players=[]
turn=0
B=[]
game_active=False

def read_pos(str):
    str= str.split(",")
    return (int(str[0]),int(str[1]))
def make_pos(tup):
    return "{},{}".format(tup[0],tup[1])

def threaded_client(uconn,player):
    global turn,B,drawing_tiles,players
    uconn.send(pickle.dumps(3))
    print("made the connection")
    reply=''
    while True:
        try: # Don't know if we'll run into an error, but if so, break
            recieved=pickle.loads(uconn.recv(2048))#Receiving 2048 bits at maximum
            if not recieved:  #If no data, we'vedisconnected
                print("Disconnected")
                break
            # print(recieved[0])
            # print("Data recieved is ",recieved[1])
            action,data=recieved
            if action=="pass":
                uconn.sendall(pickle.dumps(False))
            elif action=="drawing":
                for i in data:
                    drawing_tiles.append(i)
                uconn.sendall(pickle.dumps(True))
            elif action=="new player":
                players.append(data)
                # print(players)
                uconn.sendall(pickle.dumps(players))
            elif action=="goodbye":
                print("Trying to remove player {}".format(data))
                # print(data in players)
                for p in players:
                    if p.name==data.name:
                        players.remove(p)
                # players.remove(data)
                # print(currentPlayer)
                # print("goodbye")
                # uconn.sendall(pickle.dumps((0,0)))
                print([p.name for p in players])
                uconn.sendall(pickle.dumps(players))
            elif action=="get players":
                uconn.sendall(pickle.dumps(players))
            elif action=="make move":
                if B!=data:
                    B=data
                    turn+=1
                    turn%=len(players)
                uconn.sendall(pickle.dumps(True))

            # reply=data.decode("utf-8")# Not sure what this does
            # reply=players[(player+1)%2]
                # print("Received: ",data)
                # print("Sending: ",reply)
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
