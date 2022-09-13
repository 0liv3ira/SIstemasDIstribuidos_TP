import threading
import socket
import secrets
from traceback import print_tb
import time


global my_hash
global balance

def main():

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect(('localhost', 9999))
    except:
        return print('\nIt was not possible to connect to the server!\n')

    global balance
    global my_hash

    balance = 10
    my_hash = secrets.token_hex()

    username = input('Enter the node name :')
    print('\nName :',username, ' - Hash:', my_hash, " - Balance :", balance )
    print('\nConnected')

    thread1 = threading.Thread(target=receiveMessages, args=[client])
    thread2 = threading.Thread(target=sendMessages, args=[client, username])
    thread3 = threading.Thread(target=updateHash, args=[client])

    thread1.start()
    thread2.start()
    thread3.start()


def receiveMessages(client):
    global balance
    global my_hash

    while True:
        try:
            msg = client.recv(2048).decode('utf-8')
            print("\nThere was a transaction\n")
            msg = msg.split()
            amount_received = int(msg[2])
            hash_received = msg[1]
            sender = msg[0]

            if ( hash_received == my_hash ):
                print("You received a transaction de : ", sender)
                balance = balance + amount_received
                print('\nYour current balance is: ', balance)

        except:
            print('\nIt was not possible to remain connected to the server!\n')
            print('Press <ENTER> to continue...')
            client.close()
            break
            

def sendMessages(client, username):
    global balance
    global my_hash

    while True:
        try:
            option = "x"
            print(" Tighten 'y' to start a transaction or 'n' to leave: ")
            option = input('\n')
            if (option == 'y') :
                destination = input('\nEnter the recipients hash :')
                value = input('\nEnter the amount to be sent:')
                balance = balance - int(value)
                print('Amount sent, your current balance is: ', balance)
                client.send(f'<{username}> {destination} {value}'.encode('utf-8'))
            elif (option == 'n') :
                client.close()
                break                
            else :
                print('\nInvalid option')
        except:
            return

def updateHash(client):
    global my_hash
    while True:
        print('Your hash will be updated in 1 hour')
        time.sleep(3600)
        my_hash = secrets.token_hex()

main()