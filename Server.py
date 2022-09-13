import threading
import socket

clients = []

def main():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind(('localhost', 9999))
        server.listen()
    except:
        return print('\nIt was not possible to start the server!\n')

    while True:
        client, addr = server.accept()
        clients.append(client)

        thread = threading.Thread(target=messagesTreatment, args=[client])
        thread.start()

def messagesTreatment(client):
    while True:
        try:
            msg = client.recv(2048)
            msg_aux = msg.split()
            amount_received = int(msg_aux[2])
            hash_received = msg_aux[1]
            sender = msg_aux[0]
            print('\nThe user : ',sender, ' - Transferred : ', amount_received, ' - To the address containing the hash:', hash_received)
            broadcast(msg, client)
        except:
            deleteClient(client)
            break


def broadcast(msg, client):
    for clientItem in clients:
        if clientItem != client:
            try:
                clientItem.send(msg)
            except:
                deleteClient(clientItem)


def deleteClient(client):
    clients.remove(client)

main()