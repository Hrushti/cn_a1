# Import socket module
import socket 
import os.path as path
import crypto_c as crypto
     

c = socket.socket()        
port = 4040               
c.connect(('localhost', port)) 

 
while (True):
    x = input().split(' ')
    if (x[0] == "CMD"):
        c.send(x[0].encode())
        print(c.recv(1024).decode())
        print()
    elif (x[0] == "LS"):
        c.send(x[0].encode())
        dir_list = c.recv(1024).decode().split("$")
        print(dir_list)
        print()
    elif (x[0] == "CD"):
        c.send(x[0].encode())
        c.send(x[1].encode())
        print(c.recv(1024).decode())
        print()
    elif (x[0] == "DWD"):
        downloadDir = "/a1/client"
        filename = x[1]
        c.send(x[0].encode())
        c.send(filename.encode())
        z = c.recv(1024).decode()
        if (z == 'NOK'):
            print('NOK')
            continue
        elif (z == 'OK'):
            with open(path.join(downloadDir, filename), 'wb') as file_to_write:
                data = c.recv(1024)
                if not data:
                    break
                file_to_write.write(data)
            file_to_write.close()
            crypto.substitute_decode(filename)
            print('OK')
        print()
    elif (x[0] == "UPD"):
        filename = x[1]
        file_exists = path.exists(filename)
        if (file_exists == False):
            print('NOK')
            print()
            continue
        crypto.substitute_encode(filename)
        c.send(x[0].encode())
        c.send(filename.encode())
        with open(filename, 'rb') as file_to_send:
            for data in file_to_send:
                c.sendall(data)
        print('OK')
        print()
    else:
        print('error')
        break

c.close()
