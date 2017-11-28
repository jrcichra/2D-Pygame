import socket
import _thread
import copy

def listen(i):

    id = copy.deepcopy(i)
    #Send the player data to all other players
    while True:
        try:
            size = int(clients[id].recv(5).decode('utf-8'))
            data = clients[id].recv(size)
            for c in clients:
                if c != clients[id]:
                    string = '%000005i' % size
                    c.send(str(string).encode('utf-8'))
                    c.send(data)
        except:
            print ('Some network issue server side, flushing and continuing')
            clients[id].recv(9999)

clients = []
addresses = []

s = socket.socket()
s.bind(('',12345))

id = 0

#get clients
while True:
    s.listen(5)
    c, addr = s.accept()
    print('Got connection from ',addr)
    c.send(str(id).encode('utf-8'))
    clients.append(c)
    addresses.append(addr)
    try:
        _thread.start_new_thread(listen,(id,))
    except Exception as e:
        print (e.__doc__)
        print ("Couldn't spawn thread for id: " + str(id))
    id+=1
