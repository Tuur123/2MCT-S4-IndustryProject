import os
import sys
import getopt

argv = sys.argv[1:]

fps=30
treshhold=0.5
maxClients=5
gDriveAuthKey="ya29.a0AfH6SMB3dGAYotHUuc3vaG6FNznrwMcYVRu4hfg1oig5F7MNhyG2AFkkNSa6P6qZuFVRSrL9OMOD_Oa0zCZxBnGny6s_tcGDMICQozoFgHLg52uF-vynow8FguJg9R1Icy7b6WSn5MAirq0cr4HiRtRfkx_m"

try:
    opts, args = getopt.getopt(argv, "hftca", ["help", "fps=", "treshhold=", "maxClients=", "authKey="])
except getopt.GetoptError:
    print('server.py -f <fps> -t <treshhold> -c <maxClients> -a <google drive auth key>')
    sys.exit(2)

try: 
    for opt, arg in opts:
        if opt == '-h':
            print('server.py -f <fps> -t <treshhold> -c <maxClients> -a <google drive auth key>')
            sys.exit()

        elif opt in ("-f", "--fps"):
            fps = int(arg)

        elif opt in ("-t", "--treshhold"):
            treshhold = float(arg)

        elif opt in ("-c", "--maxClients"):
            maxClients = int(arg)

        elif opt in ("-a", "--authKey"):
            gDriveAuthKey = arg

except ValueError as e:
    print(e)

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import socket
import threading
from clienthandler import ClientHandler

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((socket.gethostname(), 9999))
serversocket.listen(maxClients)


def startFileServer():
    os.system('py fileServer.py')

fileServerThread = threading.Thread(target=startFileServer)
fileServerThread.start()

print("SERVER STARTED")



try:
    while True:
        clientSocket, address = serversocket.accept()

        print('\nConnected to: ' + address[0] + ':' + str(address[1]))
        clh = ClientHandler(clientSocket, fps, treshhold, gDriveAuthKey)
        clh.start()


except KeyboardInterrupt:
    serversocket.close()
    fileServerThread.join()
    print("Closing")