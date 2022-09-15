# import modules
import socket 
import os
import os.path as path
import crypto_c as crypto
     
# create socket
c = socket.socket()        
port = 4040               
c.connect(('localhost', port)) 

curr_dir = os.getcwd()

# process commands
while (True):
    inputs = input().split(' ')

    # get working directory
    if (inputs[0].casefold() == "CWD".casefold()):
        c.send(inputs[0].encode())
        print(c.recv(1024).decode())
        print()

    # list files and folders
    elif (inputs[0].casefold() == "LS".casefold()):
        c.send(inputs[0].encode())
        dir_list = c.recv(1024).decode().split("$")
        print(dir_list)
        print()

    # change directory to directory mentioned
    elif (inputs[0].casefold() == "CD".casefold()):
        try:
            os.chdir(path)
            curr_dir = os.getcwd()
        except: 
            None
        c.send(inputs[0].encode())
        c.send(inputs[1].encode())
        print(c.recv(1024).decode())
        print()

    # download file on server to client
    elif (inputs[0].casefold() == "DWD".casefold()):
        c.send(inputs[0].encode())
        encryptmode = inputs[-1]
        if encryptmode not in ['-pt', '-sb', '-tp']:
            encryptmode = '-pt'
        c.send(encryptmode.encode())

        downloadDir = curr_dir
        filename = os.path.basename(inputs[1])
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

            if encryptmode == '-sb':
                crypto.substitute_decode(filename)
            elif encryptmode == '-tp':
                crypto.transpose_encode_decode(filename)
            else:
                continue

            print('OK')
        print()

    #  upload file on client to server
    elif (inputs[0].casefold() == "UPD".casefold()):
        c.send(inputs[0].encode())
        encryptmode = inputs[-1]
        if encryptmode not in ['-pt', '-sb', '-tp']:
            encryptmode = '-pt'
        c.send(encryptmode.encode())

        filename = os.path.basename(inputs[1])
        filedir = path.join(curr_dir, filename)
        file_exists = path.isfile(filedir)
        if (file_exists == False):
            print('NOK')
            print()
            continue
        if encryptmode == '-sb':
                crypto.substitute_decode(filedir)
        elif encryptmode == '-tp':
            crypto.transpose_encode_decode(filedir)
        else:
            continue
        c.send(filedir.encode())
        with open(filename, 'rb') as file_to_send:
            for data in file_to_send:
                c.sendall(data)
        os.remove(filedir)
        print('OK')
        print()

    # invalid operation, exit
    else:
        print('error')
        break

# close connection
c.close()
