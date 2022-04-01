import socket
import tqdm
import os
from Crypto.PublicKey import RSA
from Crypto import Random

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 8090))
s.listen(5)

SEPARATOR = "<SEPARATOR>"

while True:
    clientsocket, address = s.accept()
    print(f'Koneksi dengan {address} berhasil!')
    # clientsocket.send(bytes('Selamat datang di server kami!', 'utf-8'))
    received = clientsocket.recv(4096).decode()
    filename, filesize = received.split(SEPARATOR)
    filename = os.path.basename(filename)
    filesize = int(filesize)

    # start receiving the file from the socket
    # and writing to the file stream
    progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open('hasil'+filename, "wb") as f:
        while True:
            # read 1024 bytes from the socket (receive)
            bytes_read = clientsocket.recv(4096)
            if not bytes_read:    
                # nothing is received
                # file transmitting is done
                break
            # write to the file the bytes we just received
            f.write(bytes_read)
            # update the progress bar
            progress.update(len(bytes_read))

    # close the client socket
    clientsocket.close()
    # close the server socket
    s.close()